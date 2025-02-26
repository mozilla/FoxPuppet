# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Panel UI."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.panel_ui.panel_ui import PanelUI, History


@pytest.fixture
def links() -> list:
    links = [
        "https://www.mozilla.org/en-US/?v=a",
        "https://www.youtube.com",
        "https://www.facebook.com/",
    ]
    return links


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
def browser_history(panel_ui: PanelUI, browser: BrowserWindow) -> History | None:
    """Create Panel UI object.

    Args:
        browser: BrowserWindow instance

    Returns:
        :py:class:`PanelUI`: FoxPuppet Panel UI object
    """
    panel_ui.open_panel_menu()
    return browser.wait_for_panel(History)


def test_open_new_tab(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test opening a new tab using the Panel UI."""
    panel_ui.open_new_tab()
    assert len(selenium.window_handles) == 2


def test_open_new_window(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test opening a new window using the Panel UI."""
    panel_ui.open_new_window()
    assert len(selenium.window_handles) == 2


def test_open_new_private_window(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test opening a new window using the Panel UI."""
    panel_ui.open_private_window()
    assert len(selenium.window_handles) == 2


def test_url_is_present_in_history(browser_history: History, selenium: WebDriver) -> None:
    """Test that visited URL appears in browser history."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    browser_history.open_history_menu()
    history_items = browser_history.history_items()
    with selenium.context(selenium.CONTEXT_CHROME):
        is_present = any(
            (image_attr := item.get_attribute("image")) and url in image_attr
            for item in history_items
        )
        assert is_present


def test_verify_url_bar_suggestions(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test that a link appears in url bar suggestions."""
    test_url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(test_url)
    all_suggestions = panel_ui.url_bar.suggestions(test_url)
    matching_suggestions = [
        suggestion
        for suggestion in all_suggestions
        if suggestion in test_url and len(suggestion) != 0
    ]
    assert len(matching_suggestions) == 1


def test_verify_links_open_in_new_tab_from_history(
    panel_ui: PanelUI, browser_history: History, selenium: WebDriver, links: list
) -> None:
    """Test that links opened in new tab are present in browser history."""
    panel_ui.open_new_tab()
    for link in links:
        selenium.get(link)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    history_items = browser_history.history_items()
    with selenium.context(selenium.CONTEXT_CHROME):
        found_urls = [
            link
            for link in links
            if any(
                image_attr is not None and link in image_attr
                for item in history_items
                if (image_attr := item.get_attribute("image"))
            )
        ]
        assert len(found_urls) == 3


def test_verify_links_open_in_new_window_from_history(
    panel_ui: PanelUI, browser_history: History, selenium: WebDriver, links: list
) -> None:
    """Test that links opened in new window are present in browser history."""
    panel_ui.open_new_window()
    for link in links:
        selenium.get(link)
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    history_items = browser_history.history_items()
    with selenium.context(selenium.CONTEXT_CHROME):
        found_urls = [
            link
            for link in links
            if any(
                image_attr is not None and link in image_attr
                for item in history_items
                if (image_attr := item.get_attribute("image"))
            )
        ]
        assert len(found_urls) == 3


def test_clear_recent_history(
    panel_ui: PanelUI, browser_history: History, selenium: WebDriver
) -> None:
    """Test clearing browser history removes visited URLs."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    panel_ui.open_history_menu()
    browser_history.clear_history()
    panel_ui.open_panel_menu()
    panel_ui.open_history_menu()
    history_items = browser_history.history_items()
    with selenium.context(selenium.CONTEXT_CHROME):
        is_present = any(
            (image_attr := item.get_attribute("image")) and url in image_attr
            for item in history_items
        )
        assert not is_present
