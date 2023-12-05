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
gi.require_version('Notify', '0.7')

from gi.repository import Notify

def notify(message):
    """ Send a notification based on a message """
    client = Client.from_token(get_token())
    title = f'{message["name"]} ({client.groups.get(message["group_id"]).name})'
    notif = Notify.Notification.new(
        title,
        message["text"],
        'xyz.krafterdev.Groupings-symbolic'
    )
    print(f'NOTIFICATION: {title}:\nNOTIFICATION:    {message["text"]}')
    notif.show()
    

def daemon(token: str):
    """ Notification Daemon """

    client = PushClient(access_token=token, on_message=notify)
    client.start()


def start_daemon():
    """ Start Notification Daemon """
    if not Notify.is_initted():
        Notify.init(lang.title)
    token = get_token()
    p = Process(target=daemon, args=(token,))
    p.start()
    return p
    


