# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

from urllib import parse
from groupy import Client

from .lang import lang

import gi
gi.require_version('Secret', '1')

from gi.repository import Secret

# GLOBAL CONSTANTS
global GROUPME_OAUTH_URI
global GROUPINGS_SYSTEM_NAME
global GROUPINGS_USER_NAME
GROUPME_OAUTH_URI = 'https://oauth.groupme.com/oauth/authorize?client_id=ZYi6KpWax6I6xANgfopm9G3VgMs9jTEeygBTyiRG0Ol64Nsx'
GROUPINGS_SYSTEM_NAME = 'xyz.krafterdev.Groupings.Store'
GROUPINGS_USER_NAME = 'user'

global SECRET_SCHEMA 
SECRET_SCHEMA = Secret.Schema.new(
    GROUPINGS_SYSTEM_NAME,
    Secret.SchemaFlags.DONT_MATCH_NAME,
    {
        'Title': Secret.SchemaAttributeType.STRING,
        'Notes': Secret.SchemaAttributeType.STRING,
        'Description': Secret.SchemaAttributeType.STRING,
    }
)

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
        
            client = Client.from_token(token)
            you = client.user.get_me()

            attrs = {
                'Title': GROUPINGS_SYSTEM_NAME,
                'Notes': lang.oauth.secret_notes + you["id"],
                'Description': lang.oauth.secret_title,
            }
            r = Secret.password_store_sync(
                SECRET_SCHEMA,
                attrs,
                Secret.COLLECTION_DEFAULT,
                GROUPINGS_SYSTEM_NAME,
                token,
                None
            )
            if not r:
                raise ValueError('Failed to store token!')

        elif uri.startswith('groupings:token'):
            # For testing, manually specify token
            token = parse.parse_qs(uri)['groupings:token?access_token'][0]        

        self.callback(*self.args, token = token, **self.kwargs)

def get_token(delete: bool = False):
    """ Fetch the token and (optionally) delete it """
    attrs = {
        'Title': GROUPINGS_SYSTEM_NAME
    }
    token = Secret.password_lookup_sync(
        SECRET_SCHEMA,
        attrs,
        None
    )

    if delete:
        Secret.password_clear_sync(
            SECRET_SCHEMA,
            attrs,
            None
        )
    return token

def do_oauth(uri, callback, *args, **kwargs):
    """ Run OAuth """
    auth = OAuthFlow(callback, *args, **kwargs)
    auth.start_oauth(uri)
