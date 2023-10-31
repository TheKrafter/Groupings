# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')
from gi.repository import Gtk, Adw, WebKit

from .lang import lang

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        """ The Main Window is constructed here. """
        super().__init__(*args, **kwargs)

        self.set_title(lang.title)
        self.set_default_size(850, 500) # Width x Height

        # Interface
        self.view = Adw.OverlaySplitView.new()

        ## Chat Panel
        self.chat_box = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 5
            )
        self.chat_box.set_size_request(300, 500) # Width x Height
        self.chat_header = Adw.HeaderBar.new()
        self.chat_title = Adw.WindowTitle.new(lang.chat.title_start, lang.chat.subtitle_start)
        self.chat_header.set_title_widget(self.chat_title)
        self.chat_header_backbtn = Gtk.Button.new_from_icon_name("go-previous-symbolic")
        self.chat_header_backbtn.connect("clicked", self.toggle_sidebar)
        self.chat_header.pack_start(self.chat_header_backbtn)
        self.chat_box.append(self.chat_header)
        self.chat_box.append(Gtk.Label.new(lang.debug.messages)) #TODO
        self.view.set_content(self.chat_box)

        ## Groups List
        self.groups_box = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 8
            )
        self.groups_box.set_size_request(250, 500) # Width x Height
        self.groups_header = Adw.HeaderBar.new()
        self.groups_title = Adw.WindowTitle.new(lang.groups.title, "")
        self.groups_box.append(self.groups_header)
        self.groups_box.append(Gtk.Label.new(lang.debug.groups_list)) #TODO
        self.view.set_sidebar(self.groups_box)

        ## TODO: Breakpoints
        #self.breakpoint_condition = Adw.BreakpointCondition.new_and("min-width: 600sp", "max-width: 850sp")
        #self.breakpoint = Adw.Breakpoint.new()
        #self.breakpoint.add_setter(self.view, "collapsed", True)

        # Set Content
        self.set_content(self.view)
    
    
    def toggle_sidebar(self, button):
        """ Toggles the sidebar in self.view (Adw.OverlaySplitView) """
        if self.view.get_show_sidebar():
            self.view.set_show_sidebar(False)
        else:
            self.view.set_show_sidebar(True)
    
    def set_chat_titles(self, title, subtitle):
        """ Sets the Title and Subtitle for the Chat pane """
        self.chat_title.set_title(title)
        self.chat_title.set_title(subtitle)

class LoginWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        """ Window for Logging in. """
        super().__init__(*args, **kwargs)

        # Login window
        self.set_title(lang.oauth.title)
        self.set_default_size(300, 500)
        self.view = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 8
            )
        self.view.set_size_request(200, 300)

        ## Titlebar
        self.header = Adw.HeaderBar.new()
        self.view.append(self.header)

        ## Webview
        self.webview = WebKit.WebView.new()
        self.webview.load_uri("https://lite.duckduckgo.com/lite")
        self.view.append(self.webview)

        # Set Content
        self.set_content(self.view)

class MainApp(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        #self.win = MainWindow(application=app)
        self.win = LoginWindow(application=app)
        self.win.present()

def run(id: str, *args, **kwargs):
    logger = logging.getLogger()
    logger.debug("Starting UI")
    app = MainApp(application_id=id)
    app.run(*args, **kwargs)
