# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from foxpuppet import FoxPuppet


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
