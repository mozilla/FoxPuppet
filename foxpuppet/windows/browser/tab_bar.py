# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/
"""Creates tab_bar object to interact with the Firefox tabs and tabbar."""

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class TabBar(Region):
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

    @property
    def selected_index(self):
        """The index of the currently selected tab.

        :return: Index of the selected tab.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            tab_bar = self.selenium.find_element(By.ID, 'tabbrowser-tabs')
            return int(tab_bar.get_property('selectedIndex'))

    @property
    def selected_tab(self):
        """A :class:`Tab` instance of the currently selected tab.

        :returns: :class:`Tab` instance.
        """
        return self.tabs[self.selected_index]

    def open_new_tab(self):
        """Open a new tab in the current window.

        Returns: list of :py:class:`Tab`.

        """
        starting_tabs = self.selenium.window_handles
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*self._new_tab_button_locator).click()
        # Wait for tab to open
        self.wait.until(
            lambda s: len(s.window_handles) == len(starting_tabs) + 1)

        current_tabs = self.selenium.window_handles
        [new_handle] = list(set(current_tabs) - set(starting_tabs))
        [new_tab] = [tab for tab in self.tabs if tab.handle == new_handle]

        # if the new tab is the currently selected tab, switch to it
        if new_tab == self.selected_tab:
            new_tab.focus()

        return new_tab

    @staticmethod
    def get_handle_for_tab(selenium, tab):
        """Retrieves the marionette handle for the given :class:`Tab` instance.

        :param marionette: An instance of the Marionette client.

        :param tab_element: The DOM element corresponding to a tab inside the tabs toolbar.

        :returns: `handle` of the tab.
        """

        handle = selenium.execute_script("""
          let win = arguments[0].linkedBrowser;
          if (!win) {
            return null;
          }
          return win.outerWindowID.toString();
        """, tab)

        return handle

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
            tab_closed = self.handle
            with self.selenium.context(self.selenium.CONTEXT_CHROME):
                button = self.root.find_anonymous_element_by_attribute(
                    'anonid', 'close-button')
                button.click()
            self.wait.until(
                lambda s: tab_closed not in s.window_handles,
                message='No new tab has been opened.')
            # Switch to last available tab
            self.selenium.switch_to.window(self.selenium.window_handles[-1])

        @property
        def selected(self):
            """Checks if the tab is selected.

            :return: `True` if the tab is selected.
            """
            with self.selenium.context(self.selenium.CONTEXT_CHROME):
                return self.selenium.execute_script("""
                    return arguments[0].hasAttribute('selected');
                """, self.root)

        def focus(self):
            """Focus the tab.

            Returns: :py:class:`Tab`.

            """
            with self.selenium.context(self.selenium.CONTEXT_CHROME):
                self.root.click()
            self.wait.until(
                lambda _: self.selected,
                message='Tab with handle "%s" could not be selected.' % self.handle)
            self.selenium.switch_to.window(self.handle)

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
