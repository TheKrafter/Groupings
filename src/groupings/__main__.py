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

# Code Here

if __name__ == '__main__':
    logging.info("Starting Groupings...")
    print('STARTING')
    logging.info(f"Arguments: {sys.argv}")

    ui.run(APPLICATION_ID) # blocking
    
