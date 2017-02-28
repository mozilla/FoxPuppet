# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


class NavBar(object):

    """Representation of the NavBar
    :param selenium: WebDriver Object
    :type selenium:
        :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object
    """

    _tracking_protection_shield_locator = (By.CSS_SELECTOR, '#tracking-protection-icon:-moz-lwtheme')

    def __init__(self, selenium, *args, **kwargs):
        self.selenium = selenium

    @property
    def tracking_shield(self):
        """Returns the Tacking Protection enabled shield"""
        time.sleep(30)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            return self.selenium.find_element(
                *self._tracking_protection_shield_locator)
            #WebDriverWait(self.selenium, timeout=10).until(
            #    lambda _: self.selenium.find_element(
            #        *self._tracking_protection_shield_locator)
            #)
