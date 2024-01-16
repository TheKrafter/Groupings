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
        self.id = "xyz.krafterdev.Groupings" # DO NOT TRANSLATE!
        
        # Debugging Labels
        self.debug = Recursion()
        self.debug.messages = "Messages Go Here!"
        self.debug.input = "Input Here!"
        self.debug.groups_list = "Groups List"

        # Groups Panel
        self.groups = Recursion()
        self.groups.title = "Groups"
        self.groups.load_more = '...'

        # Chat Box
        self.chat = Recursion()
        self.chat.title_start = "Chat"
        self.chat.subtitle_start = "Select a Group"

        # OAuth Flow
        self.oauth = Recursion()
        self.oauth.title = "Groupings — Log In"
        self.oauth.instructions_1 = "Click the button below to log in."
        self.oauth.instructions_2 = "Note: If you do not recieve a verification PIN number via SMS, check the email address associated with your GroupMe account."
        self.oauth.login = "Log In"
        self.oauth.secret_notes = "Token for GroupMe API, user id: "

        self.oauth.failed = Recursion()
        self.oauth.failed.title = "Groupings — Login Failed"
        self.oauth.failed.info = "Failed to log in. This could be because your token expired, GroupMe is unreachable, or there is a problem with this application."
        self.oauth.failed.retry = "Try Again"

        # Preferences
        self.pref = Recursion()
        self.pref.title = 'Preferences'
        self.pref.description = 'Nothing here yet'

        # Loading Errors
        self.error = Recursion()
        self.error.token = Recursion()
        self.error.token.title = 'Could Not Fetch Data'
        self.error.token.description = lambda error: f'Your token may be invalid, or GroupMe may be unreachable.\nError Code: {error}'
        self.error.token.choice_retry = 'Retry'
        self.error.token.choice_quit = 'Quit'


lang = Lang()
