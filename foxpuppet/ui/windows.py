# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class Windows(object):

    def __init__(self, foxpuppet):
        self.selenium = foxpuppet.selenium
        self._handle = None

    @property
    def all(self):
        return self.selenium.window_handles

    @property
    def current(self):
        return self.selenium.current_window_handle

    def focus(self, handle):
        return self.selenium.switch_to.window(handle)
