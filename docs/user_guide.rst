User Guide
==========

.. contents:: :depth: 3

FoxPuppet uses Selenium as it's main driver. That means selenium commands work
right along with foxpuppet specific commands.

Driver
------

FoxPuppet requires a Selenium :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
object to be instantiated::

    from selenium.webdriver import Firefox
    selenium = Firefox()

Set Up
~~~~~~

To set up FoxPuppet simply pass the selenium object you created into the object::

    from foxpuppet import FoxPuppet
    FoxPuppet(selenium)


Usage Examples
--------------

These are some simple examples for using FoxPuppet.

Window Manager
~~~~~~~~~~~~~~

To set all current windows to their appropriate object types call the :py:func:`~foxpuppet.window_manager.windows` property::

    from foxpuppet import FoxPuppet
    foxpuppet = FoxPuppet(selenium)

    foxpuppet.window_manager.windows

Open a window
~~~~~~~~~~~~~

To open a window call the function from the browser attribute within foxpuppet::

    foxpuppet.browser.open_window()

To open a private window, set the private argument as True::

    foxpuppet.browser.open_window(private=True)

:Note: The default behavior for open window is to open a non-private window.

Check if a window is private
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if the current window is private call the :py:func:`~foxpuppet.browser.is_private` property::

    foxpuppet.browser.is_private

Close a window
~~~~~~~~~~~~~~

To close a window call the :py:func:`~foxpuppet.browser.close()` function::

    foxpuppet.browser.close()
