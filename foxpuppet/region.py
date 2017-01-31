# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class Region(object):
    """A region object.

    Used as a base class for region objects.

    :param window: Window object this region appears in.
    :param root: element that serves as the root for the region.
    :type window: :py:class:`~.windows.BaseWindow`
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement`
    """

    def __init__(self, window, root):
        self.root = root
        self.selenium = window.selenium
        self.wait = window.wait
        self.window = window
