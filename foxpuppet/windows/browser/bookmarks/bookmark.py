# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""Contains classes for handling Firefox bookmarks."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from foxpuppet.windows.browser.navbar import NavBar
from typing import TYPE_CHECKING, Optional, TypedDict, List


class BookmarkData(TypedDict):
    """Bookmark properties."""

    name: str
    url: str
    tags: Optional[List[str]]
    keyword: Optional[str]


class Bookmark(NavBar):
    """Handles Bookmark operations in Firefox."""

    if TYPE_CHECKING:
        from foxpuppet.windows.browser.window import BrowserWindow

    @staticmethod
    def create(window: "BrowserWindow", root: WebElement) -> "Bookmark":
        """Create a bookmark object.

        Args:
            window (:py:class:`BrowserWindow`): Window object this bookmark appears in
            root (:py:class:`~selenium.webdriver.remote.webelement.WebElement`): WebDriver element object for bookmark

        Returns:
            :py:class:`Bookmark`: Bookmark instance
        """
        with window.selenium.context(window.selenium.CONTEXT_CHROME):
            return Bookmark(window, root)

    @property
    def is_bookmarked(self) -> bool:
        """Checks if the current page is bookmarked using the star button.

        Returns:
            bool: True if the page is bookmarked, False otherwise.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            star_button_image = self.selenium.find_element(
                *BookmarkLocators.STAR_BUTTON_IMAGE
            )
            return star_button_image.get_attribute("starred") == "true"

    def add_bookmark(
        self, bookmark_data: Optional[BookmarkData] = None, is_detailed: bool = False
    ) -> None:
        """
        Add a bookmark using either quick add (star button) or detailed menu approach.

        Args:
            detailed (bool, optional): Whether to use detailed menu approach. Defaults to False.
            bookmark_data (BookmarkData, optional): Data for the bookmark when using detailed menu.
                Required when detailed is True.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if not is_detailed:
                self.selenium.find_element(*BookmarkLocators.STAR_BUTTON_IMAGE).click()
                self.selenium.find_element(*BookmarkLocators.FOLDER_MENU).click()
                self.selenium.find_element(*BookmarkLocators.OTHER_BOOKMARKS_STAR).click()
                self.selenium.find_element(*BookmarkLocators.SAVE_BUTTON).click()
            else:
                with self.selenium.context(self.selenium.CONTEXT_CHROME):
                    self.actions.context_click(
                        self.selenium.find_element(*BookmarkLocators.NAVIGATOR_TOOLBOX)
                    ).perform()
                    WebDriverWait(self.selenium, 10).until(
                        EC.presence_of_element_located(BookmarkLocators.MENU_BAR)
                    )
                    self.selenium.find_element(*BookmarkLocators.MENU_BAR).click()
                    self.selenium.find_element(
                        *BookmarkLocators.MAIN_MENU_BOOKMARK
                    ).click()
                    self.actions.context_click(
                        self.selenium.find_element(*BookmarkLocators.MANAGE_BOOKMARKS)
                    ).perform()
                    self.selenium.find_element(*BookmarkLocators.ADD_BOOKMARK).click()

                    bookmark_frame = self.selenium.find_element(
                        *BookmarkLocators.ADD_BOOKMARK_FRAME
                    )
                    self.selenium.switch_to.frame(bookmark_frame)
                    if bookmark_data:
                        if bookmark_data["name"]:
                            self.actions.send_keys(bookmark_data["name"]).perform()
                        self.actions.send_keys(Keys.TAB).perform()

                        if bookmark_data["url"]:
                            self.actions.send_keys(
                                bookmark_data["url"] + Keys.TAB
                            ).perform()

                        if (tags := bookmark_data["tags"]) is not None:
                            for tag in tags:
                                self.actions.send_keys(tag).perform()
                                self.actions.send_keys(",").perform()
                            self.actions.send_keys(Keys.TAB).perform()

                        if bookmark_data.get("keyword"):
                            keyword = bookmark_data["keyword"] or ""
                            self.actions.send_keys(keyword + Keys.TAB).perform()

                    self.actions.send_keys(
                        Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER
                    ).perform()
                    if folder := self.selenium.find_element(
                        *BookmarkLocators.BOOKMARK_FOLDER
                    ):
                        folder.click()
                        self.selenium.switch_to.frame(folder)
                        self.actions.send_keys(Keys.TAB, Keys.ENTER).perform()

    def bookmark_exists(self, label: str) -> bool:
        """
        Check if a bookmark with the given label exists.

        Args:
            label (str): The name of the bookmark to search for.
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            self.selenium.find_element(*BookmarkLocators.PANEL_MENU).click()
            self.selenium.find_element(*BookmarkLocators.PANEL_BOOKMARK_MENU).click()
            panel_bookmarks = self.selenium.find_element(
                *BookmarkLocators.PANEL_BOOKMARK_TOOLBAR
            )
            menu_items = panel_bookmarks.find_elements(
                By.CSS_SELECTOR, "toolbarbutton.bookmark-item"
            )
            if any(
                label.lower() in item_label.lower()
                for item in menu_items
                if (item_label := item.get_attribute("label"))
            ):
                return True
        return False

    def delete_bookmark(
        self, label: Optional[str] = None, is_detailed: bool = False
    ) -> None:
        """
        Delete a bookmark using either quick delete (star button) or detailed menu approach.

        Args:
            detailed (bool, optional): Whether to use detailed menu approach. Defaults to False.
            label (str, optional): Label of the bookmark to delete when using detailed approach.
                Required when detailed is True.

        Returns:
            bool: True if bookmark was successfully deleted (always True for detailed approach)
        """
        with self.selenium.context(self.selenium.CONTEXT_CHROME):
            if not is_detailed:
                star_button_image = self.selenium.find_element(
                    *BookmarkLocators.STAR_BUTTON_IMAGE
                )
                if (
                    star_button_image
                    and star_button_image.get_attribute("starred") == "true"
                ):
                    self.selenium.find_element(
                        *BookmarkLocators.STAR_BUTTON_IMAGE
                    ).click()
                    self.selenium.find_element(*BookmarkLocators.REMOVE_BUTTON).click()
                return
            self.actions.context_click(
                self.selenium.find_element(*BookmarkLocators.NAVIGATOR_TOOLBOX)
            ).perform()
            self.selenium.find_element(*BookmarkLocators.MENU_BAR).click()
            bookmark_menu = self.selenium.find_element(
                *BookmarkLocators.MAIN_MENU_BOOKMARK
            )
            self.selenium.find_element(*BookmarkLocators.MAIN_MENU_BOOKMARK).click()
            menu_item = bookmark_menu.find_element(
                By.CSS_SELECTOR, f"menuitem.bookmark-item[label='{label}']"
            )
            self.actions.context_click(menu_item).perform()
            self.selenium.find_element(*BookmarkLocators.DELETE_MENU_ITEM).click()


class BookmarkLocators:
    ADD_BOOKMARK = (By.ID, "placesContext_new:bookmark")
    ADD_BOOKMARK_FRAME = (By.CSS_SELECTOR, "browser[class='dialogFrame']")
    BOOKMARK_FOLDER = (
        By.CSS_SELECTOR,
        "browser.dialogFrame[name='dialogFrame-window-modal-dialog-subdialog']",
    )
    BOOKMARK_PROPERTIES_DIALOG = (By.ID, "bookmarkproperties")
    DELETE_MENU_ITEM = (By.ID, "placesContext_deleteBookmark")
    FOLDER_MENU = (
        By.CSS_SELECTOR,
        "#editBookmarkPanelContent .editBMPanel_folderRow #editBMPanel_folderMenuList",
    )
    MAIN_MENU_BOOKMARK = (By.ID, "bookmarksMenu")
    MANAGE_BOOKMARKS = (By.ID, "bookmarksShowAll")
    MENU_BAR = (By.ID, "toggle_toolbar-menubar")
    NAME_FIELD = (By.ID, "editBMPanel_namePicker")
    NAVIGATOR_TOOLBOX = (By.ID, "TabsToolbar")
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
