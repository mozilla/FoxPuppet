# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Module contained custom expected waits and conditions."""

from __future__ import absolute_import


class new_browser_window_is_opened(object):
    """An expectation for checking that a new window is found.

    Returns:
        :py:class:`BrowserWindow`: Browser window.

    """

    def __init__(self, selenium, handles):
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

    def __call__(self, *args, **kwargs):
        """Check to see if a new window has opened.

        Returns:
            :py:class:`BrowserWindow`: Opened window.

        """
        handles = list(set(self.selenium.window_handles) - set(self.handles))
        if len(handles) == 1:
            from foxpuppet.windows import BrowserWindow

            return BrowserWindow(self.selenium, handles[0])
