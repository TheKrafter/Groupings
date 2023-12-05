#!/usr/bin/env python3
# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

import sys

from groupy import Client
from groupme_push.client import PushClient

from .internal import ui, oauth
from .internal.lang import lang

# GLOBAL VARIABLES
global APPLICATION_ID
APPLICATION_ID = 'xyz.krafterdev.Groupings'

# Main Process
def main():
    logging.info("Starting Groupings...")
    logging.debug(f"Arguments: {sys.argv}")

    if sys.argv[-1].startswith('groupings:login'):
        try:
            oauth.do_oauth(sys.argv[-1], ui.run, APPLICATION_ID, logged_in=True)
        except BaseException as ex:
            ui.run(APPLICATION_ID, logged_in=False, login_failed=True, login_error=ex)
    else:
        try:
            token = oauth.get_token()
            logged_in = True
        except ValueError:
            logged_in = False
        ui.run(APPLICATION_ID, logged_in=logged_in, token=token)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    
