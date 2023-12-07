# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
import logging

from .lang import lang

import gi
gi.require_version('Adw', '1')
from gi.repository import Adw

class Preferences(Adw.PreferencesWindow):
    def __init__(self, *args, **kwargs):
        """ Preferences Window """
        super().__init__(*args, **kwargs)
        self.set_search_enabled(False)

        self.page = Adw.PreferencesPage.new()
        self.page.set_title(lang.pref.title)
        self.page.set_description(lang.pref.description)

        self.add(self.page)
        self.set_visible_page(self.page)
