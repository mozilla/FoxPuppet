# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Panel UI."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.panel_ui.panel_ui import PanelUI, History


@pytest.fixture
def history(browser: BrowserWindow) -> History | None:
    """Create History panel object.

    Args:
        browser: BrowserWindow instance

    Returns:
        :py:class:`History`: FoxPuppet History panel object
    """
    panel_ui = browser.wait_for_panel_ui(PanelUI)
    if panel_ui is not None:
        panel_ui.open_panel_menu()
    return browser.wait_for_panel_ui(History)


def test_url_is_present_in_history(history: History, selenium: WebDriver) -> None:
    """Test that visited URL appears in browser history."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    history.open_history_menu()
    assert history.is_present(url)


def test_clear_recent_history(history: History, selenium: WebDriver) -> None:
    """Test clearing browser history removes visited URLs."""
    url = "https://www.mozilla.org/en-US/?v=a"
    selenium.get(url)
    history.open_history_menu()
    history.clear_history()
    import time

    time.sleep(1)
    history.open_panel_menu()
    history.open_history_menu()
    assert not history.is_present(url)
