# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Windows(object):

    def __init__(self, selenium):
        self.selenium = selenium
        self._handle = None

    @property
    def all(self):
        return self.selenium.window_handles

    @property
    def current(self):
        return self.selenium.current_window_handle

    def focus(self, handle):
        return self.selenium.switch_to.window(handle)

    @contextmanager
    def wait_for_new_window(self):
        handles_before = self.selenium.window_handles
        yield
        WebDriverWait(self.selenium, 5).until(
            lambda driver: len(handles_before) != len(driver.window_handles))

    @property
    def window_element(self):
        """Returns the inner DOM window element.

        :returns: DOM window element.
        """

        self.selenium.switch_to.window

        return self.selenium.find_element(By.CSS_SELECTOR, ':root')
