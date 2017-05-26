# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from foxpuppet.windows.browser.notifications import BaseNotification

from selenium.webdriver.common.by import By


class AddOnInstallBlocked(BaseNotification):
    """Add-on install blocked notification."""

    def allow(self):
        """Allow the add-on to be installed"""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.root.find_anonymous_element_by_attribute(
                'anonid', 'button').click()


class AddOnInstallConfirmation(BaseNotification):
    """Add-on install confirmation notification."""

    _addon_name_locator = (
        By.CSS_SELECTOR, '#addon-install-confirmation-content label')
    _cancel_locator = (By.ID, 'addon-install-confirmation-cancel')
    _confirm_locator = (By.ID, 'addon-install-confirmation-accept')

    @property
    def addon_name(self):
        """Provide access to the add-on name.

        :returns: The add-on name.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if self.window.firefox_version >= 55:
                return self.root.find_anonymous_element_by_attribute(
                    'anonid', 'description').find_element(
                        By.CSS_SELECTOR, '.addon-webext-name').text
            else:
                label = self.root.find_element(*self._addon_name_locator)
                return label.get_property('value')

    def cancel(self):
        """Cancel add-on install."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.root.find_anonymous_element_by_attribute(
                'anonid', 'secondarybutton').click()

    def install(self):
        """Confirm add-on install."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.root.find_anonymous_element_by_attribute(
                'anonid', 'button').click()


class AddOnInstallComplete(BaseNotification):
    """Add-on install complete notification."""


class AddOnInstallRestart(BaseNotification):
    """Add-on install restart notification."""


class AddOnInstallFailed(BaseNotification):
    """Add-on install failed notification."""


class AddOnProgress(BaseNotification):
    """Add-on progress notification."""


NOTIFICATIONS = {
    'addon-install-blocked-notification': AddOnInstallBlocked,
    'addon-install-confirmation-notification': AddOnInstallConfirmation,
    'addon-install-complete-notification': AddOnInstallComplete,
    'addon-install-restart-notification': AddOnInstallRestart,
    'addon-install-failed-notification': AddOnInstallFailed,
    'addon-installed-notification': AddOnInstallComplete,
    'addon-progress-notification': AddOnProgress,
    'addon-webext-permissions-notification': AddOnInstallConfirmation,
}
