# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

from urllib import parse

from .lang import lang

# GLOBAL CONSTANTS
global GROUPME_OAUTH_URI
global GROUPINGS_SYSTEM_NAME
global GROUPINGS_USER_NAME
GROUPME_OAUTH_URI = 'https://oauth.groupme.com/oauth/authorize?client_id=ZYi6KpWax6I6xANgfopm9G3VgMs9jTEeygBTyiRG0Ol64Nsx'
GROUPINGS_SYSTEM_NAME = 'Groupings'
GROUPINGS_USER_NAME = 'User'


class OAuthFlow:
    def __init__(self, callback, *args, **kwargs):
        self.oauth_uri = GROUPME_OAUTH_URI
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def start_oauth(self, uri):
        """ Starts OAuth flow with `groupings:login` uri """
        if uri.startswith('groupings:login'):
            token = parse.parse_qs(uri)['groupings:login?access_token'][0]
        
            # Save password in keying
        elif uri.startswith('groupings:token'):
            # For testing, manually specify token
            token = parse.parse_qs(uri)['groupings:token?access_token'][0]
        
        self.token = token

        self.callback(*self.args, token = self.token, **self.kwargs)
    
    def get_token(self, delete: bool = True):
        """ Fetch the token and delete it """
        token = self.token
        del self.token
        return token

def do_oauth(uri, callback, *args, **kwargs):
    """ Run OAuth """
    auth = OAuthFlow(callback, *args, **kwargs)
    auth.start_oauth(uri)
