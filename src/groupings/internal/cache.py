# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import os
from xdg import BaseDirectory
from urllib.request import urlretrieve

from typing import Optional

from .lang import lang

GROUPME_IMAGEURL_PREFIX = 'https://i.groupme.com/'

def fetch(url: Optional[str]) -> Optional[str]:
    """ Fetch a file from GroupMe's image server.
    Returns path to locally cached version of file. If file URL is invalid, returns None. """
    if url == None:
        return None
    if url.startswith(GROUPME_IMAGEURL_PREFIX):
        # Then we have a valid image to use
        os.makedirs(os.path.join(BaseDirectory.xdg_cache_home, lang.id), exist_ok=True)
        cache_file_path = os.path.join(BaseDirectory.xdg_cache_home, lang.id, url.removeprefix(GROUPME_IMAGEURL_PREFIX))
        if os.path.exists(cache_file_path):
            return cache_file_path
        else:
            path, headers = urlretrieve(url, cache_file_path)
            return path
    else:
        return None