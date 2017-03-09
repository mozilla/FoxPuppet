# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.region import Region
from foxpuppet.windows.browser.tab import Tab


class TabBar(Region):

    """Representation of the tab bar which contains the tabs.

    :param selenium: WebDriver Object
    :type selenium:
        :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
    """

    _new_tab_button_locator = (By.ID, 'new-tab-button')
    _tabs_locator = (By.TAG_NAME, 'tab')

    @property
    def tabs(self):
        """Returns a list of tabs.

        :returns: :py:class:`~foxpuppet.window.browser.tab.Tab`
        :return type: :py.class:`~foxpuppet.window.browser.tab.Tab`
        """
        from foxpuppet.windows.browser.window import BrowserWindow
        window = BrowserWindow(
            self.selenium, self.selenium.current_window_handle)

        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.switch_to
            return [Tab(window, Tab) for tabs in
                    self.selenium.find_elements(*self._tabs_locator)]

    @property
    def switch_to(self):
        self.selenium.switch_to.window(self.selenium.current_window_handle)

    def open_new_tab(self):
        """Opens a new tab in the current window.

        :returns: WebDriver Object
        :return type:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            current_tabs = self.tabs
            self.selenium.find_element(*self._new_tab_button_locator).click()
            self.wait.until(lambda _: len(self.tabs) != len(current_tabs))
