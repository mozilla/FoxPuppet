# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for the notifications API."""

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Any

from foxpuppet.windows.browser.notifications import BaseNotification
from foxpuppet.windows.browser.notifications.addons import (
    AddOnInstallBlocked,
    AddOnInstallComplete,
    AddOnInstallConfirmation,
    AddOnInstallFailed,
    AddOnProgress,
)
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet.windows import BrowserWindow
from tests.webserver import WebServer
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def firefox_options(request, firefox_options: FirefoxOptions) -> FirefoxOptions:
    """Fixture for configuring Firefox."""
    # Due to https://bugzilla.mozilla.org/show_bug.cgi?id=1329939 we need the
    # initial browser window to be in the foreground. Without this, the
    # notifications will not be displayed.
    firefox_options.add_argument("-foreground")
    if getattr(request, "param", {}).get("page_load_strategy_none", False):
        firefox_options.set_capability("pageLoadStrategy", "none")
    return firefox_options


class AddOn:
    """Class representing an add-on."""

    def __init__(self, name: str, path_key: str = "default"):
        self.name = name
        self._paths = {
            "default": "webextension.xpi",
            "corrupt": "corruptwebextension.xpi",
            "large": "largewebextension.xpi",
        }
        if path_key not in self._paths:
            raise ValueError(f"Invalid path key: {path_key}")
        self._path_key = path_key

    @property
    def path(self):
        """Returns the current path based on the selected key."""
        return self._paths.get(self._path_key)

    @path.setter
    def path(self, ext_path):
        """Sets the current path key if it exists in paths."""
        if ext_path in self._paths:
            self._path_key = ext_path
        else:
            raise ValueError(f"Invalid path key: {ext_path}")


@pytest.fixture
def addon() -> AddOn:
    """Fixture for creating an installable add-on."""
    return AddOn(name="WebExtension")


@pytest.fixture
def progress_notification(
    addon: AddOn, browser: BrowserWindow, webserver: WebServer, selenium: WebDriver
) -> AddOnProgress | None:
    """Fixture that triggers the download progress notification.

    Returns:
        :py:class:AddOnProgress: Firefox notification.
    """
    addon.path = "large"
    selenium.get(webserver.url)
    element = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, addon.path))
    )
    element.click()
    return browser.wait_for_notification(AddOnProgress)


@pytest.fixture
def blocked_notification(
    addon: AddOn, browser: BrowserWindow, webserver: WebServer, selenium: WebDriver
) -> AddOnInstallBlocked | None:
    """Fixture causing a blocked notification to appear in Firefox.

    Returns:
        :py:class:`AddOnInstallBlocked`: Firefox notification.

    """
    selenium.get(webserver.url)
    selenium.find_element(By.LINK_TEXT, addon.path).click()
    return browser.wait_for_notification(AddOnInstallBlocked)


@pytest.fixture
def confirmation_notification(
    browser: BrowserWindow, blocked_notification: AddOnInstallBlocked
) -> AddOnInstallConfirmation | None:
    """Fixture that allows an add-on to be installed.

    Returns:
        :py:class:`AddOnInstallConfirmation`: Firefox notification.

    """
    blocked_notification.allow()
    return browser.wait_for_notification(AddOnInstallConfirmation)


@pytest.fixture
def complete_notification(
    browser: BrowserWindow, confirmation_notification: AddOnInstallConfirmation
) -> AddOnInstallComplete | None:
    """Fixture that installs an add-on.

    Returns:
        :py:class:`AddOnInstallComplete` Firefox notification.

    """
    confirmation_notification.install()
    return browser.wait_for_notification(AddOnInstallComplete)


@pytest.fixture
def failed_notification(
    addon: AddOn, browser: BrowserWindow, webserver: WebServer, selenium: WebDriver
) -> AddOnInstallFailed | None:
    """Fixture that triggers a failed installation notification.

    Returns:
        :py:class:`AddOnInstallFailed`: Firefox notification.
    """
    addon.path = "corrupt"
    selenium.get(webserver.url)
    selenium.find_element(By.LINK_TEXT, addon.path).click()
    return browser.wait_for_notification(AddOnInstallFailed)


def test_add_on_path(addon: AddOn) -> None:
    with pytest.raises(ValueError, match="Invalid path key: doesNotExist"):
        addon.path = "doesNotExist"


def test_open_close_notification(
    browser: BrowserWindow, blocked_notification: AddOnInstallBlocked
) -> None:
    """Trigger and dismiss a notification."""
    assert blocked_notification is not None
    blocked_notification.close()
    return browser.wait_for_notification(None)


@pytest.mark.parametrize(
    "_class, message",
    [
        (BaseNotification, "No notification was shown"),
        (AddOnInstallBlocked, "AddOnInstallBlocked was not shown"),
    ],
)
def test_wait_for_notification_timeout(
    browser: BrowserWindow, _class: Any, message: str
) -> None:
    """Wait for a notification when one is not shown."""
    with pytest.raises(TimeoutException) as excinfo:
        browser.wait_for_notification(_class)
    assert message in str(excinfo.value)


def test_wait_for_no_notification_timeout(
    browser: BrowserWindow, blocked_notification: AddOnInstallBlocked
) -> None:
    """Wait for no notification when one is shown."""
    with pytest.raises(TimeoutException) as excinfo:
        browser.wait_for_notification(None)
    assert "Unexpected notification shown" in str(excinfo.value)


def test_notification_with_origin(
    browser: BrowserWindow,
    webserver: WebServer,
    blocked_notification: AddOnInstallBlocked,
) -> None:
    """Trigger a notification with an origin."""
    assert (
        blocked_notification.origin is not None
    ), "Notification origin should not be None"
    assert f"{webserver.host}" in blocked_notification.origin
    assert blocked_notification.label is not None


def test_allow_blocked_addon(
    browser: BrowserWindow, blocked_notification: AddOnInstallBlocked
) -> None:
    """Allow a blocked add-on installation."""
    blocked_notification.allow()
    browser.wait_for_notification(AddOnInstallConfirmation)


def test_cancel_addon_install(
    browser: BrowserWindow, confirmation_notification: AddOnInstallConfirmation
) -> None:
    """Cancel add-on installation."""
    confirmation_notification.cancel()
    browser.wait_for_notification(None)


def test_confirm_addon_install(
    addon: AddOn,
    browser: BrowserWindow,
    confirmation_notification: AddOnInstallConfirmation,
) -> None:
    """Confirm add-on installation."""
    assert confirmation_notification.addon_name == addon.name
    confirmation_notification.install()
    browser.wait_for_notification(AddOnInstallComplete)


def test_addon_install_complete(
    addon: AddOn, browser: BrowserWindow, complete_notification: AddOnInstallComplete
) -> None:
    """Complete add-on installation and close notification."""
    complete_notification.close()
    browser.wait_for_notification(None)


def test_failed_installation_notification(
    failed_notification: AddOnInstallFailed,
) -> None:
    """Test that a failed installation notification is shown for a corrupt add-on."""
    error_text = "The add-on downloaded from this site could not be installed because it appears to be corrupt."
    assert failed_notification.error_message == error_text


def test_close_failed_notification(
    browser: BrowserWindow, failed_notification: AddOnInstallFailed
) -> None:
    """Close Failed Notification"""
    failed_notification.close()
    browser.wait_for_notification(None)


@pytest.mark.parametrize(
    "firefox_options", [{"page_load_strategy_none": True}], indirect=True
)
def test_progress_notification_downloading(
    browser: BrowserWindow, progress_notification: AddOnProgress
) -> None:
    """Verify downloading status is reported correctly."""
    description = progress_notification.is_downloading
    assert description is True
