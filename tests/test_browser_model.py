# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for the browser model API."""

import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet import FoxPuppet


def test_initial_browser_window(foxpuppet: FoxPuppet) -> None:
    """Tests initial state of browser windows."""
    assert len(foxpuppet.window_manager.windows) == 1
    assert foxpuppet.browser is not None
    assert not foxpuppet.browser.is_private


def test_new_private_window(foxpuppet: FoxPuppet) -> None:
    """Tests opening a new private browsing window via menu."""
    new_browser = foxpuppet.browser.open_window(private=True)
    assert new_browser is not foxpuppet.browser
    assert new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_open_new_window(foxpuppet: FoxPuppet) -> None:
    """Tests opening a new window via menu."""
    new_browser = foxpuppet.browser.open_window(private=False)
    assert new_browser is not foxpuppet.browser
    assert not new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_close_window(foxpuppet: FoxPuppet) -> None:
    """Tests closing a window."""
    new_browser = foxpuppet.browser.open_window()
    new_browser.close()
    assert len(foxpuppet.window_manager.windows) == 1


def test_switch_to(foxpuppet: FoxPuppet, selenium: WebDriver) -> None:
    """Test Switch to function."""
    foxpuppet.browser.open_window()
    # Switch to originally window opened by pytest
    foxpuppet.browser.switch_to()
    assert foxpuppet.browser.handle == selenium.current_window_handle


@pytest.mark.firefox_preferences({"privacy.trackingprotection.enabled": True})
def test_tracking_protection_shield(foxpuppet: FoxPuppet, selenium: WebDriver) -> None:
    """Tests if the tracking protection icon displays."""
    browser = foxpuppet.browser
    assert not browser.navbar.is_tracking_shield_displayed
    selenium.get("https://itisatrap.org/firefox/its-a-tracker.html")
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed
    )
