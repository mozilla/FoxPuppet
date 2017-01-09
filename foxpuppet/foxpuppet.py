# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from .decorators import use_class_as_property


class FoxPuppet(object):

    def __init__(self, selenium):
        self._selenium = selenium

    @property
    def selenium(self):
        return self._selenium

    @use_class_as_property('api.windows.Windows')
    def windows(self):
        pass

    @use_class_as_property('api.browser.window.BrowserWindow')
    def browser(self):
        pass
