# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Windows(object):

    def __init__(self, selenium):
        self.selenium = selenium
        self._handle = None

    @property
    def all(self):
        """Returns all current window handles"""
        return self.selenium.window_handles

    def focus(self, handle):
        """Switch Selenium focus to a specific window"""
        return self.selenium.switch_to.window(handle)

    @contextmanager
    def wait_for_new_window(self):
        handles_before = self.selenium.window_handles
        yield
        WebDriverWait(self.selenium, 10).until(
            lambda driver: len(handles_before) != len(driver.window_handles))

    @property
    def window_element(self):
        """Returns the inner DOM window element.

        :returns: DOM window element.
        """

        return self.selenium.find_element(By.CSS_SELECTOR, ':root')

    @property
    def focused_chrome_window_handle(self):
        """Returns the currently focused chrome window handle.

        :returns: The `window handle` of the focused chrome window.
        """
        def get_active_handle(mn):
            with self.selenium.using_context('chrome'):
                return self.selenium.execute_script("""
                  Components.utils.import("resource://gre/modules/Services.jsm");

                  let win = Services.focus.activeWindow;
                  if (win) {
                    return win.QueryInterface(Components.interfaces.nsIInterfaceRequestor)
                              .getInterface(Components.interfaces.nsIDOMWindowUtils)
                              .outerWindowID.toString();
                  }

                  return null;
                """)

        # In case of `None` being returned no window is currently active. This can happen
        # when a focus change action is currently happening. So lets wait until it is done.
        return WebDriverWait(self.selenium, 30).until(
            get_active_handle, message='No focused window has been found.')

    def switch_to(self, target):
        """Switches context to the specified chrome window.

        :param target: The window to switch to. `target` can be a `handle` or a
                       callback that returns True in the context of the desired
                       window.

        :returns: Instance of the selected :class:`BaseWindow`.
        """
        target_handle = None

        if target in self.selenium.chrome_window_handles:
            target_handle = target
        elif callable(target):
            current_handle = self.selenium.current_chrome_window_handle

            # switches context if callback for a chrome window returns `True`.
            for handle in self.selenium.chrome_window_handles:
                self.selenium.switch_to.window(handle)
                window = self.create_window_instance(handle)
                if target(window):
                    target_handle = handle
                    break

            # if no handle has been found switch back to original window
            if not target_handle:
                self.selenium.switch_to_window(current_handle)

        if target_handle is None:
            raise logging.error("No window found for '{}'" .format(target))

        # only switch if necessary
        if target_handle != self.selenium.current_chrome_window_handle:
            self.selenium.switch_to.window(target_handle)

        return self.create_window_instance(target_handle)

    @property
    def current(self):
        """Retrieves the currently selected chrome window.

        :returns: The :class:`BaseWindow` for the currently active window.
        """
        return self.create_window_instance(
            self.selenium.current_chrome_window_handle)

    @classmethod
    def register_window(cls, window_type, window_class):
        """Registers a chrome window with this class so that this class may in
        turn create the appropriate window instance later on.

        :param window_type: The type of window.
        :param window_class: The constructor of the window
        """
        cls.windows_map[window_type] = window_class


class BaseWindow(object):
    """Base Class for any kind of chrome window."""

    def __init__(self, selenium, window_handle):
        self._windows = Windows(selenium)

        if window_handle not in self.selenium.chrome_window_handles:
            pass

        self._handle = window_handle
