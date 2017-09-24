(() => {
  const DOM = {
    addToCart: 'js-category-buy',
    tablaRow: '.table-tr',
    $cart: $('.js-cart'),
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
      .then(data => mediator.publish('onCartUpdate', { html: data, target: event.target }));
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
      offset: config.productsToFetch,
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
      filtered: data.filtered,
    });
  }

  init();
})();
