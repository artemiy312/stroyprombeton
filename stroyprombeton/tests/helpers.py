import time

from django.conf import settings
from django.test import override_settings, LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumrequests import Remote

disable_celery = override_settings(USE_CELERY=False)


def wait(seconds=1):
    """Simple wrapper on time.sleep() method."""
    time.sleep(seconds)


class BaseSeleniumTestCase(LiveServerTestCase):
    """Common superclass for running selenium-based tests."""

    @classmethod
    def setUpClass(cls):
        """Instantiate browser instance."""
        super().setUpClass()
        cls.browser = Remote(
            command_executor=settings.SELENIUM_URL,
            desired_capabilities=DesiredCapabilities.CHROME
        )
        cls.wait = WebDriverWait(cls.browser, 240)
        cls.browser.implicitly_wait(60)
        cls.browser.set_window_size(1920, 1080)

    @classmethod
    def tearDownClass(cls):
        """Close selenium session."""
        cls.browser.quit()
        super().tearDownClass()
