# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


MENU_BUTTON = 'PanelUI-menu-button'


class TabBar(object):

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium
        self._tabbrowser = None

    def _new_tab(self):

        button = self.selenium.find_element_by_css_selector(
            '#new-tab-button'
        )

        return button
