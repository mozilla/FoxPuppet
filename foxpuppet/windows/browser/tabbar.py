# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.windows.browser.tab import Tab


class TabBar(object):

    """Representation of the tab bar which contains the tabs.

    :param selenium: WebDriver Object
    :type selenium:
        :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
    """

    _new_tab_button = (By.ID, 'new-tab-button')
    _tab_browser_locator = (By.ID, 'tabbrowser-tabs')
    _tabs = (By.TAG_NAME, 'tab')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium

    @property
    def tabs(self):
        """Returns a list of tabs.

        :returns: :py:class:`~foxpuppet.window.browser.tab.Tab`
        :return type: object
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            tab = self.selenium.find_elements(*self._tabs)

        return [Tab(self.selenium) for tabs in tab]

    def open_new_tab(self):
        """Opens a new tab in the current window.

        :returns: WebDriver Object
        :return type:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.selenium.find_element(*self._new_tab_button).click()
