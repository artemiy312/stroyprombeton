const mainPage = (() => {
  const DOM = {
    $btnScrollTop: $('#btn-scroll-to-top'),
    $scrollWrapper: $('#scroll-wrapper'),
    $tooltip: $('.js-tooltip'),
    tooltipContent: '.js-tooltip-content',
  };

  const CONFIG = {
    scrollbar: {
      autoReinitialise: true,
      mouseWheelSpeed: 30,
    },
  };

  const init = () => {
    pluginsInit();
    setupXHR();
    setUpListeners();
  };

  // TODO: move to config module
  // http://youtrack.stkmail.ru/issue/dev-748
  const setupXHR = () => {
    const csrfUnsafeMethod = (method) => !(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    const token = Cookies.get('csrftoken');

    $.ajaxSetup({
      beforeSend: (xhr, settings) => {
        if (csrfUnsafeMethod(settings.type)) {
          xhr.setRequestHeader('X-CSRFToken', token);
        }
      },
    });
  };

  const setUpListeners = () => {
    $(window).scroll(toggleToTopBtn);
    DOM.$btnScrollTop.on('click', () => $('html, body').animate({ scrollTop: 0 }, 300));
    DOM.$tooltip.click(event => showTooltip($(event.target).next()));
  };

  const pluginsInit = () => {
    console.warn('Here will be plugins initialization.');
  };

  const enableScrollToTop = () => {
    DOM.$btnScrollTop.addClass('active');
  };

  const disableScrollToTop = () => {
    DOM.$btnScrollTop.removeClass('active');
  };
  
  const showTooltip = $item => {
    $item.fadeIn();
    setTimeout(() => $item.fadeOut(), 1000);
  };

  /**
   * Toggles to top button.
   */
  const toggleToTopBtn = () => {
    ($(window).scrollTop() > 300) ? enableScrollToTop() : disableScrollToTop();
  };

  init();
})();
