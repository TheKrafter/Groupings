#!/usr/bin/env python3
# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from logging42 import logger

import sys

from .internal import ui, oauth
from .internal.lang import lang

# GLOBAL VARIABLES
global APPLICATION_ID
APPLICATION_ID = 'xyz.krafterdev.Groupings'

# Code Here

if __name__ == '__main__':
    logger.success("Starting Groupings...")

    ui.run(APPLICATION_ID) # blocking
    