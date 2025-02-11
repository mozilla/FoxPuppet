# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Creates Navbar object to interact with Firefox URL Bar."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class UrlBar:
    def __init__(self, selenium: WebDriver, wait: WebDriverWait):
        self.selenium = selenium
        self.wait = wait

    def check_suggestions(self, links: list) -> list:
        """Check if the provided links are present in the URL bar's suggestions."""
        urls = []
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            for link in links:
                url_bar = self.selenium.find_element(*URLBarLocators.INPUT_FIELD)
                url_bar.clear()
                url_bar.send_keys(link)

                self.wait.until(
                    lambda _: self.selenium.find_elements(*URLBarLocators.SEARCH_RESULTS)
                )

                search_results = self.selenium.find_elements(
                    *URLBarLocators.SEARCH_RESULT_ITEMS
                )

                for result in search_results:
                    url_span = result.find_element(*URLBarLocators.SEARCH_RESULT_ITEM)
                    if url_span.text in link and len(url_span.text) != 0:
                        urls.append(link)
                        break
        return urls


class URLBarLocators:
    INPUT_FIELD = (By.ID, "urlbar-input")
    SEARCH_RESULTS = (By.ID, "urlbar-results")
    SEARCH_RESULT_ITEM = (By.CSS_SELECTOR, "span.urlbarView-url")
    SEARCH_RESULT_ITEMS = (By.CSS_SELECTOR, "div.urlbarView-row[role='presentation']")
