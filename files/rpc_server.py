#!/home/downloads/.venv/bin/python
# -*- coding: utf-8 -*-

""" XMLRPC-Server accepts new download links over the network

Requires RPC secret to be provided as an argument"""

from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import base64
import configparser

import ydl

RPC_USERNAME = 'downloads'  # hardcoded for now
RPC_PASSWORD = ydl.get_rpc_password()


class AuthServer(SimpleXMLRPCServer):
    """like SimpleXMLRPCServer, but with HTTP Basic auth"""

    def __init__(self, *args, **kwargs):
        class AuthRequestHandler(SimpleXMLRPCRequestHandler):
            def parse_request(myself):
                if SimpleXMLRPCRequestHandler.parse_request(myself):
                    if self.authenticate(myself.headers):
                        return True
                    else:
                        myself.send_error(401, "Authentication failure")
                        return False
        SimpleXMLRPCServer.__init__(self, requestHandler=AuthRequestHandler,
                                    *args, **kwargs
                                    )

    def authenticate(self, headers):
        """check if username and password match"""
        auth_headers = headers.get('Authorization')
        if not auth_headers:
            raise RuntimeError('authentication required')
        auth_method, encoded_auth = auth_headers.split(' ')
        if not auth_method == 'Basic':
            raise RuntimeError('Only HTTP Basic authentication is allowed')
        username, password = base64.b64decode(bytes(encoded_auth, 'utf-8')).split(b':')
        try:
            assert username.decode('utf-8') == RPC_USERNAME
            assert password.decode('utf-8') == RPC_PASSWORD
        except AssertionError:
            return False
        return True


class RequestHandler(SimpleXMLRPCRequestHandler):
    """restrict to a particular path"""
    rpc_path = "/RPC2"

server = AuthServer(("0.0.0.0", 6900),)
server.register_introspection_functions()


def add_download(url):
    """add url to youtube-dl -> aria2 -> tor chain for Downloading

    requires rpc_secret as a parameter for authentication"""
    filename, download_url = ydl.get_filename_and_url(url)
    ydl.add_download(filename, download_url)
server.register_function(add_download)
server.serve_forever()
