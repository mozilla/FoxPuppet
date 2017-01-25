User Guide
==========

.. contents:: :depth: 3

Example
-------

This is an example for setting up FoxPuppet and running a simple check to see if the browser window is private::

    from foxpuppet import FoxPuppet
    from selenium.webdriver import Firefox


    selenium = Firefox(
        firefox_binary='path/to/firefox-bin'
    )
    foxpuppet = FoxPuppet(selenium)

    window = foxpuppet.browser.open_window(private=True)
    window.close()
    foxpuppet.browser.close()
    selenium.quit()

This test opens a non-private and a private browser window and then closes both of the windows using :py:func:`close()`.
Finally it quits via :py:func:`selenium.quit`.

:Note: The initial browser window is automatically assigned to the :py:attr:`browser` attribute and is always available.
