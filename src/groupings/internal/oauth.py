# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from logging42 import logger

from multiprocessing import Process

from .lang import lang

class OAuthFlow:
    def __init__(token):
        self.base_uri = 'https://oauth.groupme.com/oauth/authorize?client_id='
        
        self.success_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{lang.oauth.title}</title>
            </head>
            <body style="font-family:Cantarell,Sans-serif;padding-top:30px;">
                <center>
                    <h3><strong>{lang.oauth.success_message}</strong></h3>
                    <h4>{lang.oauth.safe_to_close}</h4>
                </center>
            </body>
        <html>
        """