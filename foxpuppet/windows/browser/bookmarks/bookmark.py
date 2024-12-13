# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains classes for handling Firefox bookmarks."""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from foxpuppet.windows.browser.navbar import NavBar
from typing import Type, Any, TYPE_CHECKING, Optional, TypedDict, List


class BookmarkData(TypedDict):
    """Bookmark properties."""

    name: str
    url: str
    tags: Optional[List[str]]
    keyword: Optional[str]


class BasicBookmark(NavBar):
    """Handles basic bookmark operations."""

    if TYPE_CHECKING:
        from foxpuppet.windows.browser.window import BrowserWindow

    @staticmethod
    def create(window: "BrowserWindow", root: WebElement) -> Optional["BasicBookmark"]:
        """Create a bookmark object.

        Args:
            window (:py:class:`BrowserWindow`): Window object this bookmark appears in
            root (:py:class:`~selenium.webdriver.remote.webelement.WebElement`): WebDriver element object for the bookmark panel

        Returns:
            :py:class:`BaseBookmark`: Bookmark instance or None
        """
        with window.selenium.context(window.selenium.CONTEXT_CHROME):
            try:
                return BasicBookmark(window, root)
            except NoSuchElementException:
                return None

    @property
    def is_bookmarked(self) -> bool:
        """Checks if the current page is bookmarked.

        Returns:
            bool: True if the page is bookmarked, False otherwise.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            star_button_image = self.find_element(BookmarkLocators.STAR_BUTTON_IMAGE)
            if star_button_image is not None:
                return star_button_image.get_attribute("starred") == "true"
            else:
                return False

    def add(self) -> None:
        """Add a Bookmark using the star button."""
        self.click_element(BookmarkLocators.STAR_BUTTON)
        self.click_element(BookmarkLocators.FOLDER_MENU)
        self.click_element(BookmarkLocators.OTHER_BOOKMARKS_STAR)
        self.click_element(BookmarkLocators.SAVE_BUTTON)

    def retrieve_bookmark(self, label: str) -> bool:
        """
        Check if a bookmark with the given label exists under 'Other Bookmarks'.

        Args:
            label (str): The name of the bookmark to search for.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.open_bookmark_menu(
                locator_panel=BookmarkLocators.PANEL_MENU,
                locator_bookmark=BookmarkLocators.PANEL_BOOKMARK_MENU,
            )
            panel_bookmarks = self.find_element(BookmarkLocators.PANEL_BOOKMARK_TOOLBAR)
            if panel_bookmarks is None:
                return False
            menu_items = panel_bookmarks.find_elements(
                By.CSS_SELECTOR, "toolbarbutton.bookmark-item"
            )
            if not menu_items:
                return False
            for item in menu_items:
                item_label = item.get_attribute("label")
                if item_label and label.lower() in item_label.lower():
                    return True

            return False

    def delete(self) -> None:
        """Delete a bookmark using the star button."""
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            star_button_image = self.find_element(BookmarkLocators.STAR_BUTTON_IMAGE)
            if star_button_image and star_button_image.get_attribute("starred") == "true":
                self.click_element(BookmarkLocators.STAR_BUTTON)
                self.click_element(BookmarkLocators.REMOVE_BUTTON)


class AdvancedBookmark(BasicBookmark):
    """Handles advanced bookmark operations."""

    if TYPE_CHECKING:
        from foxpuppet.windows.browser.window import BrowserWindow

    @staticmethod
    def create(window: "BrowserWindow", root: WebElement) -> Optional["AdvancedBookmark"]:
        """Create an advanced bookmark object.

        Args:
            window (:py:class:`BrowserWindow`): The window object where the bookmark appears.
            root (:py:class:`~selenium.webdriver.remote.webelement.WebElement`): WebElement for the bookmark panel.

        Returns:
            :py:class:`AdvancedBookmark`: An instance of AdvancedBookmark if successful, otherwise None.
        """
        with window.selenium.context(window.selenium.CONTEXT_CHROME):
            try:
                return AdvancedBookmark(window, root)
            except NoSuchElementException:
                return None

    @property
    def is_bookmarked(self) -> bool:
        """Checks if the current page is bookmarked.

        Returns:
            bool: True if the page is bookmarked, False otherwise.
        """
        current_page_title = self.selenium.title
        self.open_main_menu(
            locator_toolbar=BookmarkLocators.NAVIGATOR_TOOLBOX,
            locator_menu_bar=BookmarkLocators.MENU_BAR,
        )
        bookmark_menu = self.find_element(BookmarkLocators.MAIN_MENU_BOOKMARK)
        if bookmark_menu is None:
            return False
        self.click_element(BookmarkLocators.MAIN_MENU_BOOKMARK)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            menu_items = bookmark_menu.find_elements(
                By.CSS_SELECTOR, "menuitem.bookmark-item"
            )
            for item in menu_items:
                item_label = item.get_attribute("label")
                if item_label and item_label.lower() in current_page_title.lower():
                    return True

            return False

    def add_bookmark(self, bookmark_data: BookmarkData) -> None:
        """Add a Bookmark using the main bookmark menu."""
        self.open_main_menu(
            locator_toolbar=BookmarkLocators.NAVIGATOR_TOOLBOX,
            locator_menu_bar=BookmarkLocators.MENU_BAR,
        )
        self.click_element(BookmarkLocators.MAIN_MENU_BOOKMARK)
        self.context_click(BookmarkLocators.MANAGE_BOOKMARKS)
        self.click_element(BookmarkLocators.ADD_BOOKMARK)
        self.switch_to_frame(BookmarkLocators.ADD_BOOKMARK_FRAME)

        if bookmark_data["name"]:
            self.actions.send_keys(bookmark_data["name"]).perform()
        self.actions.send_keys(Keys.TAB).perform()

        if bookmark_data["url"]:
            self.actions.send_keys(bookmark_data["url"] + Keys.TAB).perform()

        tags = bookmark_data["tags"]
        if tags is not None:
            for tag in tags:
                self.actions.send_keys(tag).perform()
                self.actions.send_keys(",").perform()
            self.actions.send_keys(Keys.TAB).perform()

        if bookmark_data.get("keyword"):
            keyword = (
                bookmark_data["keyword"] if bookmark_data["keyword"] is not None else ""
            )
            self.actions.send_keys(keyword + Keys.TAB).perform()

        self.actions.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER).perform()
        self.actions.send_keys(Keys.TAB, Keys.ENTER).perform()
        self.switch_to_default_context()

    def delete_bookmark(self, label: str) -> None:
        """Delete a bookmark using the main bookmark menu."""
        self.open_main_menu(
            locator_toolbar=BookmarkLocators.NAVIGATOR_TOOLBOX,
            locator_menu_bar=BookmarkLocators.MENU_BAR,
        )
        bookmark_menu = self.find_element(BookmarkLocators.MAIN_MENU_BOOKMARK)
        if bookmark_menu is None:
            raise ValueError("Bookmark menu not found")
        self.click_element(BookmarkLocators.MAIN_MENU_BOOKMARK)
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            menu_item = bookmark_menu.find_element(
                By.CSS_SELECTOR, f"menuitem.bookmark-item[label='{label}']"
            )
            self.actions.context_click(menu_item).perform()
            self.click_element(BookmarkLocators.DELETE_MENU_ITEM)


class BookmarkLocators:
    ADD_BOOKMARK = (By.ID, "placesContext_new:bookmark")
    ADD_BOOKMARK_FRAME = (By.CSS_SELECTOR, "browser[class='dialogFrame']")
    BOOKMARK_PROPERTIES_DIALOG = (By.ID, "bookmarkproperties")
    DELETE_MENU_ITEM = (By.ID, "placesContext_deleteBookmark")
    FOLDER_MENU = (By.ID, "editBMPanel_folderMenuList")
    MAIN_MENU_BOOKMARK = (By.ID, "bookmarksMenu")
    MANAGE_BOOKMARKS = (By.ID, "bookmarksShowAll")
    MENU_BAR = (By.ID, "toggle_toolbar-menubar")
    NAME_FIELD = (By.ID, "editBMPanel_namePicker")
    NAVIGATOR_TOOLBOX = (By.ID, "navigator-toolbox")
    OTHER_BOOKMARKS = (By.ID, "OtherBookmarks")
    OTHER_BOOKMARKS_STAR = (By.ID, "editBMPanel_unfiledRootItem")
    PANEL_BOOKMARK_MENU = (By.ID, "appMenu-bookmarks-button")
    PANEL_BOOKMARK_TOOLBAR = (By.ID, "panelMenu_bookmarksMenu")
    PANEL_MENU = (By.ID, "PanelUI-menu-button")
    REMOVE_BUTTON = (By.ID, "editBookmarkPanelRemoveButton")
    SAVE_BOOKMARK = (By.CSS_SELECTOR, 'button[dlgtype="accept"][label="Save"]')
    SAVE_BUTTON = (By.ID, "editBookmarkPanelDoneButton")
    STAR_BUTTON = (By.ID, "star-button-box")
    STAR_BUTTON_IMAGE = (By.ID, "star-button")
    TOOLBAR_CONTEXT_MENU = (By.ID, "toolbar-context-menu")
