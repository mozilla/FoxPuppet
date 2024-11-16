# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Configuration files for pytest."""

import os

import pytest
from _pytest.nodes import Item

from foxpuppet import FoxPuppet
from foxpuppet.windows import BrowserWindow
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Any, Generator
from tests.webserver import WebServer


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item: Item, call) -> Generator[None, Any, None]:
    """Add a report to the generated html report."""
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    driver = getattr(item, "_driver", None)
    xfail = hasattr(report, "wasxfail")
    failure = (report.skipped and xfail) or (report.failed and not xfail)
    if driver is not None and failure:
        with driver.context(driver.CONTEXT_CHROME):
            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, "Screenshot (chrome)"))
        report.extra = extra


@pytest.fixture(scope="session")
def webserver() -> Generator[WebServer, None, None]:
    """Fixture that starts a local web server."""
    from .webserver import WebServer

    webserver = WebServer(host="127.0.0.1", port=WebServer.get_free_port())
    webserver.start()
    yield webserver
    webserver.stop()


@pytest.fixture
def browser(foxpuppet: FoxPuppet) -> BrowserWindow:
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def firefox_options(firefox_options: FirefoxOptions) -> FirefoxOptions:
    """Fixture for configuring Firefox."""
    firefox_options.log.level = "trace"  # type: ignore
    # firefox_options.set_preference('devtools.chrome.enabled', True)
    # firefox_options.set_preference('devtools.debugger.remote-enabled', True)
    return firefox_options


@pytest.fixture
def foxpuppet(selenium) -> FoxPuppet:
    """Initialize the FoxPuppet object."""
    return FoxPuppet(selenium)
