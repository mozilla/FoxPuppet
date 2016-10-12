# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class Tabbar(object):

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._tabbrowser = None

    def open_tab(self):
        self.selenium.find_element_by_css_selector('#new-tab-button').click()
