# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from logging42 import logger

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from .lang import lang

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title(lang.title)
        self.set_default_size(740, 200)

        # INTERFACE
        self.flap_main = Adw.Flap.new()

        ## MESSAGES VIEW
        self.box_main_content = Gtk.Box.new( # Box of entire pane
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 5
        )

        self.header_main_content = Adw.HeaderBar.new() # Header for pane
        self.button_back_header_main = Gtk.Button.new_from_icon_name(
            "go-previous-symbolic"
        )
        self.header_main_content.pack_start(self.button_back_header_main)
        self.box_main_content.append(self.header_main_content)

        self.box_main_messages = Gtk.Box.new( # Box for Message View
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 10
        )
        self.box_main_messages.append(Gtk.Label.new(lang.debug.messages)) #DEBUG
        self.box_main_content.append(self.box_main_messages)
        
        self.box_main_input = Gtk.Box.new( # Box for Message send UI
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 5
        )
        self.box_main_input.append(Gtk.Label.new(lang.debug.input)) #DEBUG
        self.box_main_content.append(self.box_main_input)

        self.flap_main.set_content(self.box_main_content)

        ## GROUPS VIEW
        self.box_main_flap = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL,
            spacing = 5
        )
        self.flap_main.set_flap(self.box_main_flap)

        ### TESTING
        self.label_test2 = Gtk.Label.new(lang.debug.groups_list) #DEBUG
        self.box_main_flap.append(self.label_test2) #DEBUG

        self.set_content(self.flap_main)
    
    def show_flap(self, button):
        logger.debug('Revealing Flap!')
        self.flap_main.set_reveal_flap(True)


class MainApp(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def run(id: str, *args, **kwargs):
    logger.debug("Starting UI")
    app = MainApp(application_id=id)
    app.run(*args, **kwargs)