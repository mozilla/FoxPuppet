# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from abc import ABCMeta

from foxpuppet.region import Region


class BaseNotification(Region):
    """Abstract base class for any kind of notification."""

    __metaclass__ = ABCMeta

    @staticmethod
    def create(window, root):
        notifications = {}
        _id = root.get_property('id')
        from foxpuppet.windows.browser.notifications import addons
        notifications.update(addons.NOTIFICATIONS)
        return notifications.get(_id, BaseNotification)(window, root)

    @property
    def label(self):
        """Provide access to the notification label.

        :returns: The notification label.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.root.get_attribute('label')

    @property
    def origin(self):
        """Provide access to the notification origin.

        :returns: The notification origin.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.root.get_attribute('origin')

    def close(self):
        """Close the notification."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.root.find_anonymous_element_by_attribute(
                'anonid', 'closebutton').click()
        self.window.wait_for_notification(None)
