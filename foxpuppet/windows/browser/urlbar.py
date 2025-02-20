# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Creates Navbar object to interact with Firefox URL Bar."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from foxpuppet.region import Region


class UrlBar(Region):
    def suggestions(self, url: str) -> list[str]:
        """
        Get all URL suggestions shown in the URL bar.

        Args:
            url (str): The URL to type into the URL bar

        Returns:
            list[str]: List of suggested URLs that appear in the URL bar
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            url_bar = self.selenium.find_element(*URLBarLocators.INPUT_FIELD)
            url_bar.clear()
            url_bar.send_keys(url)

            self.wait.until(
                lambda _: self.selenium.find_elements(*URLBarLocators.SEARCH_RESULTS)
            )

            search_results = self.selenium.find_elements(
                *URLBarLocators.SEARCH_RESULT_ITEMS
            )

            suggested_urls = [
                result.find_element(*URLBarLocators.SEARCH_RESULT_ITEM).text
                for result in search_results
                if result.find_element(*URLBarLocators.SEARCH_RESULT_ITEM).text
            ]

            return suggested_urls


class URLBarLocators:
    INPUT_FIELD = (By.ID, "urlbar-input")
    SEARCH_RESULTS = (By.ID, "urlbar-results")
    SEARCH_RESULT_ITEM = (By.CSS_SELECTOR, "span.urlbarView-url")
    SEARCH_RESULT_ITEMS = (By.CSS_SELECTOR, "div.urlbarView-row[role='presentation']")
