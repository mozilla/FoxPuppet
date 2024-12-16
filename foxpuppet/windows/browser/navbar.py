# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Creates Navbar object to interact with Firefox Navigation Bar."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from foxpuppet.region import Region
from typing import Tuple, Optional
from foxpuppet.windows.base import BaseWindow


class NavBar(Region):
    """Representation of the navigation bar.

    Args:
        window (:py:class:`BaseWindow`): Window object this region appears in.
        root
            (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
            WebDriver element object that serves as the root for the
            region.

    """

    _tracking_protection_shield_locator: Tuple[str, str] = (
        By.ID,
        "tracking-protection-icon-box",
    )

    def __init__(self, window: BaseWindow, root: WebElement) -> None:
        super().__init__(window, root)
        self.actions: ActionChains = ActionChains(self.selenium)

    @property
    def is_tracking_shield_displayed(self) -> bool:
        """Tracking Protection shield.

        Returns:
            bool: True or False if the Tracking Shield is displayed.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if self.window.firefox_version >= 63:  # Bug 1471713, 1476218
                el = self.root.find_element(*self._tracking_protection_shield_locator)
                return el.get_attribute("active") is not None
            el = self.root.find_element(By.ID, "tracking-protection-icon")
            return bool(el.get_attribute("state"))

    def click_element(self, locator: Tuple[str, str]) -> None:
        """Click on an element by its locator."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.find_element(locator).click()

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Find and return a web element by its locator."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            try:
                element = self.root.find_element(*locator)
                return element
            except Exception as e:
                raise NoSuchElementException(
                    f"Error locating element with locator {locator}: {e}"
                )

    def context_click(self, locator: Tuple[str, str]) -> None:
        """
        Perform a right-click (context-click) on an element.

        Args:
            locator (tuple): Locator for the element to right-click.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            element = self.find_element(locator)
            self.actions.context_click(element).perform()

    def switch_to_frame(self, locator: Tuple[str, str]) -> None:
        """
        Switch to an iFrame using its locator

        Args:
            locator (tuple): Locator for the iFrame elemeent.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            frame_element = self.find_element(locator)
            if frame_element is not None:
                self.selenium.switch_to.frame(frame_element)
            else:
                raise NoSuchElementException(f"iFrame with locator {locator} not found.")

    def switch_to_default_context(self) -> None:
        """Switch back to default context."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.switch_to.default_content()

    def open_main_menu(
        self, locator_toolbar: Tuple[str, str], locator_menu_bar: Tuple[str, str]
    ) -> None:
        """Activate main menu bar"""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.context_click(locator_toolbar)
            self.click_element(locator_menu_bar)

    def open_bookmark_menu(
        self, locator_panel: Tuple[str, str], locator_bookmark: Tuple[str, str]
    ) -> None:
        """
        Opens the Bookmarks menu in Panel UI
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.click_element(locator_panel)
            self.click_element(locator_bookmark)
