# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By


class Navbar(object):
    _bookmark_menu_button_locator = (By.ID, 'bookmarks-menu-button')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium

    def bookmark_page(self):
        self.selenium.set_context('chrome')
        self.selenium.find_element(
            *self._bookmark_menu_button_locator).click()
