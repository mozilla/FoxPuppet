# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Window Management for FoxPuppet."""

from selenium.webdriver.remote.webdriver import WebDriver


class WindowManager(object):
    """A window manager that controls the creation of window objects.

    Args:
        selenium: (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
            Firefox WebDriver object.
    """

    def __init__(self, selenium: WebDriver) -> None:
        """Create WindowManager Object.

        Args:
            selenium:
                (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
                Firefox WebDriver object.
        """
        self.selenium = selenium

    from foxpuppet.windows import BrowserWindow

    @property
    def windows(self) -> list[BrowserWindow]:
        """Return a list of all open windows.

        Returns:
            list: List of FoxPuppet BrowserWindow objects.

        """
        from foxpuppet.windows import BrowserWindow

        return [
            BrowserWindow(self.selenium, handle)
            for handle in self.selenium.window_handles
        ]
