# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from browser.window import Window


class FoxPuppet(object):

    def __init__(self, selenium):
        self.selenium = selenium
        self.window = Window(selenium)

    @property
    def selenium(self):
        return self.__selenium

    @selenium.setter
    def selenium(self, selenium):
        self.__selenium = selenium

    def minimize(self):
        self.window._min_window_size()

    def maximize(self):
        self.window._max_window_size()

    def new_window(self, private=False):

        if private:
            self.window._new_private_browsing_window()
        else:
            self.window._new_window()

    def bookmark_page(self):
        self.window._bookmark_page()
