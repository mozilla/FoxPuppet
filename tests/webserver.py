# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import threading

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        os.chdir(os.path.join(os.path.dirname(__file__), 'web'))
        return SimpleHTTPRequestHandler.translate_path(self, path)


class WebServer(object):

    def __init__(self, host='', port=8000):
        self.server = HTTPServer((host, port), MyRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    @property
    def host(self):
        return self.server.server_address[0]

    @property
    def port(self):
        return self.server.server_address[1]

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.thread.join()

    def url(self, path='/'):
        return 'http://{0.host}:{0.port}{1}'.format(self, path)
