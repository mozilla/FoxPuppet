# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from FoxPuppet.foxpuppet import FoxPuppet

from selenium.webdriver.common.by import By


class BrowserWindow(FoxPuppet):
    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _nav_bar_locator = (By.ID, 'nav-bar')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')

    def __init__(self, selenium, *args, **kwargs):
        super().__init__(selenium)

    @property
    def is_private(self):
        """Returns True if this is a Private Browsing window."""

        self.selenium.set_context('chrome')
        return self.selenium.execute_script("""
                Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                let chromeWindow = arguments[0].ownerDocument.defaultView;
                return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
            """, self.windows.window_element)
        self.selenium.set_context('content')

    @property
    def handle(self):
        return self._handle

    @property
    def closed(self):
        """Returns closed state of the chrome window.

        :returns: True if the window has been closed.
        """
        return self.handle not in self.selenium.chrome_window_handles

    @property
    def focused(self):
        """Returns `True` if the chrome window is focused.

        :returns: True if the window is focused.
        """
        self.switch_to()

        return self.handle == self.windows.focused_chrome_window_handle

    def switch_to(self, focus=False):
        """Switches the context to this chrome window.

        By default it will not focus the window. If that behavior is wanted,
        the `focus` parameter can be used.

        :param focus: If `True`, the chrome window will be focused.

        :returns: Current window as :class:`BaseWindow` instance.
        """
        if focus:
            self.windows.focus(self.handle)
        else:
            self.windows.switch_to(self.handle)

        return self

    def open_window(self, private=False):
        self.selenium.set_context('chrome')
        self.selenium.find_element(*self._file_menu_button_locator).click()
        with self.windows.wait_for_new_window():
            if private:
                self.selenium.find_element(
                    *self._file_menu_private_window_locator).click()
            else:
                self.selenium.find_element(
                    *self._file_menu_new_window_button_locator).click()
        self.selenium.set_context('content')
