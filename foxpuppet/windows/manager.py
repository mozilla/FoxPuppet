# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Window Management for FoxPuppet."""


class WindowManager(object):
    """A window manager that controls the creation of window objects.

    Args:
        selenium: (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
            Firefox WebDriver object.
    """

    def __init__(self, selenium):
        """Create WindowManager Object.

        Args:
            selenium:
                (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
                Firefox WebDriver object.
        """
        self.selenium = selenium

    @property
    def windows(self):
        """Return a list of all open windows.

        Returns:
            list: List of FoxPuppet BrowserWindow objects.

        """
        from foxpuppet.windows import BrowserWindow

        return [
            BrowserWindow(self.selenium, handle)
            for handle in self.selenium.window_handles
        ]
