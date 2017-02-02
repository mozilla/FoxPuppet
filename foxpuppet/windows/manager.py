# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class WindowManager(object):

    """
        A window manager that controls the creation of window objects
        for interaction.

        :param selenium: WebDriver object.
        :type selenium:
            :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
    """

    def __init__(self, selenium):
        self.selenium = selenium

    @property
    def windows(self):
        """
        Returns a list of all open windows

        :returns: :py:class:`~foxpuppet.windows.browser.window.BrowserWindow`
            objects.
        :return type: list

        """
        from foxpuppet.windows import BrowserWindow
        return [BrowserWindow(self.selenium, handle)
                for handle in self.selenium.window_handles]
