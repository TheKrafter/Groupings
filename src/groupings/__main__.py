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
    logger = logging.getLogger()
    logger.info("Starting Groupings...")
    logger.debug(f"Arguments: {sys.argv}")

    ui.run(APPLICATION_ID)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    
