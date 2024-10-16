# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains a base class for interacting with Firefox notifications."""

from abc import ABCMeta

from selenium.webdriver.common.by import By

from foxpuppet.region import Region


class BaseNotification(Region):
    """Abstract base class for any kind of notification."""

    __metaclass__ = ABCMeta

    @staticmethod
    def create(window, root):
        """Create a notification object.

        Args:
            window (:py:class:`BrowserWindow`): Window object this region
                appears in.
            root
                (:py:class:`~selenium.webdriver.remote.webelement.WebElement`):
                WebDriver element object that serves as the root for the
                notification.

        Returns:
            :py:class:`BaseNotification`: Firefox notification.

        """
        notifications = {}
        _id = root.get_property("id")
        from foxpuppet.windows.browser.notifications import addons

        notifications.update(addons.NOTIFICATIONS)
        return notifications.get(_id, BaseNotification)(window, root)

    @property
    def label(self):
        """Provide access to the notification label.

        Returns:
            str: The notification label

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.root.get_attribute("label")

    @property
    def origin(self):
        """Provide access to the notification origin.

        Returns:
            str: The notification origin.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.root.get_attribute("origin")

    def find_primary_button(self):
        """Retrieve the primary button."""
        if self.window.firefox_version >= 67:
            return self.root.find_element(
                By.CLASS_NAME, "popup-notification-primary-button"
            )
        return self.root.find_anonymous_element_by_attribute("anonid", "button")

    def find_secondary_button(self):
        """Retrieve the secondary button."""
        if self.window.firefox_version >= 67:
            return self.root.find_element(
                By.CLASS_NAME, "popup-notification-secondary-button"
            )
        return self.root.find_anonymous_element_by_attribute("anonid", "secondarybutton")

    def find_description(self):
        """Retrieve the notification description."""
        if self.window.firefox_version >= 67:
            return self.root.find_element(By.CLASS_NAME, "popup-notification-description")
        return self.root.find_anonymous_element_by_attribute(
            "class", "popup-notification-description"
        )

    def find_close_button(self):
        """Retrieve the close button."""
        if self.window.firefox_version >= 67:
            return self.root.find_element(By.CLASS_NAME, "popup-notification-closebutton")
        return self.root.find_anonymous_element_by_attribute("anonid", "closebutton")

    def close(self):
        """Close the notification."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.find_close_button().click()
        self.window.wait_for_notification(None)
