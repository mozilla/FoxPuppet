# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.expected import new_browser_window_is_opened
from foxpuppet.windows import BaseWindow


class BrowserWindow(BaseWindow):

    """Representation of a browser window.

        :extends: BaseWindow
    """

    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _nav_bar_locator = (By.ID, 'nav-bar')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')

    @property
    def is_private(self):
        """:returns: True if this is a Private Browsing window.
        """

        self.switch_to()
        with self.selenium.context('chrome'):
            return self.selenium.execute_script(
                """
                Components.utils.import("resource://gre/modules/PrivateBrowsingUtils.jsm");

                let chromeWindow = arguments[0].ownerDocument.defaultView;
                return PrivateBrowsingUtils.isWindowPrivate(chromeWindow);
                """, self.document_element)

    def open_window(self, private=False):
        """Opens a new browser window

        :param private: Optional parameter to open a private browsing window.
                        Defaults to False.

        :returns: A BrowserWindow object of the opened window.
        """

        handles_before = self.selenium.window_handles
        self.switch_to()

        with self.selenium.context('chrome'):
            # Opens private or non-private window
            self.selenium.find_element(*self._file_menu_button_locator).click()
            if private:
                self.selenium.find_element(
                    *self._file_menu_private_window_locator).click()
            else:
                self.selenium.find_element(
                    *self._file_menu_new_window_button_locator).click()

        return self.wait.until(
            new_browser_window_is_opened(self.selenium, handles_before),
            message="No new browser window opened")
