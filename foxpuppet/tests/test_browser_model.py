# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from foxpuppet import FoxPuppet


def test_new_private_window(selenium):
    """Tests opening a new private browsing window via menu"""
    foxpuppet = FoxPuppet(selenium)
    foxpuppet.browser.navbar.open_window(private=True)


def test_open_new_window(selenium):
    """Tests opening a new window via menu"""
    foxpuppet = FoxPuppet(selenium)
    foxpuppet.browser.navbar.open_window()


def test_bookmark_button(selenium):
    """"Tests adding a new bookmark"""
    foxpuppet = FoxPuppet(selenium)
    foxpuppet.browser.navbar.bookmark_page()


def test_new_tab_button(selenium):
    """Tests opening a new tab via tab bar"""
    foxpuppet = FoxPuppet(selenium)
    foxpuppet.browser.tabbar.open_tab()
