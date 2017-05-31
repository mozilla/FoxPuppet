# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from foxpuppet import FoxPuppet


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
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
    from .webserver import WebServer
    webserver = WebServer()
    webserver.start()
    yield webserver
    webserver.stop()


@pytest.fixture
def browser(foxpuppet):
    """Initial Firefox browser window."""
    return foxpuppet.browser


@pytest.fixture
def foxpuppet(selenium):
    return FoxPuppet(selenium)


@pytest.fixture(scope='session', autouse=True)
def install_geckodriver():
    import requests
    import os
    from bs4 import BeautifulSoup

    r = requests.get('https://github.com/mozilla/geckodriver/releases')
    soup = BeautifulSoup(r.text, 'html.parser')
    latest = soup.find('div', {'class': 'label-latest'})
    for link in latest.find_all('a'):
        if 'linux64' in link.get('href'):
            url = 'https://github.com' + link.get('href')
            os.putenv('GECKODRIVER_URL', url)
    os.system('curl -L -o geckodriver.tar.gz $GECKODRIVER_URL')
    os.system('mkdir $HOME/geckodriver \
        && tar xvf geckodriver.tar.gz -C $HOME/geckodriver')
    os.system('export PATH=$HOME/geckodriver:$PATH')
    os.system('geckodriver --version')
