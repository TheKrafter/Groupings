""" A GTK4/Libadwaita GroupMe Client using the GroupyAPI Library """

from logging42 import logger

import sys
import os
import time

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from grouppy import GroupMeClient
import keyring


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_title("Groupings")
        self.set_default_size(480, 720)

        #self.header = Adw.HeaderBar.new()
        #self.set_titlebar(self.header)

        # Construct Window (Take Two)
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.leaflet = Adw.Leaflet(
            halign = Gtk.Align.FILL,
            valign = Gtk.Align.FILL
        )
        self.set_child(self.leaflet)

        self.page_groups = Gtk.Box(
            spacing = 4,
            halign = Gtk.Align.FILL,
            valign = Gtk.Align.FILL,
            hexpand = True,
            vexpand = True,
            orientation = Gtk.Orientation.VERTICAL
        )

        self.list_groups = Gtk.ListBox.new()
        self.list_groups.set_selection_mode(Gtk.SelectionMode.SINGLE)

        self.page_groups.append(self.list_groups)
        self.leaflet.append(self.page_groups)

        self.page_chat = Gtk.Box(
            spacing = 2,
            halign = Gtk.Align.FILL,
            valign = Gtk.Align.FILL,
            hexpand = True,
            vexpand = True,
            orientation = Gtk.Orientation.VERTICAL
        )
        placeholder = Gtk.Label(label="Select a Group")
        self.page_chat.append(placeholder)
        self.leaflet.append(self.page_chat)

    def login(self):
        # Establish Client
        self.client_id = "BNDU2FYRc9qOJOenhpVYB3SpIIPr7PJE8PNzBkriPOxiFw3Z"

        logger.info(f'Fetching access token for {os.environ["USER"]}...')
        # Fetch Keyring
        keyring.get_keyring()
        self.access_token = keyring.get_password("io.github.thekrafter.Groupings", os.environ["USER"])
        # Establish Client
        if self.access_token == None:
            # Inform user we're waiting for token
            self.waiting_screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.waiting_label = Gtk.Label(label='<strong>Waiting for browser authentication...</strong>')
            self.waiting_screen.append(self.waiting_label)
            self.set_child(self.waiting_screen)

            logger.debug(f'No token found. Logging in...')
            self.client = GroupMeClient(self.client_id, oauth_complete=False, app_name="Groupings")
            self.client.authenticate()
            logger.success(f'Logged in!')
            keyring.get_keyring()
            keyring.set_password("io.github.thekrafter.Groupings", os.environ["USER"], self.client.access_token)
            logger.info(f'Set new access token on keyring.')
        else:
            logger.success(f'Found access token!')
            self.client = GroupMeClient(self.access_token, oauth_complete=True)
        
    def populate_groups_list(self):
        """ Populate the list of groups """
        for group in self.client.get_groups():
            current = Adw.ActionRow.new()
            current.set_title(f'{group["name"]}')

            message = self.client.get_messages(group["id"], limit=1)['messages'][0]
            current.set_subtitle(f'{message["name"]}: {message["text"]}')
            
            current.connect('activated', self.on_group_open, group['id'])

            button = Gtk.Button.new()
            button.connect('clicked', self.on_group_open, group["id"])
            button.set_icon_name('user-available-symbolic')

            current.add_suffix(button)

            self.list_groups.append(current)

    def on_group_open(self, widget, id):
        """ Open group panel """
        logger.info(f'Open group {id}.')
        self.leaflet.set_visible_child(self.page_chat)

        self.page_chat



    def on_back_leaflet(self, button, name):
        pass
    
    

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

        self.win.login()
        self.win.populate_groups_list()

app = MyApp(application_id="io.github.thekrafter.Groupings")
app.run(sys.argv)
