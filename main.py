""" A GTK4/Libadwaita GroupMe Client using the GroupyAPI Library """

from logging42 import logger

import sys
import os
import time
import requests

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Adw, Gdk

from grouppy import GroupMeClient
import keyring


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_title("Groupings")
        self.set_default_size(480, 720)

        # Header
        self.header = Adw.HeaderBar.new()
        self.set_titlebar(self.header)

        # Construct Window
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_child(self.page)

        self.stack = Gtk.Stack.new()
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.page.append(self.sidebar)
        self.page.append(self.stack)

        self.chat_pages = {}
        self.got_messages = {}
        self.oldest_message = {}

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

            self.set_child(self.stack)
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
            current.set_size_request(300, 20)
            
            self.sidebar.append(current)

            self.create_page_for_group(group)
        
        logger.info(str(self.chat_pages))

    def create_page_for_group(self, group: dict):
        """ Add a stack page named by id for a given group """
        logger.debug(f'Creating page for group {group["id"]}')
        window = Gtk.ScrolledWindow.new()
        window.set_policy(hscrollbar_policy = Gtk.PolicyType.NEVER, vscrollbar_policy = Gtk.PolicyType.AUTOMATIC )

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(Gtk.Label.new(f'Group: {group["name"]}\nID: {group["id"]}'))
        box.set_size_request(500, 500)

        window.set_child(box)
        self.chat_pages[str(group["id"])] = box

        self.stack.add_named(window, group["id"])
        logger.debug(f'Created page for group {group["id"]}!')

    def on_group_open(self, widget, id, load_older ):
        """ Open group panel """
        logger.info(f'Open group {id}.')
        group = self.client.get_group(id)
        self.set_title('Groupings - ' + group["name"])
        
        self.stack.set_visible_child_name(str(id))

        child = self.stack.get_child_by_name(str(id))
        chatbox = self.chat_pages[str(id)]
            

        try:
            if self.got_messages[str(id)] == True:
                messages = self.client.get_messages_new(id)
        except KeyError:
            messages = self.client.get_messages(id, limit=20)
            self.got_messages[str(id)] = True

        got_oldest = False
        for msg in messages["messages"][::-1]:
            if not got_oldest:
                self.oldest_message[str(id)] = msg["id"]
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            box.set_size_request(400, 10)

            avatar = Adw.Avatar(text = msg["name"])
            avatar.set_size(35)
            avatar.set_show_initials(True)
            box.append(avatar)

            content = Adw.ActionRow.new()
            content.set_title(msg["name"])
            content.set_subtitle(msg["text"])
            box.append(content)

            chatbox.append(box)

    def on_message_send(self, widget, id, content, chatbox):
        """ Send a message to a group """
        self.client.send_message(id, text)
        return True

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
