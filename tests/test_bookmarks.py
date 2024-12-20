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
    def keyword(self):
        """Returns the current list of keywords."""
        return self._keyword

    @keyword.setter
    def keyword(self, new_keyword: str):
        """Sets new keywords for the bookmark."""
        if isinstance(new_keyword, str):
            self._keyword = new_keyword
        else:
            raise ValueError("Keyword must be a string.")

    @property
    def tags(self):
        """Returns the current list of tags."""
        return self._tags

    @tags.setter
    def tags(self, new_tags: list[str]):
        """Sets new tags for the bookmark."""
        if isinstance(new_tags, list) and all(isinstance(t, str) for t in new_tags):
            self._tags = new_tags
        else:
            raise ValueError("Tags must be a list of strings.")


@pytest.fixture
def bookmark_entry() -> BookmarkEntry:
    """Fixture for creating a bookmark with only a URL."""
    return BookmarkEntry(url="https://www.mozilla.org/")


@pytest.fixture
def bookmark_star(
    browser: BrowserWindow, bookmark_entry: BookmarkEntry, selenium: WebDriver
) -> Bookmark:
    """Return a Bookmark instance created using the star button."""
    selenium.get(bookmark_entry.url)
    bookmark_using_star = browser.wait_for_bookmark()
    bookmark_using_star.add()
    return bookmark_using_star


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
    bookmark_using_menu.add_bookmark(bookmark_data)
    return bookmark_using_menu


def test_invalid_keyword(bookmark_entry: BookmarkEntry) -> None:
    """Test setting a non-string value to the keyword raises ValueError."""
    with pytest.raises(ValueError, match="Keyword must be a string."):
        bookmark_entry.keyword = 123


def test_invalid_tags(bookmark_entry: BookmarkEntry) -> None:
    """Test setting a non-list or invalid list to tags raises ValueError."""
    with pytest.raises(ValueError, match="Tags must be a list of strings."):
        bookmark_entry.tags = "tag1, tag2"
    with pytest.raises(ValueError, match="Tags must be a list of strings."):
        bookmark_entry.tags = [123, "tag2"]


def test_add_bookmark_star(
    bookmark_star: Bookmark,
) -> None:
    """Ensure the bookmark is added using the star button."""
    assert bookmark_star.is_bookmarked_star


def test_add_bookmark_menu(bookmark_menu: Bookmark) -> None:
    """Ensure the bookmark is added using the main bookmark menu."""
    assert bookmark_menu.is_bookmarked_menu


def test_retrieve_bookmark_star(bookmark_star: Bookmark) -> None:
    """Retrieve bookmark added using star button."""
    label = "Internet for people"
    assert bookmark_star.retrieve_bookmark(label) is True


def test_delete_bookmark_star(bookmark_star: Bookmark) -> None:
    """Delete bookmark added using star button."""
    bookmark_star.delete()
    assert bookmark_star.is_bookmarked_star is False


def test_retrieve_bookmark_menu(bookmark_menu: Bookmark) -> None:
    """Retrieve Bookmark added using the main bookmark menu."""
    label = "Internet for people"
    assert bookmark_menu.retrieve_bookmark(label) is True


def test_delete_bookmark_menu(bookmark_menu: Bookmark) -> None:
    """Delete bookmark added using the main bookmark menu"""
    label = "Internet for people"
    bookmark_menu.delete_bookmark(label)
    assert bookmark_menu.is_bookmarked_menu is False


def test_retrieve_deleted_bookmark_star(bookmark_star: Bookmark) -> None:
    """Test retrieve deleted bookmark (star button)."""
    label = "Internet for people"
    bookmark_star.delete()
    assert bookmark_star.retrieve_bookmark(label) is False


def test_retrieve_deleted_bookmark_menu(bookmark_menu: Bookmark) -> None:
    """Test retrieve deleted bookmark (main bookmark menu)."""
    label = "Internet for people"
    bookmark_menu.delete_bookmark(label)
    assert bookmark_menu.retrieve_bookmark(label) is False
