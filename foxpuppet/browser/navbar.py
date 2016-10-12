# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Navbar(object):
    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._locationbar = None
        self._menu_button = (By.ID, 'PanelUI-menu-button')

    def open_window(self, private=False):
        self.selenium.set_context('chrome')
        if private:
            self.selenium.find_element(*self._menu_button).click()

            element = WebDriverWait(self.selenium, 5).until(
                EC.visibility_of(self.selenium.find_element(
                    By.CSS_SELECTOR, '#privatebrowsing-button')))
            element.click()

        self.selenium.find_element(*self._menu_button).click()
        element = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of(self.selenium.find_element(
                By.CSS_SELECTOR, '#new-window-button')))
        element.click()

    def bookmark_page(self):
        self.selenium.set_context('chrome')
        self.selenium.find_element(
            By.CSS_SELECTOR, '#bookmarks-menu-button').click()
