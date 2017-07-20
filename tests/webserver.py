# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A simple webserver."""

import os
import threading

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):
    """Setup http requests for Webserver."""

    def translate_path(self, path):
        """Set path for local files.

        Returns:
            obj: SimpleHTTPRequestHandler

        """
        os.chdir(os.path.join(os.path.dirname(__file__), 'web'))
        return SimpleHTTPRequestHandler.translate_path(self, path)


class WebServer(object):
    """Webserver for serving local files within the /web directory."""

    def __init__(self, host='', port=8000):
        """Set up Webserver.

        Args:
            host (str): Hostname.
            port (str, optional): Port for webserver.
                Optional and defaults to port 8000.
        """
        self.server = HTTPServer((host, port), MyRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    @property
    def host(self):
        """Hostname of the WebServer.

        Returns:
            str: WebServer hostname.

        """
        return self.server.server_address[0]

    @property
    def port(self):
        """Webserver port.

        Returns:
            str: WebServer port address.

        """
        return self.server.server_address[1]

    def start(self):
        """Start Webserver."""
        self.thread.start()

    def stop(self):
        """Stop WebServer."""
        self.server.shutdown()
        self.thread.join()

    def url(self, path='/'):
        """Webserver URL.

        Returns:
            str: path to append to WebServer URL. Optional.

        """
        return 'http://{0.host}:{0.port}{1}'.format(self, path)
