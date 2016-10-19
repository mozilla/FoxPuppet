# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from foxpuppet import FoxPuppet


class TestBrowserModel(object):

    def test_new_private_window(self, selenium):
        """Tests opening a new private browsing window via menu"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.open_window(private=True)
        open_windows = foxpuppet.browser.windows.all
        assert len(open_windows) == 2
        assert foxpuppet.browser.is_private is False
        foxpuppet.browser.windows.focus(open_windows[1])
        assert foxpuppet.browser.is_private is True

    def test_open_new_window(self, selenium):
        """Tests opening a new window via menu"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.open_window(private=False)
        open_windows = foxpuppet.browser.windows.all
        assert len(open_windows) == 2
        assert foxpuppet.browser.is_private is False
        foxpuppet.browser.windows.focus(open_windows[1])
        assert foxpuppet.browser.is_private is False

    def test_bookmark_button(self, selenium):
        """"Tests adding a new bookmark"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.navbar.bookmark_page()

    def test_new_tab_button(self, selenium):
        """Tests opening a new tab via tab bar"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.tabbar.open_tab()
