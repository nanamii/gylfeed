#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk

class AddFeedWindow(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add new Feed", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Please type in your new Feed-URL")
        entry = Gtk.Entry()

        box = self.get_content_area()
        box.add(label)
        box.add(entry)
        self.show_all()

