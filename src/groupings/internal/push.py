# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

from groupme_push.client import PushClient
from groupy import Client
from multiprocessing import Process

from .oauth import get_token

from .lang import lang

import gi
gi.require_version('Gio', '2.0')

from gi.repository import Gio

global application
application = None

def notify(title: str, body: str, id: str):
    """ Send a Notification """
    global application

    notif = Gio.Notification.new(title)
    notif.set_body(body)
    notif.set_category("im.recieved")
    notif.set_priority(Gio.NotificationPriority.HIGH)
    notif.set_icon(Gio.ThemedIcon.new('xyz.krafterdev.Groupings-symbolic'))
    print(f'NOTIFICATION: {title}:\nNOTIFICATION: > {body}')

    application.send_notification(id, notif)

def notify_message(message):
    """ Notify for Messages in Groups """
    client = Client.from_token(get_token())
    title = f'{message["name"]} ({client.groups.get(message["group_id"]).name})'

    notify(title, message["text"], message["id"])

def notify_dm(message):
    """ Notify for DMs """
    notify(message["name"], message["text"], message["id"])

def daemon(token: str, app: Gio.Application):
    """ Notification Daemon """
    global application
    application = app

    client = PushClient(
        disregard_self = False,
        access_token = token, 
        on_message = notify_message,
        on_dm = notify_dm,
    )
    client.start()


def start_daemon(app: Gio.Application):
    """ Start Notification Daemon """
    token = get_token()
    p = Process(target=daemon, args=(token, app,))
    p.start()
    return p
    


