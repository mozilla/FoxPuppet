from foxpuppet.foxpuppet import FoxPuppet


class Test_Browser_Window:

    # Tests minimizing the browser window
    def test_minimize_browser_window(self, windows, selenium):

        FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        windows.min_window_size()
        windows.close_all()
        selenium.quit()

    # Tests maximizing the browser window
    def test_maximize_browser_window(self, selenium, windows):

        FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        windows.min_window_size()
        windows.max_window_size()
        windows.close_all()
        selenium.quit()

    # Tests opening a new private browsing window via menu
    def test_new_private_window(self, selenium, windows):

        FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        windows.new_private_browsing_window()
        windows.close_all()
        selenium.quit()

    # Tests opening a new window via menu
    def test_open_new_window(self, selenium, windows):

        FoxPuppet(selenium)
        selenium.set_context('chrome')
        windows.new_window_button()
        selenium.set_context('content')
        selenium.get('http://www.android.com')
        selenium.set_context('chrome')
        assert selenium.title == 'Android'
        windows.close_all()
        selenium.quit()

    # Tests adding a new bookmark
    def test_bookmark_button(self, selenium, windows):

        FoxPuppet(selenium)
        selenium.set_context('chrome')
        windows.bookmark_page()
        windows.close_all()
        selenium.quit()
