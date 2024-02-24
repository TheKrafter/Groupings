# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from typing import Optional, Any

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
#gi.require_version('Gdk', '4')
#gi.require_version('GdkPixbuf', '2')
from gi.repository import Gtk, Adw, Gdk, GdkPixbuf


from groupy.client import Client
import groupy.exceptions

from groupy import Client

from ..lang import lang
from .. import oauth, push

from . import login

from .widgets.list_items import GroupListItem, MessageListItem

class ProfileDetailsDialog:
    def __init__(self, user):
        self.dialog = Adw.MessageDialog.new(user.nickname, )

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, application=None, token = None, **kwargs):
        """ The Main Window is constructed here. """
        super().__init__(*args, application=application, **kwargs)
        self.token = token
        self.app = application
        self.client = Client.from_token(self.token)
        self.groups = {}

        self.set_title(lang.title)
        self.set_default_size(850, 500) # Width x Height
        self.set_size_request(300, 500)

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
        self.chat_scrolledwindow = Gtk.ScrolledWindow.new()
        self.chat_scrolledwindow.set_policy(
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC
        )
        self.chat_viewport = Gtk.Viewport.new()
        self.chat_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.chat_list.set_hexpand(True)
        self.chat_list.set_vexpand(True)
        self.chat_top_spacing = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.chat_top_spacing.set_vexpand(True)
        self.chat_list.append(self.chat_top_spacing)
        self.chat_viewport.set_child(self.chat_list)
        self.chat_scrolledwindow.set_child(self.chat_viewport)
        self.chat_box.append(self.chat_scrolledwindow)

        ### Send Box
        self.send_box = Gtk.Box.new(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=4
        )
        self.send_box.set_size_request(300, 20)
        self.send_box.set_vexpand(False)
        self.send_box.set_hexpand(True)
        self.send_entry = Adw.EntryRow.new()
        self.send_entry.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        self.send_entry.set_show_apply_button(False)
        self.send_entry.set_enable_emoji_completion(True)
        self.send_entry.connect("entry-activated", self.scroll_down)
        self.send_entry.set_hexpand(True)
        self.send_button = Gtk.Button.new_from_icon_name('send-to-symbolic')
        self.send_button.connect("clicked", self.message_send_entry)
        self.send_button.set_size_request(20, 20)
        self.send_button.set_vexpand(False)
        self.send_button.set_hexpand(False)
        self.send_box.append(self.send_entry)
        self.send_box.append(self.send_button)

        self.chat_box.append(self.send_box)
        self.view.set_content(self.chat_box)

        ## Groups List
        self.groups_box = Gtk.Box.new(
            orientation = Gtk.Orientation.VERTICAL, spacing = 8
        )
        self.groups_box.set_size_request(250, 300) # Width x Height
        self.groups_header = Adw.HeaderBar.new()
        self.groups_title = Adw.WindowTitle.new(lang.groups.title, "")
        self.groups_box.append(self.groups_header)
        self.groups_scroll = Gtk.ScrolledWindow.new()
        self.groups_scroll.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC
        )
        self.groups_viewport = Gtk.Viewport.new()
        self.groups_list = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.groups_list.set_vexpand(True)
        self.groups_list.set_margin_start(8)
        self.groups_list.set_margin_end(8)
        self.groups_list.set_margin_bottom(8)
        self.groups_viewport.set_child(self.groups_list)
        self.groups_scroll.set_child(self.groups_viewport)
        self.groups_box.append(self.groups_scroll)
        
        ### Loadbox & Logout
        self.visible_group_pages = 0
        self.groups_loadbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.groups_loadbutton = Gtk.Button.new_from_icon_name('content-loading-symbolic')
        self.groups_loadbutton.connect('clicked', self.load_more_groups)
        self.groups_loadbox.append(self.groups_loadbutton)
        self.groups_logoutbutton = Gtk.Button.new_from_icon_name('system-log-out-symbolic')
        self.groups_logoutbutton.connect('clicked', self.logout)
        self.groups_loadbox.append(self.groups_logoutbutton)
        self.groups_loadbox.set_homogeneous(True)
        self.groups_loadbox.set_margin_start(16)
        self.groups_loadbox.set_margin_end(16)
        self.groups_loadbox.set_margin_bottom(16)

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
        self.typed_store = {}
        self.oldest_message = None
        self.sticky = True
    
    def init_load(self, *args, **kwargs):
        """ Loads groups, chats, etc. """
        try:
            self.client = Client.from_token(self.token)
            self.groups = {}
            #TODO: Remove children of self.groups_list
            first = None
            for group in self.client.groups.list():
                if first == None:
                    first = group.id
                self.groups[group.id] = GroupListItem(group)
                self.groups[group.id].button.connect('clicked', self.select_group, group.id)
                self.groups_list.append(self.groups[group.id].button)
            self.visible_group_pages = 1
        except groupy.exceptions.BadResponse as ex:
            self.error_dialog(ex, self.init_load())
        
        self.setup_chat_autoscroll()
        self.view.set_show_sidebar(True)
            
    
    def load_more_groups(self, button):
        """ Loads more groups when the button is pressed """
        logging.warning('LOAD_MORE_GROUPS') #TODO


    def select_group(self, button, group):
        """ Sets selected group"""
        self.typed_store[str(self.selected_group)] = self.send_entry.get_text() # Save what the user has typed
        if str(group) in self.typed_store:
            self.send_entry.set_text(self.typed_store[str(group)]) # Restore what the user has typed when in this group
            self.send_entry.set_position(-1)
        else:
            self.send_entry.set_text('')
        self.selected_group = group
        group_obj = self.client.groups.get(group)
        self.set_chat_titles(
            group_obj.name, group_obj.description
        )
        child = self.chat_list.get_first_child()
        while child != None:
            self.chat_list.remove(child)
            child = self.chat_list.get_first_child()
        
        prev = None
        self.oldest_message = None
        for message in group_obj.messages.list():
            if self.oldest_message == None:
                self.oldest_message = message.id
            msg = MessageListItem(message, prev).box
            self.chat_list.prepend(msg)
            prev = message
        
        self.sticky = True
        self.send_entry.grab_focus_without_selecting()

        self.scroll_down(override=True)
    
    def add_new_message(self, message):
        msg = MessageListItem(message).box
        self.chat_list.prepend(msg)
        self.scroll_down()
    
    def setup_chat_autoscroll(self):
        adj = self.chat_scrolledwindow.get_vadjustment()
        adj.connect("value-changed", self.set_chat_sticky)

    def set_chat_sticky(self, x: Optional[Any]):
        adj = self.chat_scrolledwindow.get_vadjustment()
        self.sticky = adj.get_value() + adj.get_page_size() >= adj.get_upper()

    def scroll_down(self, *args, override=False, **kwargs):
        """ Scrolls to bottom of self.chat_scrolledwindow"""
        #if self.sticky or override: #TODO
            ## XXX: Need to sleep to prevent segfault: <https://gitlab.gnome.org/GNOME/gtk/-/issues/5763>
        #time.sleep(0.1)
        self.chat_scrolledwindow.emit("scroll-child", Gtk.ScrollType.END, False)

    def message_send_entry(self, widget):
        """ Posts content of self.send_entry to current guild """
        text = self.send_entry.get_text()
        self.send_entry.set_text('')
        try:
            print(f"SENDING MESSAGE!\n GROUP: '{self.select_group}'") #TODO
            group = self.client.groups.get(self.selected_group) #TODO: keeps getting the wrong thing (?)
            print(f" GROUP OBJ: '{group}'") #TODO
            message = group.post(text=text)
            print(f" MESSAGE RESPONSE: '{message}'") #TODO
            self.add_new_message(message)
            self.scroll_down()
        except groupy.exceptions.BadResponse as ex:
            self.error_dialog(ex, self.message_send_entry, widget, quittable=False, retryable=False)
        except TypeError:
            self.error_dialog('Invalid Response on Message Send', self.message_send_entry, widget, quittable=False, retryable=False)

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
        """ Shows the preferences pane """

    def error_dialog(self, ex, callback, *args, quittable=True, retryable=True, **kwargs):
        """ Presents an error dialog """
        dialog = Adw.MessageDialog.new(self, lang.error.token.title, lang.error.token.description(ex))
        if retryable:
            dialog.add_response('retry', lang.error.token.choice_retry)
        if quittable:
            dialog.add_response('quit', lang.error.token.choice_quit)
            dialog.set_response_appearance('quit', Adw.ResponseAppearance.DESTRUCTIVE)
        else:
            dialog.add_response('cancel', lang.error.token.choice_cancel)
            dialog.set_response_appearance('cancel', Adw.ResponseAppearance.SUGGESTED)

        if retryable:
            dialog.set_default_response('retry')
        elif quittable:
            dialog.set_default_response('quit')
        else:
            dialog.set_default_response('cancel')

        dialog.connect('response', self.error_dialog_response, callback, *args, **kwargs)
        dialog.choose()
        dialog.response(dialog.get_close_response())

    def error_dialog_response(self, dialog, response, callback, *args, **kwargs):
        """ Handles response to error dialog """
        match response:
            case 'retry':
                callback(*args, **kwargs)
            case 'quit':
                sys.exit(1)
            case 'cancel':
                return
    
    def logout(self, button, out=False):
        if out:
            return
        else:
            token = oauth.get_token(delete=True)
            self.set_visible(False)
            win = login.LoginWindow(application=self.app)
            win.present()