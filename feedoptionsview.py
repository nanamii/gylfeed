#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, GObject
from feed import Feed



class FeedOptionsView(GObject.GObject):
    __gsignals__ = { 'feed-options': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (str,str,int))}

    def __init__(self):
        GObject.GObject.__init__(self)
        self.grid = Gtk.Grid()

        url_label = Gtk.Label("Feed-URL:")
        url_label.set_alignment(5,0.5)
        self.url_entry = Gtk.Entry()

        naming_label = Gtk.Label("Set a feed name:")
        naming_label.set_alignment(5, 0.5)
        self.naming_entry = Gtk.Entry()

        auto_label = Gtk.Label("Update feed automatic")
        auto_label.set_alignment(5, 0.5)
        auto_switch = Gtk.Switch()

        notify_label = Gtk.Label("Enable sytem-notifies")
        notify_label.set_alignment(5, 0.5)
        notify_switch = Gtk.Switch()

        button_box = Gtk.Box()
        ok_button = Gtk.Button("  OK  ")
        ok_button.connect("clicked", self.set_user_input, self.url_entry, self.naming_entry)
        cancel_button = Gtk.Button(" Cancel ")
        button_box.pack_end(ok_button, False, False, 5)
        button_box.pack_end(cancel_button, False, False, 5)

        self.grid.set_border_width(20)
        self.grid.set_column_spacing(30)
        self.grid.set_row_spacing(20)
        self.grid.attach(url_label, 0, 1, 2, 1)

        self.grid.insert_row(2)
        self.grid.attach_next_to(self.url_entry,url_label,Gtk.PositionType.RIGHT, 10, 1)
        self.grid.attach(naming_label, 0, 2, 2, 1)
        self.grid.attach_next_to(self.naming_entry, naming_label, Gtk.PositionType.RIGHT, 10, 1)

        self.grid.insert_row(3)
        self.grid.attach(auto_label,0, 3, 2, 1 )
        self.grid.attach_next_to(auto_switch, auto_label, Gtk.PositionType.RIGHT, 1,1)

        self.grid.attach(notify_label, 0, 4, 2, 1)
        self.grid.attach_next_to(notify_switch, notify_label, Gtk.PositionType.RIGHT, 1,1)

        self.grid.insert_row(5)
        self.grid.attach(button_box, 0, 5, 12, 1)


    def get_url(self):
        return self.url_entry.get_text()

    def get_name(self):
        return self.naming_entry.get_text()

    def empty_form(self):
        self.url_entry.set_text("")
        self.naming_entry.set_text("")

    #call-back-function für ok-button
    def set_user_input(self, button, url_entry, naming_entry):
        self.emit('feed-options', self.get_url(), self.get_name(), 13)


