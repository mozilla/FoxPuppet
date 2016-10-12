# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By


class Tabbar(object):
    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._tabbrowser = None
        self._new_tab_locator = (By.CSS_SELECTOR, '#new-tab-button')

    def open_tab(self):
        self.selenium.set_context('chrome')
        self.selenium.find_element(*self._new_tab_locator).click()
