(() => {
  const DOM = {
    $order: $('.js-order-contain'),
    productCount: '.js-count-input',
    remove: '.js-remove',
  };

  const init = () => {
    setUpListeners();
  };

  function setUpListeners() {
    mediator.subscribe('onCartUpdate', render);

    $(DOM.$order).on('keyup', 'input', storeInput);
    $(DOM.$order).on('keyup', 'textarea', storeInput);
    $(DOM.$order).on('input', DOM.productCount, helpers.debounce(changeProductCount, 300));
    $(DOM.$order).on('click', DOM.remove, removeProduct);
  }

  const getProductId = $target => $target.closest('.js-product-row').data('product-id');

  /**
   * Change Product's count in Cart with delay for better UX.
   */
  function changeProductCount(event) {
    const $target = $(event.target);
    const productID = getProductId($target);
    const newCount = $target.closest('.js-product-row').find(DOM.productCount).val();

    server.changeInCart(productID, newCount)
      .then(data => mediator.publish('onCartUpdate', { html: data }));
  }

  /**
   * Store inputted value into localStorage.
   */
  function storeInput(event) {
    const $target = $(event.target);
    localStorage.setItem($target.attr('name'), $target.val());
  }

  /**
   * Remove product from Cart's table.
   */
  function removeProduct(event) {
    const productID = getProductId($(event.target));

    server.removeFromCart(productID)
      .then(data => mediator.publish('onCartUpdate', { html: data }));
  }

  /**
   * Add order's table and form html into the page.
   */
  function render(_, data) {
    const html = data.html || data;
    DOM.$order.html(html.table);
  }

  init();
})();
