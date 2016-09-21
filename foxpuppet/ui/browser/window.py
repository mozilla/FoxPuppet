# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.foxpuppet import FoxPuppet
from . import Navbar, TabBar
from foxpuppet.ui import Windows, BaseWindow


class BrowserWindow(FoxPuppet):

    def __init__(self, *args, **kwargs):
        BaseWindow.__init__()
        self.selenium = FoxPuppet.selenium

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
        self.selenium.switch_to()

        if not self._tabbar:
            tabbrowser = self.selenium.find_element_by_id('tabbrowser-tabs')
            self._tabbar = TabBar(lambda: self.selenium, self, tabbrowser)

        return self._tabbar

    def close(self):
        self.selenium.switch_to()
        self.selenium.close()

    def min_window_size(self):
        self.selenium.switch_to()
        return self.selenium.find_element_by_id('titlebar-min')

    def max_window_size(self):
        self.selenium.switch_to()
        return self.selenium.find_element_by_id('titlebar-max')

    def new_private_browsing_window(self):
        self.selenium.switch_to()
        return self.selenium.find_element_by_id('privatebrowsing-button')

    def new_window_button(self):
        self.selenium.switch_to()
        return self.selenium.find_element_by_id('new-window-button')
