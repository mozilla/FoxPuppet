# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By


class Navbar(object):

    _file_menu_button_locator = (By.ID, 'file-menu')
    _file_menu_private_window_locator = (By.ID, 'menu_newPrivateWindow')
    _file_menu_new_window_button_locator = (By.ID, 'menu_newNavigator')
    _bookmark_menu_button_locator = (By.ID, 'bookmarks-menu-button')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._locationbar = None

    def open_window(self, private=False):
        self.selenium.set_context('chrome')
        self.selenium.find_element(*self._file_menu_button_locator).click()
        if private:
            self.selenium.find_element(
                *self._file_menu_private_window_locator).click()
        else:
            self.selenium.find_element(
                *self._file_menu_new_window_button_locator).click()

    def bookmark_page(self):
        self.selenium.set_context('chrome')
        self.selenium.find_element(
            *self._bookmark_menu_button_locator).click()
