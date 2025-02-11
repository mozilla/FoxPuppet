# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains BrowserWindow object representing the Firefox browser."""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from foxpuppet import expected
from foxpuppet.windows import BaseWindow
from foxpuppet.windows.browser.navbar import NavBar
from foxpuppet.windows.browser.notifications import BaseNotification
from foxpuppet.windows.browser.bookmarks.bookmark import Bookmark
from foxpuppet.windows.browser.panel_ui.panel_ui import PanelUI
from selenium.webdriver.remote.webelement import WebElement
from typing import Any, Optional, Union, TypeVar, Type

T = TypeVar("T", bound="BaseNotification")
P = TypeVar("P", bound="PanelUI")


class BrowserWindow(BaseWindow):
    """Representation of a browser window."""

    _bookmark_locator = (By.ID, "main-window")
    _file_menu_button_locator = (By.ID, "file-menu")
    _file_menu_private_window_locator = (By.ID, "menu_newPrivateWindow")
    _file_menu_new_window_button_locator = (By.ID, "menu_newNavigator")
    _nav_bar_locator = (By.ID, "nav-bar")
    _notification_locator = (By.CSS_SELECTOR, "#notification-popup popupnotification")
    _panel_ui_locator = (By.ID, "PanelUI-menu-button")
    _app_menu_notification_locator = (
        By.CSS_SELECTOR,
        "#appMenu-notification-popup popupnotification",
    )
    _app_menu_panel_ui_locator = (
        By.CSS_SELECTOR,
        "#appMenu-mainView .panel-subview-body toolbarbutton",
    )
    _tab_browser_locator = (By.ID, "tabbrowser-tabs")

    @property
    def navbar(self) -> NavBar:
        """Provide access to the Navigation Bar.

        Returns:
            :py:class:`NavBar`: FoxPuppet NavBar object.

        """
        window = BaseWindow(self.selenium, self.selenium.current_window_handle)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            el: WebElement = self.selenium.find_element(*self._nav_bar_locator)
            return NavBar(window, el)

    @property
    def notification(self) -> BaseNotification | Any:
        """Provide access to the currently displayed notification.

        Returns:
            :py:class:`BaseNotification`: FoxPuppet BaseNotification object.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            try:
                root = self.selenium.find_element(*self._notification_locator)
                return BaseNotification.create(self, root)
            except NoSuchElementException:
                pass
            try:
                notifications = self.selenium.find_elements(
                    *self._app_menu_notification_locator
                )
                root = next(n for n in notifications if n.is_displayed())
                return BaseNotification.create(self, root)
            except StopIteration:
                pass
        return None  # no notification is displayed

    @property
    def bookmark(self) -> Bookmark:
        """Provide access to the currently displayed bookmark.

        Returns:
            :py:class:`BaseBookmark`: FoxPuppet BasicBookmark object.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            root = self.selenium.find_element(*self._bookmark_locator)
            return Bookmark.create(self, root)

    @property
    def panel(self) -> PanelUI | Any:
        panel_root = None
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            root = self.selenium.find_element(*self._panel_ui_locator)
            panel_root = PanelUI.create(self, root)

            panel_items = self.selenium.find_elements(*self._app_menu_panel_ui_locator)
            for item in panel_items:
                _id = item.get_property("id")
                from foxpuppet.windows.browser.panel_ui.panel_ui import PANEL_ITEMS

                if _id in PANEL_ITEMS and item.is_displayed():
                    panel_root = PANEL_ITEMS[_id].create(self, item)  # type: ignore

        return panel_root

    def wait_for_notification(
        self,
        notification_class: Optional[Type[T]] = BaseNotification,  # type: ignore
    ) -> Optional[T]:
        """Wait for the specified notification to be displayed.

        Args:
            notification_class (:py:class:`BaseNotification`, optional):
                The notification class to wait for. If `None` is specified it
                will wait for any notification to be closed. Defaults to
                `BaseNotification`.

        Returns:
            Optional[:py:class:`BaseNotification`]: Firefox notification or None.

        """
        if notification_class:
            if notification_class is BaseNotification:
                message = "No notification was shown."
            else:
                message = "{0} was not shown.".format(notification_class.__name__)
            self.wait.until(
                lambda _: isinstance(self.notification, notification_class),
                message=message,
            )
            return self.notification  # type: ignore
        else:
            self.wait.until(
                lambda _: self.notification is None,
                message="Unexpected notification shown.",
            )
            return None

    def wait_for_bookmark(self) -> Bookmark:
        """Wait for the bookmark panel to be displayed.

        Returns:
            Optional[Bookmark]: The Bookmark object if found, or None if not found.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            message = "Bookmark panel was not shown."

            self.wait.until(
                lambda _: self.bookmark is not None,
                message=message,
            )
            return self.bookmark

    def wait_for_panel(
        self, panel_ui_class: Optional[Type[P]] = PanelUI  # type: ignore
    ) -> Optional[P]:
        """Wait for the specified PanelUI item to be displayed.

        Args:
            panel_ui_class (:py:class:`PanelUI`, optional):
                The PanelUI subclass to wait for. If `None` is specified, it
                will wait for any panel UI to be displayed. Defaults to `PanelUI`.

        Returns:
            Optional[:py:class:`PanelUI`]: The displayed PanelUI or `None` if not found.
        """
        if panel_ui_class:
            if panel_ui_class is PanelUI:
                message = "No panel UI was shown."
            else:
                message = f"{panel_ui_class.__name__} was not shown."
            self.wait.until(
                lambda _: isinstance(self.panel, panel_ui_class),
                message=message,
            )
            return self.panel  # type: ignore
        else:
            self.wait.until(
                lambda _: self.panel is None,
                message="Unexpected panel UI was shown.",
            )
            return None

    @property
    def is_private(self) -> bool | Any:
        """Property that checks if the specified window is private or not.

        Returns:
            bool: True if this is a Private Browsing window.

        """
        self.switch_to()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.selenium.execute_async_script(
                """
                let callback = arguments[arguments.length - 1];
                (async () => {
                    try {
                        const mod = await import("resource://gre/modules/PrivateBrowsingUtils.sys.mjs");
                        let chromeWindow = arguments[0].ownerDocument.defaultView;

                        callback(mod.PrivateBrowsingUtils.isWindowPrivate(chromeWindow));
                    } catch (e) {
                        callback({error: e.message});
                    }
                })();
                """,
                self.document_element,
            )

    def open_window(self, private: bool = False) -> Union["BrowserWindow", Any]:
        """Open a new browser window.

        Args:
            private (bool): Optional parameter to open a private browsing
                window. Defaults to False.

        Returns:
            :py:class:`BrowserWindow`: Opened window.

        """
        handles_before: list[str] = self.selenium.window_handles
        self.switch_to()

        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            # Opens private or non-private window
            self.selenium.find_element(*self._file_menu_button_locator).click()
            if private:
                self.selenium.find_element(
                    *self._file_menu_private_window_locator
                ).click()
            else:
                self.selenium.find_element(
                    *self._file_menu_new_window_button_locator
                ).click()

        return self.wait.until(
            expected.new_browser_window_is_opened(self.selenium, handles_before),
            message="No new browser window opened",
        )
