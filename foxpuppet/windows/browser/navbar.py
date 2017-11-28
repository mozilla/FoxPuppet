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

    _tracking_protection_shield_locator = (By.ID, 'tracking-protection-icon')

    @property
    def extensions(self):
        """List of current extensions installed."""
        return self.Extensions(self, self.root).extensions_list

    @property
    def is_tracking_shield_displayed(self):
        """Tracking Protection shield.

        Returns:
            bool: True or False if the Tracking Shield is displayed.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            el = self.selenium.find_element(
                *self._tracking_protection_shield_locator)
            return bool(el.get_attribute('state'))

    class Extensions(Region):
        """Representation of the extension secrtion of the navbar."""

        _extension_locator = (By.CLASS_NAME, 'webextension-browser-action')

        @property
        def extensions_list(self):
            """List of current extensions installed."""
            with self.selenium.context(self.selenium.CONTEXT_CHROME):
                els = self.selenium.find_elements(*self._extension_locator)
                return [self.Extension(self, el) for el in els]

        class Extension(Region):
            """Representation of a single extension."""

            @property
            def name(self):
                """Extension name."""
                with self.selenium.context(self.selenium.CONTEXT_CHROME):
                    return self.root.get_attribute('label')

            def click(self):
                """Click on the extension."""
                handles = len(self.selenium.window_handles)
                with self.selenium.context(self.selenium.CONTEXT_CHROME):
                    self.root.click()
                # Wait for tab to open
                self.wait.until(
                    lambda _: len(self.selenium.window_handles) != handles)
                # Switch to tab
                self.selenium.switch_to.window(
                    self.selenium.window_handles[-1])
                # Wait for the URL request to process
                self.wait.until(
                    lambda _: self.selenium.current_url != 'about:blank')
