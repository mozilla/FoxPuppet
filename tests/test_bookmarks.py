# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Bookmarks."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.bookmarks.bookmark import (
    Bookmark,
    BookmarkData,
)


class BookmarkEntry:
    """Class representing a Firefox bookmark entry."""

    def __init__(self, url: str, name: str = "", keyword: str = "", tags: list[str] = []):
        self.url = url
        self.name = name
        self._keyword = keyword
        self._tags = tags or []

    @property
    def keyword(self) -> str:
        """Returns the current keyword."""
        return self._keyword

    @keyword.setter
    def keyword(self, new_keyword: str):
        """Sets new keywords for the bookmark."""
        self._keyword = new_keyword

    @property
    def tags(self) -> list[str]:
        """Returns the current list of tags."""
        return self._tags

    @tags.setter
    def tags(self, new_tags: list[str]):
        """Sets new tags for the bookmark."""
        self._tags = new_tags


@pytest.fixture
def bookmark_entry() -> BookmarkEntry:
    """Fixture for creating a bookmark with only a URL."""
    return BookmarkEntry(url="https://www.mozilla.org/en-US/?v=a")


@pytest.fixture
def bookmark_star(
    browser: BrowserWindow, bookmark_entry: BookmarkEntry, selenium: WebDriver
) -> Bookmark:
    """Return a Bookmark instance created using the star button."""
    selenium.get(bookmark_entry.url)
    bookmark_using_star = browser.wait_for_bookmark()
    bookmark_using_star.add_bookmark()
    return bookmark_using_star


@pytest.fixture
def label() -> str:
    """Fixture for the bookmark label."""
    return "Internet for people"


@pytest.fixture
def bookmark_menu(
    browser: BrowserWindow, bookmark_entry: BookmarkEntry, selenium: WebDriver
) -> Bookmark:
    """Return a Bookmark instance created using main menu."""
    selenium.get(bookmark_entry.url)
    bookmark_using_menu = browser.wait_for_bookmark()
    bookmark_entry.name = "Internet fInternet for people"
    bookmark_entry.tags = ["Browser", "Open Source"]
    bookmark_entry.keyword = "Mozilla"
    bookmark_data: BookmarkData = {
        "name": bookmark_entry.name,
        "url": bookmark_entry.url,
        "tags": bookmark_entry.tags,
        "keyword": bookmark_entry.keyword,
    }
    bookmark_using_menu.add_bookmark(bookmark_data, is_detailed=True)
    return bookmark_using_menu


def test_page_is_bookmarked_using_star(
    bookmark_star: Bookmark,
) -> None:
    """Ensure the bookmark is added using the star button."""
    assert bookmark_star.is_bookmarked


def test_page_is_bookmarked_using_menu(bookmark_menu: Bookmark) -> None:
    """Ensure the bookmark is added using the main bookmark menu."""
    assert bookmark_menu.is_bookmarked


def test_retrieve_bookmark_star(bookmark_star: Bookmark, label: str) -> None:
    """Retrieve bookmark added using star button."""
    assert bookmark_star.bookmark_exists(label)


def test_delete_bookmark_star(bookmark_star: Bookmark, label: str) -> None:
    """Delete bookmark added using star button."""
    bookmark_star.delete_bookmark()
    assert bookmark_star.is_bookmarked is False
    assert bookmark_star.bookmark_exists(label) is False


def test_delete_bookmark_menu(bookmark_menu: Bookmark, label: str) -> None:
    """Delete bookmark added using the main bookmark menu"""
    bookmark_menu.delete_bookmark(label, is_detailed=True)
    assert bookmark_menu.is_bookmarked is False
    assert bookmark_menu.bookmark_exists(label) is False


def test_retrieve_deleted_bookmark_star(bookmark_star: Bookmark, label: str) -> None:
    """Test retrieve deleted bookmark (star button)."""
    bookmark_star.delete_bookmark()
    assert bookmark_star.bookmark_exists(label) is False


def test_retrieve_deleted_bookmark_menu(bookmark_menu: Bookmark, label: str) -> None:
    """Test retrieve deleted bookmark (main bookmark menu)."""
    bookmark_menu.delete_bookmark(label, is_detailed=True)
    assert bookmark_menu.bookmark_exists(label) is False
