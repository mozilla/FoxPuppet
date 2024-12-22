# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Region object model for interacting with different parts of Firefox."""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from foxpuppet.windows import BaseWindow


class Region(object):
    """A region object.

    Used as a base class for region objects.

    :param window: Window object this region appears in.
    :param root: element that serves as the root for the region.
    :type window: :py:class:`~.windows.BaseWindow`
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement`
    """

    from foxpuppet.windows import BaseWindow

    def __init__(self, window: BaseWindow, root: WebElement):
        """Create a Region object.

        Args:
            window (:py:class:`BaseWindow`): Window object this region appears
                in.
            root
                (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
                WebDriver element object that serves as the root for the
                region.

        """
        self.root: WebElement = root
        self.selenium: WebDriver = window.selenium
        self.wait: WebDriverWait = window.wait
        self.window: BaseWindow = window
        self.actions: ActionChains = ActionChains(self.selenium)
