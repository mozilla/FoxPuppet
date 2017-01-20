# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class WindowManager(object):

    """
        A window manager that controls the creation of window objects
        for interaction.

        :param selenium: A selenium object.
    """

    def __init__(self, selenium):
        self.selenium = selenium

    @property
    def windows(self):
        """
        Sets all current windows to appropriate window instances.

        :returns: A list of Window Instances

        """
        from foxpuppet.windows import BrowserWindow
        return [BrowserWindow(self.selenium, handle)
                for handle in self.selenium.window_handles]
