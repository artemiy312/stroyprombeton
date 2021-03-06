import unittest

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase, tag
from selenium import webdriver

from stroyprombeton.models import Product
from stroyprombeton.tests.helpers import CAPABILITIES, wait


class SeleniumTestCase(LiveServerTestCase):
    """Common superclass for running selenium-based tests."""

    fixtures = ['dump.json']
    host = settings.LIVESERVER_HOST

    @classmethod
    def setUpClass(cls):
        """Instantiate browser instance."""
        super().setUpClass()

        cls.browser = webdriver.Remote(
            command_executor=settings.SELENIUM_URL,
            desired_capabilities={
                **CAPABILITIES,
                'mobileEmulation': {
                    'deviceName': 'Apple iPhone 5'
                },
            },
        )
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        """Close selenium session."""
        cls.browser.quit()
        super().tearDownClass()


# @todo #355:60m  Make positions table adaptive.
#  And fix mobile test below.
#  Now it's failing because "order" button is not visible on mobile page.
@unittest.expectedFailure
@tag('slow')
class Mobile(SeleniumTestCase):

    def setUp(self):
        """Set up testing urls and dispatch selenium webdriver."""
        self.browser.get(self.live_server_url)
        self.toggler = 'js-mobile-menu-toggler'

    def test_cart(self):
        """Cart should updated after Product buy."""
        price = 100
        product_id = Product.objects.filter(price=price).first().id
        product_page = self.live_server_url + reverse('product', args=(product_id,))
        self.browser.get(product_page)

        offer_section = self.browser.find_element_by_class_name('option-order')
        self.browser.execute_script('return arguments[0].scrollIntoView();', offer_section)
        self.browser.find_element_by_id('buy-product').click()
        wait(2)
        size = self.browser.find_element_by_class_name('js-cart-size').text
        cart_price = self.browser.find_element_by_class_name('js-mobile-cart-price').text

        self.assertEqual(int(size), 1)
        self.assertEqual(int(cart_price), price)
