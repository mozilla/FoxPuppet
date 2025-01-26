# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains classes for handling Firefox Panel UI (Hamburger menu)."""

from abc import ABCMeta

from selenium.webdriver.common.by import By

from foxpuppet.region import Region
from selenium.webdriver.remote.webelement import WebElement
from typing import Type, Any, TYPE_CHECKING, Optional


class PanelUI(Region):
    """Handles interaction with Panel UI."""

    __metaclass__ = ABCMeta
    if TYPE_CHECKING:
        from foxpuppet.windows import BrowserWindow

    @staticmethod
    def create(
        window: Optional["BrowserWindow"], root: WebElement
    ) -> Type["PanelUI"] | Any:
        """Create a Panel UI object.

        Args:
            window (:py:class:`BrowserWindow`): Window object this region
                appears in.
            root
                (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
                WebDriver element object that serves as the root for the
                Panel UI.

        Returns:
            :py:class:`PanelUI`: Firefox Panel UI.

        """
        panel_items: dict = {}
        _id: str | bool | WebElement | dict = root.get_property("id")

        panel_items.update(PANEL_ITEMS)
        return panel_items.get(_id, PanelUI)(window, root)

    def open_panel_menu(self) -> None:
        """
        Opens the Panel UI menu.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.PANEL_UI_BUTTON).click()

    def open_private_window(self) -> None:
        """
        Opens a new window in private browsing mode using the Panel UI menu.
        """
        # self.open_panel_menu()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.PRIVATE_WINDOW).click()

    def open_history_menu(self) -> None:
        """
        Opens the History in Panel UI Menu
        """
        # self.open_panel_menu()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.HISTORY).click()

    def wait_for_num_windows_or_tabs(self, expected_count: int) -> None:
        """
        Waits until the number of open browser windows or tabs matches the expected value.

        Args:
            expected_count (int): The expected number of windows or tabs.
        """
        self.wait.until(
            lambda _: len(self.driver.window_handles) == expected_count,
            f"Expected {expected_count} windows or tabs, but found {len(self.driver.window_handles)}",
        )

    def switch_to_new_window_or_tab(self) -> None:
        """Get list of all window handles, switch to the newly opened tab/window"""
        handles = self.selenium.window_handles
        self.selenium.switch_to.window(handles[-1])


class History(PanelUI):
    """Handles interactions with Firefox History."""

    def is_present(self, link: str) -> bool:
        """
        Checks if a specific link is present in the recent history.
        Args:
            link `str`: The URL or part of the URL to check for in the recent history.

        Returns:
            bool: `True` if the link is present in the recent history, `False` otherwise.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            history_items = self.selenium.find_elements(
                *PanelUILocators.RECENT_HISTORY_ITEMS
            )
            for item in history_items:
                item_src = item.get_attribute("image")
                if item_src and link in item_src:
                    print(item_src)
                    return True
            return False

    def clear_history(self):
        """
        Clears the browsing history.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.CLEAR_RECENT_HISTORY).click()
            self.selenium.switch_to.frame(
                self.selenium.find_element(*PanelUILocators.HISTORY_IFRAME)
            )
            with self.selenium.context(self.selenium.CONTEXT_CONTENT):
                self.selenium.find_element(*PanelUILocators.DROPDOWN_HISTORY).click()
                self.selenium.find_element(
                    *PanelUILocators.CLEAR_HISTORY_EVERYTHING
                ).click()
                self.selenium.execute_script(
                    """
                const shadowHost = arguments[0];
                    const shadowRoot = shadowHost.shadowRoot;
                    const clearRecentHistoryButton = shadowRoot.querySelector('button[dlgtype="accept"]');
                    clearRecentHistoryButton.click();
                """,
                    self.selenium.find_element(*PanelUILocators.HISTORY_DIALOG_BUTTON),
                )
            self.selenium.switch_to.default_content()


class PrivateWindow(PanelUI):
    """Handles interactions with Firefox Private Window."""

    def verify_private_browsing_links_not_in_awesome_bar(self, links: list) -> list:
        """
        Verifies that the provided links visited in private browing session do not appear in the awesome bar.
        Args:
            links `list`: A list of links to be verified.

        Returns:
            list: A list of links that appeared in the awesome bar during private browsing.
        """
        invalid_links = []
        initial_window_handle = self.driver.current_window_handle
        # self.open_private_window()
        self.switch_to_new_window_or_tab()

        for link in links:
            self.selenium.get(link)

        self.driver.switch_to.window(initial_window_handle)

        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            for link in links:
                awesome_bar = self.selenium.find_element(*PanelUILocators.INPUT_FIELD)
                awesome_bar.clear()
                awesome_bar.send_keys(link)

                self.wait.until(
                    lambda _: self.selenium.find_elements(*PanelUILocators.SEARCH_RESULTS)
                )

                search_results = self.selenium.find_elements(
                    *PanelUILocators.SEARCH_RESULTS
                )
                if any(link in result.text for result in search_results):
                    invalid_links.append(link)

        return invalid_links

    def verify_private_browsing_links_not_in_history(
        self, links: list, history: History
    ) -> list:
        """
        Verifies that the provided links visited in private browsing session do not appear in the history.
        Args:
        links (`list[str]`): List of URLs visited during private browsing session
        history (`History`): An instance of the History class used to check if a link is present in the history.

        Returns:
            list: A list of links that were found in the history during the private browsing session.
        """
        invalid_links = []
        initial_window_handle = self.driver.current_window_handle
        # self.open_private_window()
        self.switch_to_new_window_or_tab()

        for link in links:
            self.selenium.get(link)

        self.selenium.switch_to.window(initial_window_handle)
        self.open_panel_menu()
        self.open_history_menu()
        for link in links:
            if history.is_present(link):
                invalid_links.append(link)
        return invalid_links


class PanelUILocators:
    PANEL_UI_BUTTON = (By.ID, "PanelUI-menu-button")
    PRIVATE_WINDOW = (By.ID, "appMenu-new-private-window-button2")
    HISTORY = (By.ID, "appMenu-history-button")
    CLEAR_RECENT_HISTORY = (By.ID, "appMenuClearRecentHistory")
    CLEAR_RECENT_HISTORY_BUTTON = (By.CSS_SELECTOR, "button[dlgtype='accept']")
    CLEAR_HISTORY_EVERYTHING = (By.CSS_SELECTOR, "menuitem[value='0']")
    HISTORY_DIALOG_BUTTON = (By.CSS_SELECTOR, "dialog[defaultButton='accept']")
    DROPDOWN_HISTORY = (By.ID, "sanitizeDurationChoice")
    RECENT_HISTORY_ITEMS = (
        By.CSS_SELECTOR,
        "#appMenu_historyMenu toolbarbutton.subviewbutton",
    )
    HISTORY_IFRAME = (By.CSS_SELECTOR, "browser.dialogFrame")


PANEL_ITEMS = {
    "PanelUI-menu-button": PanelUI,
    "appMenu-history-button": History,
    "appMenu-new-private-window-button2": PrivateWindow,
}
