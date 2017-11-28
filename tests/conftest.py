# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Configuration files for pytest."""

import pytest
from foxpuppet import FoxPuppet
from foxpuppet.windows.browser.notifications.addons import (  # noqa: I001
    AddOnInstallBlocked,  # noqa: I001
    AddOnInstallComplete,  # noqa: I001
    AddOnInstallConfirmation)  # noqa: I001


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """Add a report to the generated html report."""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    driver = getattr(item, '_driver', None)
    xfail = hasattr(report, 'wasxfail')
    failure = (report.skipped and xfail) or (report.failed and not xfail)
    if driver is not None and failure:
        with driver.context(driver.CONTEXT_CHROME):
            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(
                screenshot, 'Screenshot (chrome)'))
        report.extra = extra


@pytest.fixture(scope='session')
def webserver():
    """Fixture that starts a local web server."""
    from .webserver import WebServer
    webserver = WebServer()
    webserver.start()
    yield webserver
    webserver.stop()


@pytest.fixture
def browser(foxpuppet):
    """First Firefox browser window opened."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    """Initialize the FoxPuppet object."""
    return FoxPuppet(selenium)


@pytest.fixture
def firefox_options(firefox_options):
    """Fixture for configuring Firefox."""
    # Due to https://bugzilla.mozilla.org/show_bug.cgi?id=1329939 we need the
    # initial browser window to be in the foreground. Without this, the
    # notifications will not be displayed.
    firefox_options.add_argument('-foreground')
    return firefox_options


@pytest.fixture
def addon():
    """Fixture for creating an installable add-on.

    Returns:
        :py:class:`AddOn`: Add-on object containing a name and a path to the
            add-on.

    """
    class AddOn(object):
        name = 'WebExtension'
        path = 'webextension.xpi'
    return AddOn()


@pytest.fixture
def blocked_notification(addon, browser, webserver, selenium):
    """Fixture causing a blocked notification to appear in Firefox.

    Returns:
        :py:class:`AddOnInstallBlocked`: Firefox notification.

    """
    selenium.get(webserver.url())
    selenium.find_element_by_link_text(addon.path).click()
    return browser.wait_for_notification(AddOnInstallBlocked)


@pytest.fixture
def confirmation_notification(browser, blocked_notification):
    """Fixture that allows an add-on to be installed.

    Returns:
        :py:class:`AddOnInstallConfirmation`: Firefox notification.

    """
    blocked_notification.allow()
    return browser.wait_for_notification(AddOnInstallConfirmation)


@pytest.fixture
def complete_notification(browser, confirmation_notification):
    """Fixture that installs an add-on.

    Returns:
        :py:class:`AddOnInstallComplete` Firefox notification.

    """
    confirmation_notification.install()
    return browser.wait_for_notification(AddOnInstallComplete)
