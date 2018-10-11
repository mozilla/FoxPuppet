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


class BrowserWindow(BaseWindow):
    """Representation of a browser window."""

    _file_menu_button_locator = (By.ID, "file-menu")
    _file_menu_private_window_locator = (By.ID, "menu_newPrivateWindow")
    _file_menu_new_window_button_locator = (By.ID, "menu_newNavigator")
    _nav_bar_locator = (By.ID, "nav-bar")
    _notification_locator = (By.CSS_SELECTOR, "#notification-popup popupnotification")
    _app_menu_notification_locator = (
        By.CSS_SELECTOR,
        "#appMenu-notification-popup popupnotification",
    )
    _tab_browser_locator = (By.ID, "tabbrowser-tabs")

    @property
    def navbar(self):
        """Provide access to the Navigation Bar.

        Returns:
            :py:class:`NavBar`: FoxPuppet NavBar object.

        """
        window = BaseWindow(self.selenium, self.selenium.current_window_handle)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            el = self.selenium.find_element(*self._nav_bar_locator)
            return NavBar(window, el)

    @property
    def notification(self):
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

    def wait_for_notification(self, notification_class=BaseNotification):
        """Wait for the specified notification to be displayed.

        Args:
            notification_class (:py:class:`BaseNotification`, optional):
                The notification class to wait for. If `None` is specified it
                will wait for any notification to be closed. Defaults to
                `BaseNotification`.

        Returns:
            :py:class:`BaseNotification`: Firefox notification.

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
            return self.notification
        else:
            self.wait.until(
                lambda _: self.notification is None,
                message="Unexpected notification shown.",
            )

    @property
    def is_private(self):
        """Property that checks if the specified window is private or not.

        Returns:
            bool: True if this is a Private Browsing window.

        """
        self.switch_to()
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.selenium.execute_script(
                """
                Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                let chromeWindow = arguments[0].ownerDocument.defaultView;
                return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
                """,
                self.document_element,
            )

    def open_window(self, private=False):
        """Open a new browser window.

        Args:
            private (bool): Optional parameter to open a private browsing
                window. Defaults to False.

        Returns:
            :py:class:`BrowserWindow`: Opened window.

        """
        handles_before = self.selenium.window_handles
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
