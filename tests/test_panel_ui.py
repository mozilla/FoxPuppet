# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Panel UI."""

import pytest
import time
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.panel_ui.panel_ui import PanelUI, History


links = [
    "https://www.mozilla.org/en-US/?v=a",
    "https://www.youtube.com",
    "https://www.facebook.com/",
]


@pytest.fixture
def panel_ui(browser: BrowserWindow) -> PanelUI | None:
    """Create Panel UI object.

    Args:
        browser: BrowserWindow instance

    Returns:
        :py:class:`PanelUI`: FoxPuppet Panel UI object
    """
    return browser.wait_for_panel(PanelUI)


@pytest.fixture
def history(panel_ui: PanelUI, browser: BrowserWindow) -> History | None:
    """Create Panel UI object.

    Args:
        browser: BrowserWindow instance

    Returns:
        :py:class:`PanelUI`: FoxPuppet Panel UI object
    """
    panel_ui.open_panel_menu()
    return browser.wait_for_panel(History)


def test_open_new_tab(panel_ui: PanelUI, browser: BrowserWindow) -> None:
    """Test opening a new tab using the Panel UI."""
    panel_ui.open_new_tab()
    assert browser.wait_for_num_windows_or_tabs(2)


def test_open_new_window(panel_ui: PanelUI, browser: BrowserWindow) -> None:
    """Test opening a new window using the Panel UI."""
    panel_ui.open_new_window()
    assert browser.wait_for_num_windows_or_tabs(2)


def test_verify_links_open_in_new_tab_in_url_bar(
    panel_ui: PanelUI, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in new tab are present in the url bar."""
    links = ["https://www.mozilla.org/en-US/?v=a"]
    panel_ui.open_new_tab()
    browser.switch_to_new_window_or_tab()
    for link in links:
        selenium.get(link)
    urls = panel_ui.url_bar(links)
    assert len(urls) == 1


def test_verify_links_open_in_new_tab_in_history(
    panel_ui: PanelUI, history: History, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in new tab are present in browser history."""
    urls = []
    panel_ui.open_new_tab()
    browser.switch_to_new_window_or_tab()
    for link in links:
        selenium.get(link)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    for link in links:
        if history.is_present(link):
            urls.append(link)
    assert len(urls) == 3


def test_verify_links_open_in_new_window_in_history(
    panel_ui: PanelUI, history: History, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in new window are present in browser history."""
    urls = []
    panel_ui.open_new_window()
    browser.switch_to_new_window_or_tab()
    for link in links:
        selenium.get(link)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    for link in links:
        if history.is_present(link):
            urls.append(link)
    assert len(urls) == 3


def test_verify_links_open_in_new_window_in_url_bar(
    panel_ui: PanelUI, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in new window are present in the url bar."""
    links = ["https://www.mozilla.org/en-US/?v=a"]
    panel_ui.open_new_window()
    browser.switch_to_new_window_or_tab()
    time.sleep(1)
    for link in links:
        selenium.get(link)
    url = panel_ui.url_bar(links)
    assert len(url) == 1


def test_url_is_present_in_history(history: History, selenium: WebDriver) -> None:
    """Test that visited URL appears in browser history."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    history.open_history_menu()
    assert history.is_present(url)


def test_clear_recent_history(
    panel_ui: PanelUI, history: History, selenium: WebDriver
) -> None:
    """Test clearing browser history removes visited URLs."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    panel_ui.open_history_menu()
    history.clear_history()
    time.sleep(1)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    assert not history.is_present(url)


def test_verify_private_browsing_links_not_in_history(
    panel_ui: PanelUI, history: History, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in private window are not present in browser history."""
    invalid_links = []
    initial_window_handle = selenium.current_window_handle
    panel_ui.open_private_window()
    browser.switch_to_new_window_or_tab()
    for link in links:
        selenium.get(link)
    selenium.switch_to.window(initial_window_handle)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    for link in links:
        if history.is_present(link):
            invalid_links.append(link)
    assert not invalid_links


def test_verify_private_browsing_links_not_in_url_bar(
    panel_ui: PanelUI, browser: BrowserWindow, selenium: WebDriver
) -> None:
    """Test that links opened in private window are not present in the url bar."""
    initial_window_handle = selenium.current_window_handle
    panel_ui.open_private_window()
    browser.switch_to_new_window_or_tab()

    for link in links:
        selenium.get(link)

    selenium.switch_to.window(initial_window_handle)
    assert not panel_ui.url_bar(links)
