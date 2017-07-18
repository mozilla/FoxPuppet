# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class NavBar(Region):

    """Representation of the Navigation Bar
    :param window: Window object this region appears in.
    :param root: element that serves as the root for the region.
    :type window: :py:class:`~.windows.BaseWindow`
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement`
    """
    _tracking_protection_shield_locator = (By.ID, 'tracking-protection-icon')

    @property
    def is_tracking_shield_displayed(self):
        """Tracking Protection shield
        :returns: True or False if the Tracking Shield is displayed
        :type return: boolean
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            el = self.selenium.find_element(
                *self._tracking_protection_shield_locator)
            return bool(el.get_attribute('state'))
