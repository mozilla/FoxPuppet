User Guide
==========

FoxPuppet is a library for automating user interactions in Firefox using Selenium.
This section gives some example use-cases of FoxPuppet.

Example
-------

This is an example for setting up FoxPuppet and opening a private window::

    from foxpuppet import FoxPuppet
    from selenium.webdriver import Firefox


    selenium = Firefox()
    foxpuppet = FoxPuppet(selenium)

    window = foxpuppet.browser.open_window(private=True)
    selenium.quit()

This example opens first a non-private browser window, then proceeds to open a private browser window.
Finally it quits via :py:func:`selenium.quit`.

:Note: The initial browser window is automatically assigned to the :py:attr:`browser` attribute and is always available.
