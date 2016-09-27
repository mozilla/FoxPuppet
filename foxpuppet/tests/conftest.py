import pytest
from foxpuppet.foxpuppet import FoxPuppet
from foxpuppet.ui.browser.window import Browser_Window


@pytest.fixture
def set_up(selenium):
    foxpuppet = FoxPuppet(selenium)
    foxpuppet.selenium.get('http://www.google.com')
    return foxpuppet


@pytest.fixture
def windows(set_up):
        return Browser_Window(set_up)
