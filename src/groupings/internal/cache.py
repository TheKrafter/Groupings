# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import os
import time
import logging
from xdg import BaseDirectory
from urllib import request
from urllib.error import HTTPError

from typing import Optional, Union

from .lang import lang

GROUPME_IMAGEURL_PREFIX = 'https://i.groupme.com/'
SPOOFED_HEADERS = [
    ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'),
    ('Accept-Encoding', 'gzip, deflate, br'),
]

def fetch(token: str, url: Optional[str]) -> Optional[Union[str, bool]]: #TODO: Doesn't need a token (?)
    """ Fetch a file from GroupMe's image server.
    Returns path to locally cached version of file. If file URL is invalid, returns None.
    If HTTP was unsuccessful, returns False """
    if url == None:
        return None
    if url.startswith(GROUPME_IMAGEURL_PREFIX):
        # Then we have a valid image to use
        os.makedirs(os.path.join(BaseDirectory.xdg_cache_home, lang.id), exist_ok=True)
        cache_file_path = os.path.join(BaseDirectory.xdg_cache_home, lang.id, url.removeprefix(GROUPME_IMAGEURL_PREFIX))
        if os.path.exists(cache_file_path):
            return cache_file_path
        else:
            try:
                opener = request.build_opener()
                opener.addheaders = SPOOFED_HEADERS
                request.install_opener(opener)
                path, headers = request.urlretrieve(url, cache_file_path)
                return path
            except HTTPError as ex:
                logging.warning(f'Failed to download file at "{url}": {ex}')
                return False
    else:
        return None