# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


MENU_BUTTON = 'PanelUI-menu-button'


class Navbar(object):

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._locationbar = None

    def open_window(self, private=False):

        if private:
            self.selenium.find_element_by_id(MENU_BUTTON).click()
            self.selenium.find_element_by_css_selector(
                '#privatebrowsing-button').click()

        self.selenium.find_element_by_id(MENU_BUTTON).click()
        self.selenium.find_element_by_css_selector(
            '#new-window-button').click()

    def bookmark_page(self):
        button = self.selenium.find_element_by_css_selector(
            '#bookmarks-menu-button')

        return button
