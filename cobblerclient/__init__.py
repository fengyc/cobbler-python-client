# -*- coding: utf-8 -*-

"""
Copyright (c) 2017, Yingcai FENG <fengyc.work AT gmail>

Under MIT license, see LICENSE.
"""

import functools
from xmlrpc.client import ServerProxy



class CobblerClient(object):
    """Cobbler API client."""

    def __init__(self, uri="http://127.0.0.1/cobbler_api", username='cobbler',
                 password=None, *args, **kwargs):
        """Create a cobbler client.

        :param uri:  URI of cobbler api
        :param username: Cobbler username
        :param password: Cobbler password

        """
        self.url = uri
        self.username = username
        self.password = password
        self._token = kwargs.get("token", None)
        if uri.startswith("https"):
            context = kwargs.get("context", None)
            if context is not None:
                self._proxy = ServerProxy(uri, context=context)
                return
        self._proxy = ServerProxy(uri)
        super(CobblerClient, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self._proxy.__getattr__(item)

    def login(self, username=None, password=None):
        """Login and get a token.

        Login with the given username and password, if successful returns a
        token which must be used on latter method calls.
        """
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        try:
            self._token = self._proxy.login(username, password)
        except:
            raise

    def logout(self):
        """Logout and retires the current token."""
        try:
            self._proxy.logout()
        return True

    def check(self, token=None):
        pass

    def xapi_object_edit(self, object_type, object_name, edit_type, attributes):
        """Old style api call.

        Old style api for backwards compatibility and cause less XMLRPC traffic.
        Use new_, modify_, save_ directly for new style object manipulations.

        :param object_type:
        :param object_name:
        :param edit_type: One of 'add', 'rename', 'copy', 'remove'
        """
        return self._proxy.xapi_object_edit(object_type, object_name, edit_type,
                                            attributes)
