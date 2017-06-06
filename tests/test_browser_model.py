# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


def test_initial_browser_window(foxpuppet):
    """Tests initial state of browser windows"""
    assert len(foxpuppet.window_manager.windows) == 1
    assert foxpuppet.browser is not None
    assert not foxpuppet.browser.is_private


def test_new_private_window(foxpuppet):
    """Tests opening a new private browsing window via menu"""
    new_browser = foxpuppet.browser.open_window(private=True)
    assert new_browser is not foxpuppet.browser
    assert new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_open_new_window(foxpuppet):
    """Tests opening a new window via menu"""
    new_browser = foxpuppet.browser.open_window(private=False)
    assert new_browser is not foxpuppet.browser
    assert not new_browser.is_private
    assert len(foxpuppet.window_manager.windows) == 2


def test_close_window(foxpuppet):
    """Tests closing a window"""
    new_browser = foxpuppet.browser.open_window()
    new_browser.close()
    assert len(foxpuppet.window_manager.windows) == 1


def test_switch_to(foxpuppet, selenium):
    """Test Switch to function"""
    foxpuppet.browser.open_window()

    # Switch to originally window opened by pytest
    foxpuppet.browser.switch_to()
    assert foxpuppet.browser.handle == selenium.current_window_handle


def test_open_new_tab(foxpuppet, selenium):
    """Test Open new Tab"""
    assert len(foxpuppet.browser.tabbar.tabs) == 1
    foxpuppet.browser.tabbar.open_new_tab()
    assert len(foxpuppet.browser.tabbar.tabs) == 2
