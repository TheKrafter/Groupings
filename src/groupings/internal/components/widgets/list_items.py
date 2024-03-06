# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from typing import Optional, Any

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GdkPixbuf

from ...lang import lang
from ... import oauth, cache

global_token = None

def get_token():
    """ Caches token so we don't have to ask the keyring for every widget """
    global global_token
    if global_token != None:
        return global_token
    else:
        return oauth.get_token()

class GroupListItem:
    def __init__(self, group):
        """ Widget for a Group shown in the list """
        self.box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        # Avatar
        self.avatar = Adw.Avatar(size=32, text=group.name)
        avatar_filename = cache.fetch(get_token(), group.image_url)
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
        self.label_title = Gtk.Label.new(f'<span weight="bold">{title}</span>')
        self.label_title.set_use_markup(True)
        self.label_title.set_halign(Gtk.Align.START)
        self.box_info.append(self.label_title)
        self.label_msg = Gtk.Label.new(f'<span weight="normal">{group.description[0:25].strip()}</span>')
        self.label_msg.set_use_markup(True)
        self.label_msg.set_halign(Gtk.Align.START)
        self.box_info.append(self.label_msg)
        self.box.append(self.box_info)

        self.button = Gtk.Button.new()
        self.button.set_label(group.name)
        self.button.set_child(self.box)

class MessageListItem:
    def __init__(self, message, previous: Optional[Any]):
        """ Widget for a message in list of messages """
        self.box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        # Avatar
        avatar_set = False
        self.avatar_box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing = 8)
        self.avatar_box.set_hexpand(False)
        self.avatar_box.set_vexpand(True)
        self.avatar_box.set_margin_start(8)
        if message.system:
            self.avatar = Adw.Avatar.new(24, 'GroupMe', False)
            self.avatar.set_icon_name('dialog-information-symbolic')
            self.avatar_box.append(self.avatar)
            avatar_set = True
        if not message.system:
            try:
                if previous is None:
                    if str(previous.user_id) == str(message.user_id):
                        do_avatar = False
                    else:
                        do_avatar = True
                else:
                    do_avatar = True
            except AttributeError:
                do_avatar = True
            if do_avatar:
                self.avatar = Adw.Avatar.new(24, message.name, True)
                pfp = cache.fetch(get_token(), message.avatar_url)
                if pfp != None and pfp != False:
                    self.texture_avatar = Gdk.Texture.new_for_pixbuf(
                        GdkPixbuf.Pixbuf.new_from_file(filename=pfp)
                    )
                else:
                    self.avatar.set_show_initials(True)
                self.avatar_box.append(self.avatar)
                avatar_set = True
        if not avatar_set:
            self.avatar = None
        self.spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.spacer.set_vexpand(True)
        self.spacer.set_hexpand(False)
        self.spacer.set_size_request(width=24, height=24)
        self.avatar_box.append(self.spacer)
        self.box.append(self.avatar_box)
        # Username & Message
        self.box_msg = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        if avatar_set and not message.system:
            self.label_username = Gtk.Label.new(
                f'<span weight="bold">{message.name}</span> ' +
                f'<span weight="ultralight" size="small">— {message.created_at.strftime("%a %d %b %Y, %I:%M %p")}</span>'
            )
            self.label_username.set_use_markup(True)
            self.label_username.set_halign(Gtk.Align.START)
            self.box_msg.append(self.label_username)
        if message.system:
            text = f'<span weight="light"><i>{message.text}</i></span>'
        else:
            text = f'<span weight="normal">{message.text}</span>'
        self.label_message = Gtk.Label.new(text)
        self.label_message.set_use_markup(True)
        self.label_message.set_wrap(True)
        self.label_message.set_halign(Gtk.Align.START)
        if message.system:
            self.label_message.set_valign(Gtk.Align.CENTER)
        self.box_msg.append(self.label_message)

        self.box_msg.set_hexpand(True)

        self.box.append(self.box_msg)