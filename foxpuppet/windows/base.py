# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BaseWindow(object):

    """
        A base window model.

        :param selenium: WebDriver object.
        :type selenium:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
        :param handle: A window handle.
        :type handle: str
    """

    _document_element = (By.CSS_SELECTOR, ':root')

    def __init__(self, selenium, handle):
        self.selenium = selenium
        self.handle = handle
        self.wait = WebDriverWait(self.selenium, timeout=10)

    @property
    def document_element(self):
        """ Returns the inner DOM window element.

        :return: DOM window element.
        :return type:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` locator
        """

        return self.selenium.find_element(*self._document_element)

    @property
    def firefox_version(self):
        """ Major version of Firefox in use.

        :returns: Major component of the Firefox version.
        :rtype: int
        """
        version = self.selenium.capabilities['browserVersion']
        return int(version.partition('.')[0])

    def close(self):
        """Closes the window."""
        self.switch_to()
        self.selenium.close()

    def switch_to(self):
        """Switches focus for Selenium commands to this window."""

        self.selenium.switch_to.window(self.handle)

    @contextmanager
    def open_new_element(self, elements_before, expected_class, timeout=10):
        """Context manager for opening any new <name>

        :param elements_before: Any elements open currently
        :param timeout: The time given, in seconds, to wait for the new element
         to open. Defaults to 10 seconds.
        :param expected_class: Class of the element that is going to be opened.
         Currently 'window' and 'tab' are supported.
        :type elements_before: str
        :type timeout: int
        :type expected_class: str
        """

        yield
        if expected_class == 'window':
            WebDriverWait(self.selenium, timeout).until(
                lambda driver: elements_before != len(driver.window_handles))
        elif expected_class == 'tab':
            from foxpuppet.windows.browser.tabbar import TabBar
            tabbar = TabBar(self.selenium)
            WebDriverWait(self.selenium, timeout).until(
                lambda driver: elements_before != len(tabbar.tabs))
