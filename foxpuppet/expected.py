# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import


class new_browser_window_is_opened(object):
    """
    An expectation for checking that a new window is found after requesting
    it to be opened

    :returns: A BrowserWindow Object
    """

    def __init__(self, selenium, handles):
        self.selenium = selenium
        self.handles = handles

    def __call__(self, *args, **kwargs):
        handles = list(set(self.selenium.window_handles) - set(self.handles))
        if len(handles) == 1:
            from foxpuppet.windows import BrowserWindow
            return BrowserWindow(self.selenium, handles[0])
