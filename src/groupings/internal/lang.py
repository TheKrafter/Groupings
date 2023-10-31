# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2023 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 

# Language File
#  All text shown in the app is taken from here
#  in hopes to make translation easier in the future.

class Recursion:
    def __init__(self):
        pass

class Lang:
    def __init__(self):
        # Meta Stuff
        self.title = "Groupings"
        
        # Debugging Labels
        self.debug = Recursion()
        self.debug.messages = "Messages Go Here!"
        self.debug.input = "Input Here!"
        self.debug.groups_list = "Groups List"

        # Groups Panel
        self.groups = Recursion()
        self.groups.title = "Groups"

        # Chat Box
        self.chat = Recursion()
        self.chat.title_start = "Chat"
        self.chat.subtitle_start = "Select a Group"

        # OAuth Flow
        self.oauth = Recursion()
        self.oauth.title = "Groupings — Log In"
        self.oauth.success_message = "Success!"
        self.oauth.safe_to_close = "You may now safely close this window."



lang = Lang()