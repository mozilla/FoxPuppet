# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.foxpuppet import FoxPuppet

from selenium.webdriver.common.by import By


class BrowserWindow(FoxPuppet):
    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _nav_bar_locator = (By.ID, 'nav-bar')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')

    def __init__(self, selenium, *args, **kwargs):
        super(BrowserWindow, self).__init__(selenium)

    @property
    def is_private(self):
        """Returns True if this is a Private Browsing window."""

        with self.selenium.context('chrome'):
            return self.selenium.execute_script("""
                    Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                    let chromeWindow = arguments[0].ownerDocument.defaultView;
                    return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
                """, self.windows.window_element)

    def open_window(self, private=False):
        with self.selenium.context('chrome'):
            self.selenium.find_element(*self._file_menu_button_locator).click()
            with self.windows.wait_for_new_window():
                if private:
                    self.selenium.find_element(
                        *self._file_menu_private_window_locator).click()
                else:
                    self.selenium.find_element(
                        *self._file_menu_new_window_button_locator).click()
