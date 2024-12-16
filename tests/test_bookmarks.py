# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Tests for Bookmarks."""

import pytest
from unittest.mock import Mock, patch
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from foxpuppet.windows import BrowserWindow
from foxpuppet.windows.browser.bookmarks.bookmark import (
    BasicBookmark,
    AdvancedBookmark,
    BookmarkData,
)


class Bookmark:
    """Class representing a Firefox bookmark."""

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
def bookmark() -> Bookmark:
    """Fixture for creating a bookmark with only a URL."""
    return Bookmark(url="https://www.mozilla.org/")


@pytest.fixture
def basic_bookmark(
    browser: BrowserWindow, bookmark: Bookmark, selenium: WebDriver
) -> BasicBookmark:
    """Return a BasicBookmark instance."""
    selenium.get(bookmark.url)
    bookmark_instance = browser.wait_for_bookmark(BasicBookmark)
    if bookmark_instance is None:
        raise ValueError("Failed to get BasicBookmark instance.")
    bookmark_instance.add()
    return bookmark_instance


@pytest.fixture
def advanced_bookmark(
    browser: BrowserWindow, bookmark: Bookmark, selenium: WebDriver
) -> AdvancedBookmark:
    """Return a AdvancedBookmark instance."""
    selenium.get(bookmark.url)
    bookmark_instance = browser.wait_for_bookmark(AdvancedBookmark)
    if bookmark_instance is None:
        raise ValueError("Failed to get AdvancedBookmark instance.")
    if not isinstance(bookmark_instance, AdvancedBookmark):
        raise ValueError("Expected AdvancedBookmark instance but got different type")
    bookmark.name = "Internet fInternet for people"
    bookmark.tags = ["Browser", "Open Source"]
    bookmark.keyword = "Mozilla"
    bookmark_data: BookmarkData = {
        "name": bookmark.name,
        "url": bookmark.url,
        "tags": bookmark.tags,
        "keyword": bookmark.keyword,
    }
    bookmark_instance.add_bookmark(bookmark_data)
    return bookmark_instance


def test_invalid_keyword(bookmark: Bookmark) -> None:
    """Test setting a non-string value to the keyword raises ValueError."""
    with pytest.raises(ValueError, match="Keyword must be a string."):
        bookmark.keyword = 123


def test_invalid_tags(bookmark: Bookmark) -> None:
    """Test setting a non-list or invalid list to tags raises ValueError."""
    with pytest.raises(ValueError, match="Tags must be a list of strings."):
        bookmark.tags = "tag1, tag2"
    with pytest.raises(ValueError, match="Tags must be a list of strings."):
        bookmark.tags = [123, "tag2"]


def test_create_basic_bookmark_none(browser: BrowserWindow) -> None:
    """Test BasicBookmark.create returns None on NoSuchElementException."""
    mock_root = Mock()
    with patch(
        "foxpuppet.windows.browser.bookmarks.bookmark.BasicBookmark.__init__"
    ) as mock_init:
        mock_init.side_effect = NoSuchElementException
        result = BasicBookmark.create(browser, mock_root)
        assert result is None


def test_create_advanced_bookmark_none(browser: BrowserWindow) -> None:
    """Test AdvancedBookmark.create returns None on NoSuchElementException."""
    mock_root = Mock()
    with patch(
        "foxpuppet.windows.browser.bookmarks.bookmark.AdvancedBookmark.__init__"
    ) as mock_init:
        mock_init.side_effect = NoSuchElementException
        result = AdvancedBookmark.create(browser, mock_root)
        assert result is None


def test_add_basic_bookmark(
    basic_bookmark: BasicBookmark,
) -> None:
    """Ensure the basic bookmark is added."""
    assert basic_bookmark.is_bookmarked


def test_retrieve_basic_bookmark(basic_bookmark: BasicBookmark) -> None:
    """Retrieve Basic Bookmark."""
    label = "Internet for people"
    assert basic_bookmark.retrieve_bookmark(label) is True


def test_delete_basic_bookmark(basic_bookmark: BasicBookmark) -> None:
    """Delete Advanced bookmark"""
    basic_bookmark.delete()
    assert basic_bookmark.is_bookmarked is False


def test_add_advanced_bookmark(
    advanced_bookmark: AdvancedBookmark,
) -> None:
    """Ensure the advanced bookmark is added."""
    assert advanced_bookmark.is_bookmarked


def test_retrieve_advanced_bookmark(advanced_bookmark: AdvancedBookmark) -> None:
    """Retrieve Advanced Bookmark."""
    label = "Internet for people"
    assert advanced_bookmark.retrieve_bookmark(label) is True


def test_retrieve_deleted_bookmark(basic_bookmark: BasicBookmark) -> None:
    """Test retrieve deleted bookmark."""
    basic_bookmark.delete()
    assert basic_bookmark.retrieve_bookmark("any label") is False


def test_delete_advanced_bookmark(advanced_bookmark: AdvancedBookmark) -> None:
    """Delete Advanced bookmark"""
    label = "Internet for people"
    advanced_bookmark.delete_bookmark(label)
    assert advanced_bookmark.is_bookmarked is False
