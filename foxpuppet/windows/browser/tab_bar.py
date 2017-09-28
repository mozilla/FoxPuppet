# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/
"""Creates tab_bar object to interact with the Firefox tabs and tabbar."""

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class Tab_bar(Region):
    """Representation of the tab bar which contains the tabs.

    Args:
        window (:py:class:`BaseWindow`): Window object this region appears in.
        root
            (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
            WebDriver element object that serves as the root for the
            region.

    """

    _new_tab_button_locator = (By.ID, 'new-tab-button')
    _tabs_locator = (By.TAG_NAME, 'tab')

    @property
    def tabs(self):
        """Return a list of tabs.

        Returns: :py:class:`~foxpuppet.window.browser.tab_bar.Tab`

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            tabs = [self.Tab(self, el) for el in
                    self.selenium.find_elements(*self._tabs_locator)]
        # Assign handles
        for tab, handle in zip(tabs, self.selenium.window_handles):
            tab.handle = handle
        return tabs

    def open_new_tab(self):
        """Open a new tab in the current window.

        Returns: list of :py:class:`Tab`.

        """
        current_tabs = len(self.selenium.window_handles)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*self._new_tab_button_locator).click()
        self.wait.until(
            lambda _: len(self.selenium.window_handles) != current_tabs)
        return self.tabs

    class Tab(Region):
        """Representaion of the Tab.

        Args:
            window (:py:class:`BaseWindow`): Window object this region appears
                    in.
            root
                (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
                WebDriver element object that serves as the root for the
                region.

        """

        def close(self):
            """Close the selected tab."""
            current_tabs = len(self.selenium.window_handles)
            with self.selenium.context(self.selenium.CONTEXT_CHROME):
                button = self.root.find_anonymous_element_by_attribute(
                    'anonid', 'close-button')
                button.click()
            self.wait.until(
                lambda _: len(self.selenium.window_handles) != current_tabs)

        def select(self):
            """Select the tab.

            Returns: :py:class:`Tab`.

            """
            self.selenium.switch_to.window(self.handle)
            return self

        @property
        def handle(self):
            """Return the handle of the tab.

            Returns: Selenium Firefox window handle.

            """
            return self._handle

        @handle.setter
        def handle(self, value):
            """Handle setter."""
            self._handle = value
