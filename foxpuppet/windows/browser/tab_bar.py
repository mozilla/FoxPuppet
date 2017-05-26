# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


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

        :returns: :py:class:`~foxpuppet.window.browser.tab_bar.Tab`
        :return type: :py.class:`~foxpuppet.window.browser.tab_bar.Tab`
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return [Tab(self, el) for el in
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


class Tab(Region):

    @property
    def tab_bar(self):
        """ Creates a reference to the TabBar object
        :returns: :py:class:`~foxpuppet.window.browser.tab_bar.TabBar`
        :return type: object
        """
        return TabBar(self.window, self.root)

    @property
    def close_button(self):
        """ A reference to the close button element within each tab
        :returns: Webdriver Object
        :return type:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.root.find_anonymous_element_by_attribute(
                'anonid', 'close-button')

    def close(self):
        """
        Closes the selected tab
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            current_tabs = self.tab_bar.tabs
            self.close_button.click()

        self.wait.until(lambda _: len(current_tabs) != len(self.tab_bar.tabs))
