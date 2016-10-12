# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from .tabbar import Tabbar
from .navbar import Navbar
from foxpuppet.browser.windows import Windows

NAV_BAR = 'nav-bar'
TAB_BROWSER = 'tabbrowser-tabs'
TITLE_BAR_CLOSE = 'titlebar-close'
TITLE_BAR_MIN = 'titlebar-min'
TITLE_BAR_MAX = 'titlebar-max'


class BrowserWindow(object):
    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self.windows = Windows(selenium)
        self.navbar = Navbar(selenium)
        self.tabbar = Tabbar(selenium)

    @property
    def _navbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._navbar:
            navbar = self.selenium.find_element_by_id(NAV_BAR)
            self._navbar = Navbar(self.selenium, navbar)

        return self._navbar

    @property
    def _tabbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._tabbar:
            tabbrowser = self.selenium.find_element_by_id(TAB_BROWSER)
            self._tabbar = Tabbar(self.selenium, tabbrowser)

        return self._tabbar

    def close(self, handle):
        self.selenium.close()

    def minimize(self):
        button = self.selenium.find_element_by_id(TITLE_BAR_MIN)
        button.click()

    def maximize(self):
        self.selenium.maximize()
