import sys
import gi
from gi.repository import Gtk, Gio, GLib, Adw

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from grouppy import GroupMeClient, GroupMeListener

class GroupMeChatWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="GroupMe Chat")
        self.set_default_size(600, 400)

        # Create a GroupMe client instance
        self.client = GroupMeClient()
        self.client.login(client_id='YOUR_CLIENT_ID', redirect_uri='http://localhost')

        # Create a list box to display the groups
        self.groups_list = Gtk.ListBox()
        self.groups_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.groups_list.set_margin_top(12)
        self.groups_list.set_margin_bottom(12)
        self.groups_list.set_margin_start(12)
        self.groups_list.set_margin_end(12)

        # Populate the list box with the groups
        self.populate_groups_list()

        # Create a text view to display the messages
        self.messages_view = Gtk.TextView()
        self.messages_view.set_editable(False)
        self.messages_view.set_cursor_visible(False)
        self.messages_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.messages_view.set_margin_top(12)
        self.messages_view.set_margin_bottom(12)
        self.messages_view.set_margin_start(12)
        self.messages_view.set_margin_end(12)

        # Create a text entry to send messages
        self.send_entry = Gtk.Entry()
        self.send_entry.set_placeholder_text("Type your message...")
        self.send_entry.set_margin_top(12)
        self.send_entry.set_margin_bottom(12)
        self.send_entry.set_margin_start(12)
        self.send_entry.set_margin_end(12)

        # Create a button to send messages
        self.send_button = Gtk.Button.new_from_icon_name("mail-send-symbolic", Gtk.IconSize.BUTTON)
        self.send_button.set_margin_top(12)
        self.send_button.set_margin_bottom(12)
        self.send_button.set_margin_end(12)
        self.send_button.set_sensitive(False)
        self.send_button.connect("clicked", self.send_message)

        # Create a grid to arrange the widgets
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(12)
        self.grid.set_row_spacing(12)
        self.grid.attach(self.groups_list, 0, 0, 1, 3)
        self.grid.attach(self.messages_view, 1, 0, 1, 2)
        self.grid.attach(self.send_entry, 1, 2, 1, 1)
        self.grid.attach(self.send_button, 2, 2, 1, 1)

        # Set the grid as the window's main widget
        self.set_child(self.grid)

        # Connect to the "row-selected" signal of the groups list box
        self.groups_list.connect("row-selected", self.fetch_messages)

        # Connect to the "changed" signal of the send entry
        self.send_entry.connect("changed", self.update_send_button)

    def populate_groups_list(self):
        # Fetch the list of groups from the GroupMe client
        groups = self.client.get_groups()

        # Add each group to the list box
        for group in groups:
            row = Gtk.ListBox
            row = Gtk.ListBoxRow()
            row.set_activatable(True)
            row.set_selectable(True)
            row.set_margin_top(6)
            row.set_margin_bottom(6)
            row.set_margin_start(6)
            row.set_margin_end(6)
            label = Gtk.Label()
            label.set_markup(f"<b>{group['name']}</b>")
            row.add(label)
            self.groups_list.add(row)

    def fetch_messages(self, listbox, row):
        # Fetch the messages for the selected group
        group_id = row.get_index()

class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = App(application_id="com.github.thekrafter.Groupings")
app.run(sys.argv)