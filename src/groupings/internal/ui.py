# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging
import webbrowser
import sys
import time
from typing import Optional, Any

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from .components import login, client
from . import push


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
        main = False
        if self.logged_in and self.token != None:
            self.win = client.MainWindow(application=app, token = self.token)
            main = True
        elif self.login_failed:
            self.win = login.FailWindow(application=app, error = self.login_error)
        else:
            self.win = login.LoginWindow(application=app)
        self.win.present()
        if main:
            self.win.init_load()
            self.push = push.start_daemon(app)

def run(id: str, *args, logged_in: bool = False, token = None, login_failed: bool = False, login_error = None, run_push: bool = False, **kwargs):
    logging.debug("Starting UI")
    app = MainApp(
        application_id=id, 
        logged_in=logged_in, 
        token=token, 
        login_failed=login_failed, 
        login_error=login_error
    )
    if app.register():
        logging.debug('Succesfully registered application.')
    else:
        logging.warning('Application not registered successfully.')
    app.run(*args, **kwargs)
    if run_push:
        try:
            app.push.terminate()
        except AttributeError:
            pass
