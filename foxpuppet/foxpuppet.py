# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""FoxPuppet object for browser interaction."""

from __future__ import absolute_import

from foxpuppet.windows import WindowManager


class FoxPuppet(object):
    """Set up the interface for interacting with the Firefox browser.

    Args:
        selenium:
            (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
            Firefox WebDriver object.
    """

    def __init__(self, selenium):
        """Create FoxPuppet object.

        Args:
            selenium:
                (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
                Firefox WebDriver object.
        """
        self.selenium = selenium
        self.window_manager = WindowManager(selenium)
        # Need to ensure the first window is a browser window
        self.browser = self.window_manager.windows[0]
