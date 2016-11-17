# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from .api.browser.window import BrowserWindow
from .api.windows import Windows


class FoxPuppet(object):

    def __init__(self, selenium):
        self.selenium = selenium
        self.browser = BrowserWindow(selenium)
        self.windows = Windows(selenium)
