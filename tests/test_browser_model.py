# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from FoxPuppet.foxpuppet import FoxPuppet


class TestBrowserModel(object):

    def test_new_private_window(self, selenium):
        """Tests opening a new private browsing window via menu"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.open_window(private=True)
        assert len(foxpuppet.windows.all) == 2
        assert foxpuppet.browser.is_private is False
        foxpuppet.windows.focus(foxpuppet.windows.all[1])
        assert foxpuppet.browser.is_private is True

    def test_open_new_window(self, selenium):
        """Tests opening a new window via menu"""
        foxpuppet = FoxPuppet(selenium)
        foxpuppet.browser.open_window(private=False)
        assert len(foxpuppet.windows.all) == 2
        assert foxpuppet.browser.is_private is False
        foxpuppet.windows.focus(foxpuppet.windows.all[1])
        assert foxpuppet.browser.is_private is False
