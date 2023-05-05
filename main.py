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

        self.header = Adw.HeaderBar.new()
        self.set_titlebar(self.header)

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



        # Construct window
        ## Leaflet
        self.chat_leaflet = Adw.Leaflet.new() # can_navigate_back = True, hexpand = True
        self.chat_leaflet.set_can_navigate_back(True)
        self.chat_leaflet.set_hexpand(True)
        
        ### Left Pane
        self.chat_leaflet_left = Gtk.Box()
        #### HeaderBar
        #groups_headerbar = Adw.HeaderBar.new()
        #groups_headerbar.set_title_widget(Gtk.Label.new("Groups"))
        #self.chat_leaflet_left.append(groups_headerbar)
        #### ListBox
        self.groups_listing = Gtk.ListBox.new()
        self.groups_listing.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.groups_listing.set_hexpand(True)
        self.groups_listing.set_margin_top(12)
        self.groups_listing.set_margin_bottom(12)
        self.groups_listing.set_margin_start(6)
        self.groups_listing.set_margin_end(6)

        ##### Get Groups
        for group in self.client.get_groups():
            current = Adw.ActionRow.new()
            current.set_title(f'{group["name"]}')
            current.set_subtitle(f'{group["id"]}')
            current.connect('activated', self.on_group_open, group["id"])
            self.groups_listing.append(current)
        self.chat_leaflet_left.append(self.groups_listing)

        self.chat_leaflet.append(self.chat_leaflet_left)

        
        self.set_child(self.chat_leaflet)

    def on_group_open(self, group_id):
        """ Open group panel """
        logger.info(f'Open group {group_id}')
    
    

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="io.github.thekrafter.Groupings")
app.run(sys.argv)
