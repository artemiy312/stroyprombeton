(() => {
  // @todo #187:120m Move catalog's js code to refarm.catalog app.
  //  `refarm.catalog` sided js module should contain
  //  this functions: Tags, Pagination and DBTemplate.
  //  But see full feature set to implement on refarm side
  //  in refarm.catalog.context.

  // @todo #187:120m Take selenium tests for category page.
  //  And fix some front bugs: currently front has some.
  //  I don't describe them, tests will do it.
  const DOM = {
    addToCart: 'js-category-buy',
    tablaRow: '.table-tr',
    $cart: $('.js-cart'),
    $loadMoreBtn: $('#load-more-products'),
    $filtersWrapper: $('.js-tags-inputs'),
    $filtersApplyBtn: $('.js-apply-filter'),
    $showMoreLink: $('#load-more-products'),
    $productsTable: $('#products-wrapper'),
    $searchFilter: $('#search-filter'),
    $seoCategoryDescription: $('#js-category-description'),
    $seoCategoryDescriptionDestination: $('#js-category-description-destination'),
  };

  const config = {
    fetchProductsUrl: '/fetch-products/',
    productsToFetch: 30,
    totalProductsCount: parseInt($('.js-total-products').first().text(), 10),
  };

  const init = () => {
    setLoadMoreLinkState();
    setUpListeners();
    setUpFilters();
    moveCategoryDescription();
  };

  /**
   * Subscribing on events using mediator.
   */
  function setUpListeners() {
    mediator.subscribe('onCartUpdate', showTooltip);
    mediator.subscribe('onProductsFilter', updateLoadMoreLink, refreshProductsList);
    mediator.subscribe('onProductsLoad', updateLoadMoreLink, appendToProductsList);

    $(DOM.$productsTable).on('click', buyProduct);
    DOM.$showMoreLink.click(loadProducts);
    DOM.$searchFilter.keyup(helpers.debounce(filterProducts, 400));
    DOM.$filtersApplyBtn.click(loadFilteredProducts);
    DOM.$filtersWrapper.on('click', 'input', toggleApplyBtnState);
  }

  const TAGS_TYPE_DELIMITER = '-or-';
  const TAGS_GROUP_DELIMITER = '-and-';

  function serializeTags(tags) {
    const tagsByGroups = tags.reduce((group, item) => {
      const groupId = item.group;
      group[groupId] = group[groupId] || [];  // Ignore ESLintBear (no-param-reassign)
      group[groupId].push(item.slug);
      return group;
    }, {});

    return Object.keys(tagsByGroups).reduce((previous, current) => {
      const delim = previous ? TAGS_GROUP_DELIMITER : '';
      return previous + delim + tagsByGroups[current].join(TAGS_TYPE_DELIMITER);
    }, '');
  }

  function parseTags(string) {
    return string
      .split(TAGS_GROUP_DELIMITER)
      .map(group => group.split(TAGS_TYPE_DELIMITER))
      .reduce((acc, e) => acc.concat(e), []);
  }

  /**
   * Set up filter checkboxes based on query `tags` parameter.
   */
  function setUpFilters() {
    // /tags/от-сети-220-в-and-брелок/ => ['от-сети-220-в', 'брелок']
    const activeFilterIds = parseTags(helpers.getUrlEndpointParam('tags'));

    activeFilterIds.map(item => $(`#tag-${item}`).attr('checked', true));
    toggleApplyBtnState();
  }

  /**
   * Reloads current page with `tags` query parameter.
   */
  function loadFilteredProducts() {
    const $tagsObject = DOM.$filtersWrapper
      .find('input:checked')
      .map((_, checkedItem) => (
        {
          slug: $(checkedItem).data('tag-slug'),
          group: $(checkedItem).data('tag-group-id'),
        }
      ));
    const tags = serializeTags(Array.from($tagsObject));

    window.location.href = `${DOM.$loadMoreBtn.data('url')}tags/${tags}/`;
  }

  /**
   * Toggle apply filter btn active\disabled state based on
   * checked\unchecked checkboxes.
   */
  function toggleApplyBtnState() {
    const checkboxesArr = Array.from(DOM.$filtersWrapper.find('input'));
    const isSomeChecked = checkboxesArr.some(item => item.checked === true);

    DOM.$filtersApplyBtn.attr('disabled', !isSomeChecked);
  }

  function setLoadMoreLinkState() {
    if ($(DOM.tablaRow).size() < config.productsToFetch) {
      DOM.$showMoreLink.addClass('disabled');
    }
  }

  /**
   * Moves category description to bottom of page
   */
  function moveCategoryDescription() {  // Ignore ESLintBear (consistent-return)
    if (!DOM.$seoCategoryDescription.length) {
      return 0;
    }
    DOM.$seoCategoryDescription.detach().appendTo(DOM.$seoCategoryDescriptionDestination);
  }

  /**
   * Get product quantity & id from DOM.
   */
  const getProductInfo = (event) => {
    const $product = $(event.target);
    const productCount = $product.closest('td').prev().find('.js-count-input').val();
    const productId = $product.closest('tr').attr('id');

    return {
      count: parseInt(productCount, 10),
      id: parseInt(productId, 10),
    };
  };

  /**
   * Add product to Cart and update it.
   */
  function buyProduct(event) {
    if (!$(event.target).hasClass(DOM.addToCart)) return;
    const { id, count } = getProductInfo(event);

    server.addToCart(id, count)
      .then((data) => {
        mediator.publish('onCartUpdate', { html: data, target: event.target });
        mediator.publish('onProductAdd', [id, count]);
      });
  }

  /**
   * Show tooltip after adding Product to the Cart.
   */
  function showTooltip(_, data) {
    const $target = $(data.target).siblings().filter('.js-popover');

    $target.fadeIn();
    setTimeout(() => $target.fadeOut(), 1000);
  }

  const getLoadedProductsCount = () => parseInt(DOM.$showMoreLink.attr('data-load-count'), 10);
  const getFilterTerm = () => DOM.$searchFilter.val();
  const getCategoryId = () => DOM.$searchFilter.attr('data-category');

  /**
   * Update products to load data attribute counter.
   * Add 'disabled' attribute to button if there are no more products to load.
   *
   * @param {string} products - HTML string of fetched products
   */
  function updateLoadMoreLink(_, products) {
    const oldCount = getLoadedProductsCount();
    const newCount = oldCount + config.productsToFetch;
    const productsLoaded = countWord(products, 'table-tr');

    DOM.$showMoreLink.attr('data-load-count', newCount);

    if (productsLoaded < config.productsToFetch) {
      DOM.$showMoreLink.addClass('disabled');
    }
  }

  /**
   * Update Products list in DOM via appending HTML-list of loaded products to wrapper.
   *
   * @param {string} products - HTML string of fetched product's list
   */
  function appendToProductsList(_, products) {
    DOM.$productsTable.append(products);
  }

  /**
   * Insert filtered Products list.
   *
   * @param {string} products - HTML string of fetched product's list
   */
  function refreshProductsList(_, products) {
    DOM.$productsTable.html(products);
  }

  /**
   * Count word occurrence in string.
   *
   * @param {string} source - string to search occurrence in
   * @param {string} word - searched word in whole string
   * @return {number} count - word occurrence count in source string
   */
  function countWord(source, word) {
    let count = 0;
    let index = 0;

    while ((index = source.indexOf(word)) >= 0) {  // Ignore ESLintBear (no-cond-assign)
      source = source.substring(index + word.length);  // Ignore ESLintBear (no-param-reassign)
      count += 1;
    }

    return count;
  }

  /**
   * Load more products from back-end with/without filtering.
   * After products successfully loaded - publishes 'onProductLoad' event.
   */
  function loadProducts() {
    if (DOM.$showMoreLink.hasClass('disabled')) return;

    const fetchData = {
      categoryId: getCategoryId(),
      offset: getLoadedProductsCount(),
      limit: config.productsToFetch,
      filterValue: getFilterTerm(),
      filtered: getFilterTerm().length > 0,
    };

    fetchProducts(fetchData)
      .then(
        products => mediator.publish('onProductsLoad', products),
        response => console.warn(response),
      );
  }

  /**
   * Load filtered products from back-end by filter term on typing in filter field.
   * After products successfully loaded - publishes 'onProductsFilter' event.
   * Number `3` is minimal length for search term.
   */
  function filterProducts() {
    const filterValue = getFilterTerm();
    if (filterValue.length && filterValue.length < 3) return;

    const fetchData = {
      categoryId: getCategoryId(),
      filterValue,
      filtered: filterValue.length >= 3,
      offset: 0,
      limit: config.productsToFetch,
    };

    fetchProducts(fetchData)
      .then(
        (products) => {
          mediator.publish('onProductsFilter', products);
          DOM.$showMoreLink.attr('data-load-count', config.productsToFetch);
        },
        response => console.warn(response),
      );
  }

  /**
   * Load products from back-end by passed data.
   */
  function fetchProducts(data) {
    return $.post(config.fetchProductsUrl, {
      categoryId: data.categoryId,
      term: data.filterValue,
      offset: data.offset,
      limit: data.limit,
      filtered: data.filtered,
    });
  }

  init();
})();
