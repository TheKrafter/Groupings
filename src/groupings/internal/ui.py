# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging
import webbrowser
import sys

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
#gi.require_version('Gdk', '4')
#gi.require_version('GdkPixbuf', '2')
from gi.repository import Gtk, Adw, Gdk, GdkPixbuf

from groupy.client import Client
import groupy.exceptions

from groupy import Client

from .lang import lang
from . import oauth, push, cache

class GroupListItem:
    def __init__(self, group):
        """ Widget for a Group shown in the list """
        self.box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        # Avatar
        self.avatar = Adw.Avatar(size=32, text=group.name)
        avatar_filename = cache.fetch(group.image_url)
        if avatar_filename != None:
            self.texture_avatar = Gdk.Texture.new_for_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file(filename=avatar_filename)
                )
            self.avatar.set_custom_image(self.texture_avatar)
        self.box.append(self.avatar)
        # Label
        self.box_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        if len(group.name) > 25:
            title = group.name[0:22].strip() + '...'
        else:
            title = group.name
        self.label_title = Gtk.Label.new(f'<b>{title}</b>')
        self.label_title.set_use_markup(True)
        self.box_info.append(self.label_title)
        self.label_msg = Gtk.Label.new(group.description[0:25].strip())
        self.box_info.append(self.label_msg)
        self.box.append(self.box_info)

        self.button = Gtk.Button.new()
        self.button.set_label(group.name)
        self.button.set_child(self.box)


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, token = None, **kwargs):
        """ The Main Window is constructed here. """
        super().__init__(*args, **kwargs)
        self.token = token
        self.client = Client.from_token(self.token)
        self.groups = {}

        self.set_title(lang.title)
        self.set_default_size(850, 500) # Width x Height
        self.set_size_request(300, 400)

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
        self.groups_list = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.groups_box.append(self.groups_list)
        self.visible_group_pages = 0
        self.groups_loadbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.groups_loadbutton = Gtk.Button.new_with_label(lang.groups.load_more)
        self.groups_loadbutton.connect('clicked', self.load_more_groups)
        self.groups_loadbox.append(self.groups_loadbutton)
        self.groups_box.append(self.groups_loadbox)

        self.groups_scroll = Gtk.ScrolledWindow.new()
        self.groups_list = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.groups_box.append(self.groups_list)
        self.visible_group_pages = 0
        self.groups_loadbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.groups_loadbutton = Gtk.Button.new_with_label(lang.groups.load_more)
        self.groups_loadbutton.connect('clicked', self.load_more_groups)
        self.groups_loadbox.append(self.groups_loadbutton)
        self.groups_box.append(self.groups_loadbox)
        self.view.set_sidebar(self.groups_box)

        # Breakpoint
        self.condition = Adw.BreakpointCondition.parse("max-width: 500sp")
        self.breakpoint = Adw.Breakpoint.new(self.condition)
        self.breakpoint.add_setter(self.view, "collapsed", True)
        self.add_breakpoint(self.breakpoint)

        # Set Content
        self.set_content(self.view)

        self.selected_group = None
    
    def init_load(self, *args, **kwargs):
        """ Loads groups, chats, etc. """
        try:
            self.client = Client.from_token(self.token)
            self.groups = {}
            #TODO: Remove children of self.groups_list
            for group in self.client.groups.list():
                self.groups[group.id] = GroupListItem(group)
                self.groups[group.id].button.connect('clicked', self.select_group, group.id)
                self.groups_list.append(self.groups[group.id].button)
            self.visible_group_pages = 1

        except groupy.exceptions.BadResponse as ex:
            self.error_dialog(ex, self.init_load())
            
    
    def load_more_groups(self, button):
        """ Loads more groups when the button is pressed """


    def select_group(self, button, group):
        """ Sets selected group"""
        self.select_group = group
        group_obj = self.client.groups.get(group)
        self.set_chat_titles(
            group_obj.name, group_obj.description
        )
        print(f'Selected GROUP: {group}')
    
    def toggle_sidebar(self, button):
        """ Toggles the sidebar in self.view (Adw.OverlaySplitView) """
        if self.view.get_show_sidebar():
            self.view.set_show_sidebar(False)
        else:
            self.view.set_show_sidebar(True)
    
    def set_chat_titles(self, title, subtitle):
        """ Sets the Title and Subtitle for the Chat pane """
        self.chat_title.set_title(title)
        self.chat_title.set_subtitle(subtitle)
    
    def show_pref_pane(self, button):
        """ Shows the prefrences pane """

    def error_dialog(self, ex, callback):
        """ Presents an error dialog """
        dialog = Adw.MessageDialog.new(self, lang.error.token.title, lang.error.token.description(ex))
        dialog.add_response('retry', lang.error.token.choice_retry, callback)
        dialog.add_response('quit', lang.error.token.choice_quit)
        dialog.set_response_appearance('quit', Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response('retry')
        dialog.connect('response', self.error_dialog_response)
        dialog.choose()
        dialog.response(dialog.get_close_response())

    def error_dialog_response(self, dialog, response, callback):
        """ Handles response to error dialog """
        match response:
            case 'retry':
                callback()
            case 'quit':
                sys.exit(1)
        

class LoginWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        """ Window for Logging in. """
        super().__init__(*args, **kwargs)

        # Login window
        self.set_title(lang.oauth.title)
        self.set_default_size(300, 500)
        self.view = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 15
        )
        self.view.set_size_request(200, 300)

        ## Titlebar
        self.header = Adw.HeaderBar.new()
        self.view.append(self.header)

        ## Instructions
        self.instruct_1 = Gtk.Label.new(lang.oauth.instructions_1)
        self.instruct_1.set_size_request(200, 10)
        self.instruct_1.set_wrap(True)
        self.view.append(self.instruct_1)
        
        ## Button
        self.button = Gtk.Button.new_with_label(lang.oauth.login)
        self.button.set_margin_top(15)
        self.button.set_margin_end(20)
        self.button.set_margin_start(20)
        self.button.connect("clicked", self.open_uri)
        self.view.append(self.button)
        
        ## Instructions 2
        self.instruct_2 = Gtk.Label.new(lang.oauth.instructions_2)
        self.instruct_2.set_margin_top(10)
        self.instruct_2.set_margin_end(15)
        self.instruct_2.set_margin_start(15)
        self.instruct_2.set_size_request(150, 25)
        self.instruct_2.set_wrap(True)
        self.view.append(self.instruct_2)

        ## GroupMe Logo (for complying with their brand guidelines)
        self.corpo_greed = Gtk.Image.new_from_file('/app/assets/groupme-dark.png')
        self.corpo_greed.set_size_request(350, 175)
        self.view.append(self.corpo_greed)

        # Set Content
        self.set_content(self.view)
    
    def open_uri(self, button):
        """ Opens OAuth uri in Browser and closes the app.
        It will be reopened with a `groupings:login` uri where it can start the OAuth flow. """
        webbrowser.open_new(oauth.GROUPME_OAUTH_URI)
        logging.info('Sent user to OAuth URI.')
        logging.info('Exiting...')
        sys.exit(0)

class FailWindow(Adw.ApplicationWindow):
    def __init__(self, *args, error = None, **kwargs):
        """ Window for when Client Fails to log in. 
        Very similar to LoginWindow, except this is displayed when the user has already tried to login, but it has failed. """
        super().__init__(*args, **kwargs)

        # Login window
        self.set_title(lang.oauth.failed.title)
        self.set_default_size(300, 500)
        self.view = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 15
        )
        self.view.set_size_request(200, 300)

        ## Titlebar
        self.header = Adw.HeaderBar.new()
        self.view.append(self.header)

        ## Instructions
        self.instruct_1 = Gtk.Label.new(lang.oauth.failed.info + f" Error: {error}")
        self.instruct_1.set_size_request(200, 10)
        self.instruct_1.set_wrap(True)
        self.view.append(self.instruct_1)
        
        ## Button
        self.button = Gtk.Button.new_with_label(lang.oauth.failed.retry)
        self.button.set_margin_top(15)
        self.button.set_margin_end(20)
        self.button.set_margin_start(20)
        self.button.connect("clicked", self.open_uri)
        self.view.append(self.button)
        
        ## Instructions 2
        self.instruct_2 = Gtk.Label.new(lang.oauth.instructions_2)
        self.instruct_2.set_margin_top(10)
        self.instruct_2.set_margin_end(15)
        self.instruct_2.set_margin_start(15)
        self.instruct_2.set_size_request(150, 25)
        self.instruct_2.set_wrap(True)
        self.view.append(self.instruct_2)

        ## GroupMe Logo (for complying with their brand guidelines)
        self.corpo_greed = Gtk.Image.new_from_file('/app/assets/groupme-dark.png')
        self.corpo_greed.set_size_request(350, 175)
        self.view.append(self.corpo_greed)

        # Set Content
        self.set_content(self.view)
    
    def open_uri(self, button):
        """ Opens OAuth uri in Browser and closes the app.
        It will be reopened with a `groupings:login` uri where it can start the OAuth flow. """
        webbrowser.open_new(oauth.GROUPME_OAUTH_URI)
        logging.info('Sent user to OAuth URI, after previous login attempt failed.')
        logging.info('Exiting...')
        sys.exit(0)


class MainApp(Adw.Application):
    def __init__(self, *args, 
        logged_in: bool = False, 
        token = None, 
        login_failed: bool = False, 
        login_error = None, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.connect('activate', self.on_activate)
        self.logged_in = logged_in
        self.login_failed = login_failed
        self.login_error = login_error
        self.token = token
    
    def on_activate(self, app):
        if self.logged_in and self.token != None:
            self.win = MainWindow(application=app, token = self.token)
        elif self.login_failed:
            self.win = FailWindow(application=app, error = self.login_error)
        else:
            self.win = LoginWindow(application=app)
        self.win.present()
        self.win.init_load()

def run(id: str, *args, logged_in: bool = False, token = None, login_failed: bool = False, login_error = None, run_push: bool = False, **kwargs):
    logging.debug("Starting UI")
    app = MainApp(
        application_id=id, 
        logged_in=logged_in, 
        token=token, 
        login_failed=login_failed, 
        login_error=login_error
    )
    if run_push:
        p = push.start_daemon(app)
    app.run(*args, **kwargs)
    if run_push:
        p.terminate()
