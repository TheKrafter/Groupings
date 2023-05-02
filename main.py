""" A GTK4/Libadwaita GroupMe Client using the GroupyAPI Library """

from logging42 import logger

import sys
import os
import time

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from groupy.client import Client
import keyring


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_title("Groupings")
        self.client_id = "BNDU2FYRc9qOJOenhpVYB3SpIIPr7PJE8PNzBkriPOxiFw3Z"
        self.set_default_size(720, 240)

        logger.info(f'Fetching access token for {os.environ["USER"]}...')
        # Fetch Keyring
        keyring.get_keyring()
        self.access_token = keyring.get_password("io.github.thekrafter.Groupings", os.environ["USER"])
        if self.access_token == None:
            # Get Access Token if it Doesn't Exist
            # ------------------------------------
            # 0. Show we're waiting for token
            # 1. Sends the user to the OAuth URL in their browser
            # 2. Sets up a flask server to accept the callback
            # 3. Gets the token from the passed 'access_token' argument, saving to to the keyring
            # 4. Waits for the value to be in the keyring
            # 5. Closes the webserver and continues

            # Inform user we're waiting for token
            self.waiting_screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.waiting_label = Gtk.Label(label='Waiting for browser authentication...')
            self.waiting_screen.append(self.waiting_label)
            self.set_child(self.waiting_screen)

            import webbrowser
            from flask import Flask, request
            from multiprocessing import Process
            
            # Open in Browser
            webbrowser.open(f'https://oauth.groupme.com/oauth/authorize?client_id={self.client_id}')

            # Define Webserver
            html_success_page = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>{self.get_title()} Authentication</title>
                </head>
                <body style="font-family:Cantarell,Sans-serif;padding-top:30px;">
                    <center>
                        <h3><strong>Success!</strong></h3>
                        <h4>You may now close this window.</h4>
                    </center>
                </body>
            <html>
            """
            self.flask_server = Flask(__name__)
            @self.flask_server.route('/oauth', methods=['GET'])
            def oauth():
                args = request.args
                keyring.set_password("io.github.thekrafter.Groupings", os.environ["USER"], args.get('access_token'))
                return html_success_page
        
            # Start Webserver
            webserver = Process(target=self.flask_server.run, kwargs=dict(host='127.0.0.1', port='8089'))
            webserver.start()

            # Wait for oauth to complete
            waited = 0
            while keyring.get_password("io.github.thekrafter.Groupings", os.environ["USER"]) == None:
                time.sleep(5)
                waited += 5
                logger.debug(f'Waiting for access token... ({waited} seconds)')
            
            # Once complete, tidy up
            self.access_token = keyring.get_password("io.github.thekrafter.Groupings", os.environ["USER"])
            logger.success(f'Got access token!')
            webserver.kill()
            webserver.join()
        
        else:
            logger.success(f'Found access token!')

        # Establish Client
        self.client = Client.from_token(self.access_token)

        # Construct window
        self.box_grouplist = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box_grouplist)
        ## Add group items
        self.listbox_groups = Gtk.ListBox()
        for group in client.groups.list():
            current = Gtk.ListBoxRow(label=group.name, description=group.id)
            self.listbox_groups.append(current)
    
    

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="io.github.thekrafter.Groupings")
app.run(sys.argv)
