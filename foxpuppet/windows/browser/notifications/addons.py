# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains all current install notifications Firefox will display."""

from selenium.webdriver.common.by import By

from foxpuppet.windows.browser.notifications import BaseNotification


class AddOnInstallBlocked(BaseNotification):
    """Add-on install blocked notification."""

    def allow(self):
        """Allow the add-on to be installed."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.find_primary_button().click()


class AddOnInstallConfirmation(BaseNotification):
    """Add-on install confirmation notification."""

    @property
    def addon_name(self):
        """Provide access to the add-on name.

        Returns:
            str: Add-on name.

        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            el = self.find_description()
            return el.find_element(By.CSS_SELECTOR, "b").text

    def cancel(self):
        """Cancel add-on install."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.find_secondary_button().click()

    def install(self):
        """Confirm add-on install."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.find_primary_button().click()


class AddOnInstallComplete(BaseNotification):
    """Add-on install complete notification."""

    def close(self):
        """Close the notification."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if self.window.firefox_version > 63:
                self.find_primary_button().click()
                self.window.wait_for_notification(None)
            else:
                BaseNotification.close(self)


class AddOnInstallRestart(BaseNotification):
    """Add-on install restart notification."""


class AddOnInstallFailed(BaseNotification):
    """Add-on install failed notification."""


class AddOnProgress(BaseNotification):
    """Add-on progress notification."""


# Clean up of these notifications will happen once Firefox ESR is past version 63
# https://github.com/mozilla/FoxPuppet/issues/212
NOTIFICATIONS = {
    "addon-install-blocked-notification": AddOnInstallBlocked,
    "addon-install-confirmation-notification": AddOnInstallConfirmation,
    "addon-install-complete-notification": AddOnInstallComplete,
    "appMenu-addon-installed-notification": AddOnInstallComplete,
    "addon-install-restart-notification": AddOnInstallRestart,
    "addon-install-failed-notification": AddOnInstallFailed,
    "addon-installed-notification": AddOnInstallComplete,
    "addon-progress-notification": AddOnProgress,
    "addon-webext-permissions-notification": AddOnInstallConfirmation,
}
