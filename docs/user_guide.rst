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

Now pass the Selenium object you created into the object::

    FoxPuppet(selenium)

Using FoxPuppet
---------------

These are some simple examples for using FoxPuppet.

Window Manager
~~~~~~~~~~~~~~

To set all current windows to their appropriate object types call the :py:func:`~foxpuppet.window_manager.windows` property::

    foxpuppet = FoxPuppet(selenium)

    foxpuppet.window_manager.windows

:Note: All windows except for the initial window is available through this method.

Open a window
~~~~~~~~~~~~~

To open a window call the function from the browser attribute within FoxPuppet::

    foxpuppet.browser.open_window()

To open a private window, set the private argument as True::

    foxpuppet.browser.open_window(private=True)

:Note: The default behavior for :py:func:`~foxpuppet.browser.open_window` is to open a non-private window.

Check if a window is private
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if the current window is private call the :py:func:`~foxpuppet.browser.is_private` property::

    foxpuppet.browser.is_private

Close a window
~~~~~~~~~~~~~~

To close a window call the :py:func:`~foxpuppet.browser.close()` function::

    foxpuppet.browser.close()

To close a specific window call the :py:func:`~foxpuppet.browser.close()` function on a window from the window managers list::

    foxpuppet.window_manager.windows[1].close()
