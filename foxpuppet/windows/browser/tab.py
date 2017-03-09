# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class Tab(Region):

    _tabs_locator = (By.TAG_NAME, 'tab')

    @property
    def close_button(self):
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            tab = self.selenium.find_element(*self._tabs_locator)
            return tab.find_anonymous_element_by_attribute(
                'anonid', 'close-button')

    @property
    def switch_to(self):
        self.selenium.switch_to.window(self.selenium.current_window_handle)

    def close(self):
        from foxpuppet.windows.browser.tab_bar import TabBar
        from foxpuppet.windows.browser.window import BrowserWindow

        window = BrowserWindow(
            self.selenium, self.selenium.current_window_handle)

        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            tabbar = TabBar(window, Tab)
            current_tabs = tabbar.tabs
            self.close_button.click()

            # Switch selenium focus back to window
            self.switch_to
            self.wait.until(lambda _: len(tabbar.tabs) != len(current_tabs))
