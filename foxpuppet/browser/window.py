# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.windows import Windows
from selenium.webdriver.common.by import By

from .navbar import Navbar
from .tabbar import Tabbar


class BrowserWindow(object):
    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _nav_bar_locator = (By.ID, 'nav-bar')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self.navbar = Navbar(selenium)
        self.tabbar = Tabbar(selenium)
        self._windows = Windows(selenium)

    @property
    def is_private(self):
        """Returns True if this is a Private Browsing window."""

        self.selenium.set_context('chrome')
        return self.selenium.execute_script("""
                Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                let chromeWindow = arguments[0].ownerDocument.defaultView;
                return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
            """, self._windows.window_element)
        self.selenium.set_context('content')

    def open_window(self, private=False):
        self.selenium.set_context('chrome')
        handles_before = self.selenium.window_handles
        self.selenium.find_element(*self._file_menu_button_locator).click()
        with self._windows.wait_for_new_window():
            if private:
                self.selenium.find_element(
                    *self._file_menu_private_window_locator).click()
            else:
                self.selenium.find_element(
                    *self._file_menu_new_window_button_locator).click()
        self.selenium.set_context('content')
        return self._windows.get_new_window_handle(handles_before)
