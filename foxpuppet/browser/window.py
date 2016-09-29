# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from .tabbar import TabBar
from .navbar import Navbar
from foxpuppet.browser.windows import Windows

NAV_BAR = 'nav-bar'
TAB_BROWSER = 'tabbrowser-tabs'
TITLE_BAR_CLOSE = 'titlebar-close'
TITLE_BAR_MIN = 'titlebar-min'
TITLE_BAR_MAX = 'titlebar-max'


class Window(object):

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self.windows = Windows(selenium)
        self._navbar = None
        self._tabbar = None

    @property
    def navbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._navbar:
            navbar = self.selenium.find_element_by_id(NAV_BAR)
            self._navbar = Navbar(self.selenium, navbar)

        return self._navbar

    @property
    def tabbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._tabbar:
            tabbrowser = self.selenium.find_element_by_id(TAB_BROWSER)
            self._tabbar = TabBar(lambda: self.selenium, self, tabbrowser)

        return self._tabbar

    def close(self, handle):
        self.selenium.switch_to.window(handle)
        self.selenium.find_element_by_id(TITLE_BAR_CLOSE).click()

    def close_all(self, exceptions=None):

        windows_to_keep = exceptions or []

        for handle in self.windows.all:
            if windows_to_keep == handle:
                continue
            self.selenium.switch_to.window(handle)
            self.close(handle)

    def _min_window_size(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.selenium.find_element_by_id(TITLE_BAR_MIN)

        button.click()

    def _max_window_size(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.selenium.find_element_by_id(TITLE_BAR_MAX)

        button.click()

    def _new_private_browsing_window(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.navbar._open_window(private=True)

        button.click()

    def _new_window(self):

        """ Opens a Non-Private widow """
        self.selenium.switch_to.window(self.windows.current)
        button = self.navbar._open_window(private=False)

        button.click()

    def _bookmark_page(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.navbar._bookmark_page()

        button.click()
