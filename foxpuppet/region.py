# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Region object model for interacting with different parts of Firefox."""


class Region(object):
    """A region object.

    Used as a base class for region objects.

    :param window: Window object this region appears in.
    :param root: element that serves as the root for the region.
    :type window: :py:class:`~.windows.BaseWindow`
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement`
    """

    def __init__(self, window, root):
        """Create a Region object.

        Args:
            window (:py:class:`BaseWindow`): Window object this region appears
                in.
            root
                (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
                WebDriver element object that serves as the root for the
                region.

        """
        self.root = root
        self.selenium = window.selenium
        self.wait = window.wait
        self.window = window
