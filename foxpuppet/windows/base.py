# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Handles creation of a base object for interacting with Firefox windows."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class BaseWindow(object):
    """A base window model."""

    _document_element = (By.CSS_SELECTOR, ":root")

    def __init__(self, selenium: WebDriver, handle: str) -> None:
        """Create a BaseWindow object.

        Args:
            selenium:
                (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
                Firefox WebDriver object.
            handle: (str): WebDriver Firefox window handle.
        """
        self.selenium: WebDriver = selenium
        self.handle: str = handle
        self.wait: WebDriverWait = WebDriverWait(self.selenium, timeout=10)

    @property
    def document_element(self) -> WebElement:
        """Return the inner DOM window element.

        Returns:
            :py:class:`~selenium.webdriver.remote.webelement.WebElement`:
                WebDriver element object for the DOM window element.

        """
        return self.selenium.find_element(*self._document_element)

    @property
    def firefox_version(self) -> int:
        """Major version of Firefox in use.

        Returns:
            int: Major component of the Firefox version.

        """
        version: str = self.selenium.capabilities["browserVersion"]
        return int(version.partition(".")[0])

    def close(self) -> None:
        """Close the window."""
        self.switch_to()
        self.selenium.close()

    def switch_to(self) -> None:
        """Switch focus for Selenium commands to this window."""
        self.selenium.switch_to.window(self.handle)
