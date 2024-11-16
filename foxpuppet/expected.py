# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Module contained custom expected waits and conditions."""

from __future__ import absolute_import
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any, TYPE_CHECKING, Optional, Type


class new_browser_window_is_opened(object):
    """An expectation for checking that a new window is found.

    Returns:
        :py:class:`BrowserWindow`: Browser window.

    """

    def __init__(self, selenium: WebDriver, handles: list[str]):
        """Create new_browser_window_is_opened object.

        Args:
            selenium:
                (:py:class:`~selenium.webdriver.remote.webdriver.WebDriver`):
                Firefox WebDriver object.
            handles: (:obj:`list` of str): List of current Firefox window
                handles.
        """
        self.selenium = selenium
        self.handles = handles

    if TYPE_CHECKING:
        from foxpuppet.windows import BrowserWindow  # Import for static typing

    def __call__(self, *args: Any, **kwargs: Any) -> Optional["BrowserWindow"]:
        """Check to see if a new window has opened.

        Returns:
            :py:class:`BrowserWindow`: Opened window.

        """
        handles = list(set(self.selenium.window_handles) - set(self.handles))
        if len(handles) == 1:
            from foxpuppet.windows import BrowserWindow

            return BrowserWindow(self.selenium, handles[0])
        else:
            return None
