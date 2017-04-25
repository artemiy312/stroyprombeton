from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase

from stroyprombeton.models import Product
from stroyprombeton.tests.helpers import wait


class SeleniumTestCase(LiveServerTestCase):
    """Common superclass for running selenium-based tests."""

    fixtures = ['dump.json']

    @classmethod
    def setUpClass(cls):
        """Instantiate browser instance."""
        super(SeleniumTestCase, cls).setUpClass()
        capabilities = {
            'browserName': 'chrome',
            'mobileEmulation': {
                'deviceName': 'Apple iPhone 5'
            },
        }
        cls.browser = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub',
                                       desired_capabilities=capabilities)
        cls.browser.implicitly_wait(5)
        cls.browser.set_window_size(640, 320)

    @classmethod
    def tearDownClass(cls):
        """Close selenium session."""
        cls.browser.quit()
        super(SeleniumTestCase, cls).tearDownClass()


class Mobile(SeleniumTestCase):

    def setUp(self):
        """Set up testing urls and dispatch selenium webdriver."""
        self.browser.get(self.live_server_url)
        self.toggler = 'js-mobile-menu-toggler'

    def test_cart(self):
        """Cart should updated after Product buy."""
        product_id = Product.objects.first().id
        product_page = self.live_server_url + reverse('product', args=(product_id,))
        self.browser.get(product_page)

        offer_section = self.browser.find_element_by_class_name('product-order')
        self.browser.execute_script('return arguments[0].scrollIntoView();', offer_section)
        self.browser.find_element_by_id('buy-product').click()
        wait(2)
        size = self.browser.find_element_by_class_name('js-cart-size').text
        price = self.browser.find_element_by_class_name('js-mobile-cart-price').text

        self.assertEqual(int(size), 1)
        self.assertEqual(int(price), 1000)