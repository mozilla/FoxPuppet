# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Creates Navbar object to interact with Firefox Navigation Bar."""

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class NavBar(Region):
    """Representation of the navigation bar.

    Args:
        window (:py:class:`BaseWindow`): Window object this region appears in.
        root
            (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
            WebDriver element object that serves as the root for the
            region.

    """

    _tracking_protection_shield_locator = (By.ID, "tracking-protection-icon-box")

    @property
    def is_tracking_shield_displayed(self):
        """Tracking Protection shield.

        Returns:
            bool: True or False if the Tracking Shield is displayed.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if self.window.firefox_version >= 63:  # Bug 1471713, 1476218
                el = self.root.find_element(*self._tracking_protection_shield_locator)
                return el.get_attribute("active") is not None
            el = self.root.find_element(By.ID, "tracking-protection-icon")
            return bool(el.get_attribute("state"))
