# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A simple web server."""

import os
import threading

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler that serves files from another directory."""

    def translate_path(self, path):
        """Change working directory and translate path.

        Returns:
            str: Path to web server resource

        """
        os.chdir(os.path.join(os.path.dirname(__file__), "web"))
        return SimpleHTTPRequestHandler.translate_path(self, path)


class WebServer(object):
    """Web server for serving local files within the /web directory."""

    def __init__(self, host="", port=8000):
        """Set up web server.

        Args:
            host (str): Hostname.
            port (int, optional): Port for web server.
                Optional and defaults to port 8000.
        """
        self.server = HTTPServer((host, port), MyRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    @property
    def host(self):
        """Hostname of the web server.

        Returns:
            str: Web server hostname.

        """
        return self.server.server_address[0]

    @property
    def port(self):
        """Web server port.

        Returns:
            int: Web server port.

        """
        return self.server.server_address[1]

    def start(self):
        """Start web server."""
        self.thread.start()

    def stop(self):
        """Stop web server."""
        self.server.shutdown()
        self.thread.join()

    def url(self, path="/"):
        """Web server URL.

        Args:
            path (str, optional): Path to append to the web server URL.

        Returns:
            str: URL of web server.

        """
        return "http://{0.host}:{0.port}{1}".format(self, path)
