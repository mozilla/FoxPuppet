# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import

from foxpuppet.windows import WindowManager


class FoxPuppet(object):
    """
        Class that sets up the interface for interacting with the Firefox
        browser.

        :param selenium: WebDriver object
        :type selenium:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
    """

    def __init__(self, selenium):
        self.selenium = selenium
        self.window_manager = WindowManager(selenium)
        # Need to ensure the first window is a browser window
        self.browser = self.window_manager.windows[0]
