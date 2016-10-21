from foxpuppet import FoxPuppet
from time import sleep


class Test_new_window_handle:

    def test_new_private_window(self, selenium):

        foxpuppet = FoxPuppet(selenium)
        selenium.get('http://www.google.com')
        selenium.set_context('chrome')
        menu = selenium.find_element_by_id('main-menubar')
        menu.get_attribute('File')
        menu.click()
        menu.get_attribute('New Private Window')
        menu.click()
        sleep(5)
