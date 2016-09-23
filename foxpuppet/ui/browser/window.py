# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.foxpuppet import FoxPuppet
from .tabbar import TabBar
from .navbar import Navbar
from foxpuppet.ui.windows import Windows
from foxpuppet.ui.base_window import BaseWindow


class Browser_Window(FoxPuppet):

    def __init__(self, foxpuppet, *args, **kwargs):
        BaseWindow()
        self.windows = Windows(foxpuppet)

        self.selenium = foxpuppet.selenium
        self._navbar = None
        self._tabbar = None

    @property
    def navbar(self):
        self.selenium.switch_to()

        if not self._navbar:
            navbar = self.selenium.find_element_by_id('nav-bar')
            self._navbar = Navbar(lambda: self.selenium, self, navbar)

        return self._navbar

    @property
    def tabbar(self):
        self.selenium.switch_to.window(self.windows.current)

        if not self._tabbar:
            tabbrowser = self.selenium.find_element_by_id('tabbrowser-tabs')
            self._tabbar = TabBar(lambda: self.selenium, self, tabbrowser)

        return self._tabbar

    def close(self, handle):
        self.selenium.switch_to.window(handle)
        self.selenium.find_element_by_id('titlebar-close').click()

    def close_all(self, exceptions=None):

        windows_to_keep = exceptions or []

        for handle in self.windows.all:
            if windows_to_keep == handle:
                continue
            self.selenium.switch_to.window(handle)
            self.close(handle)

    def min_window_size(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.selenium.find_element_by_id('titlebar-min')

        button.click()

    def max_window_size(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.selenium.find_element_by_id('titlebar-max')

        button.click()

    def new_private_browsing_window(self):
        self.selenium.switch_to.window(self.windows.current)
        button = self.selenium.find_element_by_css_selector(
            '#privatebrowsing-button'
        )

        button.click()

    def new_window_button(self):
        self.selenium.switch_to.window(self.windows.current)
        self.selenium.find_element_by_id('PanelUI-menu-button').click()
        button = self.selenium.find_element_by_css_selector(
            '#new-window-button'
        )

        button.click()
