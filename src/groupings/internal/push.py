# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
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

def notify(message):
    """ Send a notification based on a message """
    client = Client.from_token(get_token())
    title = f'{message["name"]} ({client.groups.get(message["group_id"]).name})'
    notif = Gio.Notification.new(title)
    notif.set_body(message["text"])
    notif.set_category("im.recieved")
    notif.set_priority(Gio.NOtificationPriority.HIGH)
    notif.set_icon('xyz.krafterdev.Groupings-symbolic')
    print(f'NOTIFICATION: {title}:\nNOTIFICATION:    {message["text"]}')
    notif.show()
    

def daemon(token: str):
    """ Notification Daemon """

    client = PushClient(access_token=token, on_message=notify)
    client.start()


def start_daemon():
    """ Start Notification Daemon """
    token = get_token()
    p = Process(target=daemon, args=(token,))
    p.start()
    return p
    


