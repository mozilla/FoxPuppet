# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from foxpuppet import FoxPuppet


# Tests opening a new private browsing window via menu
def test_new_private_window(selenium):

    foxpuppet = FoxPuppet(selenium)
    selenium.get('http://www.google.com')
    selenium.set_context('chrome')
    foxpuppet.new_window(private=True)


# Tests opening a new window via menu
def test_open_new_window(selenium):

    foxpuppet = FoxPuppet(selenium)
    selenium.set_context('chrome')
    foxpuppet.new_window()
    selenium.set_context('content')
    selenium.get('http://www.android.com')
    assert selenium.title == 'Android'


# Tests adding a new bookmark
def test_bookmark_button(selenium):

    foxpuppet = FoxPuppet(selenium)
    selenium.set_context('chrome')
    foxpuppet.bookmark_page()


def test_new_tab_button(selenium):

    foxpuppet = FoxPuppet(selenium)
    selenium.get('http://www.google.com')
    selenium.set_context('chrome')
    foxpuppet.new_tab()
