# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from foxpuppet import FoxPuppet


class Test_Browser_Window:

    # Tests minimizing the browser window
    def test_minimize_browser_window(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        foxpuppet.minimize()

    # Tests maximizing the browser window
    def test_maximize_browser_window(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        foxpuppet.minimize()
        foxpuppet.maximize()

    # Tests opening a new private browsing window via menu
    def test_new_private_window(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        foxpuppet.new_window(private=True)

    # Tests opening a new window via menu
    def test_open_new_window(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.set_context('chrome')
        foxpuppet.new_window()
        selenium.set_context('content')
        selenium.get('http://www.android.com')
        selenium.set_context('chrome')
        assert selenium.title == 'Android'

    # Tests adding a new bookmark
    def test_bookmark_button(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.set_context('chrome')
        foxpuppet.bookmark_page()
