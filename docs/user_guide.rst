User Guide
==========

.. contents:: :depth: 3

:Note: FoxPuppet uses Selenium as it's main driver. That means Selenium commands work
       right along with FoxPuppet specific commands.

Example
-------

This is an example for setting up FoxPuppet and running a simple check to see if the browser window is private::

    from foxpuppet import FoxPuppet
    from selenium.webdriver import Firefox


    selenium = Firefox
    foxpuppet = FoxPuppet(selenium)

    assert not foxpuppet.browser.is_private
    foxpuppet.browser.open_window(private=True)
    assert foxpuppet.browser.is_private

:Note: The initial browser window is automatically assigned to the :py:attr:`browser` attribute and is always available.

Setup
------

FoxPuppet requires a Selenium :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
object to be instantiated::

    from foxpuppet import FoxPuppet
    from selenium.webdriver import Firefox


    selenium = Firefox()

Now pass the Selenium object you created into FoxPuppet::

    FoxPuppet(selenium)
