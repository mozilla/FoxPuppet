# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


MENU_BUTTON = 'PanelUI-menu-button'


class Navbar(object):

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._locationbar = None

    def _open_window(self, private=False):

        if private:
            menu = self.selenium.find_element_by_id(MENU_BUTTON)
            menu.click()
            button = self.selenium.find_element_by_css_selector(
                '#privatebrowsing-button'

            )

        menu = self.selenium.find_element_by_id(MENU_BUTTON)
        menu.click()
        button = self.selenium.find_element_by_css_selector(
            '#new-window-button'
        )

        return button

    def _bookmark_page(self):
        button = self.selenium.find_element_by_css_selector(
            '#bookmarks-menu-button')

        return button
