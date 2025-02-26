# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains classes for handling Firefox Panel UI (Hamburger menu)."""

from selenium.webdriver.common.by import By
import time
from foxpuppet.windows.browser.navbar import NavBar
from selenium.webdriver.remote.webelement import WebElement
from typing import Type, Any, TYPE_CHECKING, Optional
from selenium.webdriver.support import expected_conditions as EC


class PanelUI(NavBar):
    """Handles interaction with Panel UI."""

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

    @property
    def is_update_available(self) -> bool:
        """
        Checks if the Panel UI button indicates a pending Firefox update.

        Returns:
            bool: True if an update notification (barge) is present, False otherwise.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            update_status = self.selenium.find_element(
                *PanelUILocators.PANEL_UI_BUTTON
            ).get_attribute("barged")
            return update_status == "true"

    def open_panel_menu(self) -> None:
        """
        Opens the Panel UI menu.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.PANEL_UI_BUTTON).click()
            self.wait.until(
                EC.presence_of_element_located(*PanelUILocators.PANEL_POPUP),
                message="Panel UI menu did not open",
            )

    def open_new_tab(self) -> None:
        """
        Opens a new tab using the Panel UI menu.
        """
        initial_handles = set(self.selenium.window_handles)
        self.open_panel_menu()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.NEW_TAB).click()
            self.wait.until(
                lambda _: set(self.selenium.window_handles) - initial_handles,
                message="New Tab did not open",
            )
            new_tab = (set(self.selenium.window_handles) - initial_handles).pop()
            self.selenium.switch_to.window(new_tab)

    def open_new_window(self) -> None:
        """
        Opens a new window using the Panel UI menu.
        """
        initial_handles = set(self.selenium.window_handles)
        self.open_panel_menu()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.NEW_WINDOW).click()
            self.wait.until(
                lambda _: set(self.selenium.window_handles) - initial_handles,
                message="New window did not open",
            )
            new_window = (set(self.selenium.window_handles) - initial_handles).pop()
            self.selenium.switch_to.window(new_window)
            self.wait.until(
                lambda _: self.selenium.execute_script("return document.readyState")
                == "complete",
                message="New window document not fully loaded",
            )

    def open_private_window(self) -> None:
        """
        Opens a new window in private browsing mode using the Panel UI menu.
        """
        initial_handles = set(self.selenium.window_handles)
        self.open_panel_menu()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.PRIVATE_WINDOW).click()
            self.wait.until(
                lambda _: set(self.selenium.window_handles) - initial_handles,
                message="Private window did not open",
            )
            from foxpuppet.windows.browser.window import BrowserWindow

            new_private_window = self.selenium.window_handles[-1]
            try:
                private_window = BrowserWindow(
                    self.selenium, new_private_window
                ).is_private
                if private_window:
                    self.selenium.switch_to.window(new_private_window)
            except Exception as e:
                raise Exception(f"The new window is not private: {str(e)}")

    def open_history_menu(self) -> None:
        """
        Opens the History in Panel UI Menu
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*PanelUILocators.HISTORY).click()
            self.wait.until(
                lambda _: self.selenium.find_element(
                    *PanelUILocators.PANEL_HISTORY
                ).is_displayed(),
                message="History menu did not open",
            )


class History(PanelUI):
    def history_items(self) -> list[WebElement]:
        """
        Retrieves all history items from the Panel UI history menu.

        Returns:
            list[WebElement]: List of WebElement objects representing history items.
                Returns an empty list if no history items are found.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            history_items = self.selenium.find_elements(
                *PanelUILocators.RECENT_HISTORY_ITEMS
            )
            return history_items

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
        time.sleep(1)


class PanelUILocators:
    CLEAR_HISTORY_EVERYTHING = (By.CSS_SELECTOR, "menuitem[value='0']")
    CLEAR_RECENT_HISTORY = (By.ID, "appMenuClearRecentHistory")
    CLEAR_RECENT_HISTORY_BUTTON = (By.CSS_SELECTOR, "button[dlgtype='accept']")
    DROPDOWN_HISTORY = (By.ID, "sanitizeDurationChoice")
    HISTORY = (By.ID, "appMenu-history-button")
    HISTORY_DIALOG_BUTTON = (By.CSS_SELECTOR, "dialog[defaultButton='accept']")
    HISTORY_IFRAME = (By.CSS_SELECTOR, "browser.dialogFrame")
    NEW_TAB = (By.ID, "appMenu-new-tab-button2")
    NEW_WINDOW = (By.ID, "appMenu-new-window-button2")
    PANEL_HISTORY = (By.ID, "PanelUI-history")
    PANEL_POPUP = ((By.ID, "appMenu-popup"),)
    PANEL_UI_BUTTON = (By.ID, "PanelUI-menu-button")
    PRIVATE_WINDOW = (By.ID, "appMenu-new-private-window-button2")
    RECENT_HISTORY_ITEMS = (
        By.CSS_SELECTOR,
        "#appMenu_historyMenu toolbarbutton.subviewbutton",
    )


PANEL_ITEMS = {
    "PanelUI-menu-button": PanelUI,
    "appMenu-history-button": History,
}
