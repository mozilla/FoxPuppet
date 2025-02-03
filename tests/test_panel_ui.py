# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Panel UI."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.panel_ui.panel_ui import PanelUI


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
    return browser.wait_for_panel_ui(PanelUI)


def test_open_new_tab(panel_ui: PanelUI) -> None:
    """Test opening a new tab using the Panel UI."""
    panel_ui.open_new_tab()
    assert panel_ui.wait_for_num_windows_or_tabs(2)


def test_open_new_window(panel_ui: PanelUI) -> None:
    """Test opening a new window using the Panel UI."""
    panel_ui.open_new_window()
    assert panel_ui.wait_for_num_windows_or_tabs(2)


def test_verify_links_open_in_new_tab_in_awesome_bar(panel_ui: PanelUI) -> None:
    """Test that links opened in new tab are present in the awesome bar."""
    link = ["https://www.mozilla.org/en-US/?v=a"]
    urls = panel_ui.verify_links_in_awesome_bar(link)
    assert len(urls) == 1


def test_verify_links_open_in_new_tab_in_history(panel_ui: PanelUI) -> None:
    """Test that links opened in new tab are present in browser history."""
    urls = panel_ui.verify_links_in_history(links)
    assert len(urls) == 3


def test_verify_links_open_in_new_window_in_history(panel_ui: PanelUI) -> None:
    """Test that links opened in new window are present in browser history."""
    urls = panel_ui.verify_links_in_history(links, new_window=True)
    assert len(urls) == 3


def test_verify_links_open_in_new_window_in_awesome_bar(panel_ui: PanelUI) -> None:
    """Test that links opened in new window are present in the awesome bar."""
    link = ["https://www.mozilla.org/en-US/?v=a"]
    urls = panel_ui.verify_links_in_awesome_bar(link, new_window=True)
    assert len(urls) == 1


def test_url_is_present_in_history(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test that visited URL appears in browser history."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    panel_ui.open_history_menu()
    assert panel_ui.is_present(url)


def test_clear_recent_history(panel_ui: PanelUI, selenium: WebDriver) -> None:
    """Test clearing browser history removes visited URLs."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    panel_ui.open_history_menu()
    panel_ui.clear_history()
    import time

    time.sleep(1)
    panel_ui.open_history_menu()
    assert not panel_ui.is_present(url)


def test_verify_private_browsing_links_not_in_history(panel_ui: PanelUI) -> None:
    """Test that links opened in private window are not present in browser history."""
    invalid_links = panel_ui.verify_private_browsing_links_not_in_history(links)
    assert not invalid_links


def test_verify_private_browsing_links_not_in_awesome_bar(panel_ui: PanelUI) -> None:
    """Test that links opened in private window are not present in the awesome bar."""
    invalid_links = panel_ui.verify_private_browsing_links_not_in_awesome_bar(links)
    assert not invalid_links
