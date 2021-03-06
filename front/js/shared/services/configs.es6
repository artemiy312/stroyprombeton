/**
 * There are all common configs for all common plugins.
 * This module is an entry point for plugins initialization.
 */
const configs = (() => {  // Ignore ESLintBear (no-unused-vars)
  const DOM = {
    $mobileMenu: $('#mobile-menu'),
    $phoneInputs: $('.js-masked-phone'),
    $tooltipTarget: $('.js-object-tooltip.active'),
    $galleryItem: $('.js-photoswipe'),
    gallerySlide: '.js-photoswipe-slide',
  };

  const labels = {
    phone: 'phone',
  };

  let $menu;

  const init = () => {
    pluginsInit();
    setupXHR();
  };

  function pluginsInit() {
    initMmenu();

    DOM.$phoneInputs
      .attr('placeholder', '+7 (999) 000 00 00')
      .mask('+0 (000) 000 00 00');

    DOM.$tooltipTarget.tooltipster({
      anchor: 'bottom-center',
      contentAsHTML: true,
      interactive: true,
      maxWidth: 300,
      offset: [0, 20],
      trigger: 'custom',
      // close tooltip when element is clicked again,
      // tapped or when the mouse leaves it
      triggerClose: {
        click: true,
        // ensuring that scrolling mobile is not tapping
        scroll: false,
        tap: true,
        mouseleave: true,
      },
      // open tooltip when element is clicked, tapped (mobile) or hovered
      triggerOpen: {
        click: true,
        tap: true,
        mouseenter: true,
      },
    });

    /**
     * https://goo.gl/oF818r - Featherlight Gallery
     */
    DOM.$galleryItem.photoSwipe(DOM.gallerySlide, {
      closeOnScroll: false,
      fullscreenEl: false,
      shareEl: false,
    });
  }

  /**
   * Set all unsafe ajax requests with csrftoken.
   */
  function setupXHR() {
    const csrfUnsafeMethod = method => !(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

    $.ajaxSetup({
      beforeSend: (xhr, settings) => {
        if (csrfUnsafeMethod(settings.type)) {
          xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
        }
      },
    });
  }

  function initMmenu() {
    $menu = DOM.$mobileMenu.mmenu({
      extensions: [
        'border-offset', 'shadow-page',
        'shadow-panels', 'effect-menu-slide',
      ],
      iconPanels: true,
      screenReader: true,
      navbar: {
        title: 'Меню',
      },
    }, {
      offCanvas: {
        pageSelector: '#desktop-wrapper',
      },
    });
  }

  init();

  return {
    $menu,
    labels,
  };
})();
