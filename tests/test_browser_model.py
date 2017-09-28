# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for the browser model API."""

from selenium.webdriver.support.wait import WebDriverWait

import pytest


def test_initial_browser_window(foxpuppet):
    """Tests initial state of browser windows."""
    assert len(foxpuppet.window_manager.windows) == 1
    assert foxpuppet.browser is not None
    assert not foxpuppet.browser.is_private


def test_new_private_window(foxpuppet):
    """Tests opening a new private browsing window via menu."""
    new_browser = foxpuppet.browser.open_window(private=True)
    assert new_browser is not foxpuppet.browser
    assert new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_open_new_window(foxpuppet):
    """Tests opening a new window via menu."""
    new_browser = foxpuppet.browser.open_window(private=False)
    assert new_browser is not foxpuppet.browser
    assert not new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_close_window(foxpuppet):
    """Tests closing a window."""
    new_browser = foxpuppet.browser.open_window()
    new_browser.close()
    assert len(foxpuppet.window_manager.windows) == 1


def test_switch_to(foxpuppet, selenium):
    """Test Switch to function."""
    foxpuppet.browser.open_window()
    # Switch to originally window opened by pytest
    foxpuppet.browser.switch_to()
    assert foxpuppet.browser.handle == selenium.current_window_handle


@pytest.mark.firefox_preferences({'privacy.trackingprotection.enabled': True})
def test_tracking_protection_shield(foxpuppet, selenium):
    """Tests if the tracking protection icon displays."""
    browser = foxpuppet.browser
    assert not browser.navbar.is_tracking_shield_displayed
    selenium.get('https://www.washingtonpost.com/')
    WebDriverWait(selenium, timeout=5).until(
        lambda _: browser.navbar.is_tracking_shield_displayed)


def test_open_new_tab(browser, selenium):
    """Test Open new Tab."""
    assert len(browser.tab_bar.tabs) == 1
    browser.tab_bar.open_new_tab()
    assert len(browser.tab_bar.tabs) == 2


def test_close_tab(browser, selenium):
    """Test close Tab."""
    browser.tab_bar.open_new_tab()
    browser.tab_bar.tabs[1].close()
    assert len(browser.tab_bar.tabs) == 1


def test_select_tab(browser, selenium):
    """Test selecting a tab."""
    selenium.get('https://www.mozilla.org/')
    tabs = browser.tab_bar.open_new_tab()
    tabs[-1].select()
    assert 'about:newtab' in selenium.current_url
    tabs[0].select()
    assert 'https://www.mozilla.org/' in selenium.current_url
