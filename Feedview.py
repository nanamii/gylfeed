#!usr/bin/env python3
# encoding: utf8

from gi.repository import Gtk
from AddFeedWindow import AddFeedWindow


class Feedview():
    def __init__(self):
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        liststore = Gtk.ListStore(str,str)
        treeIter = liststore.append(["A","B"])
        liststore.append(["A1","B1"])

        view = Gtk.TreeView(model = liststore)
        renderer = Gtk.CellRendererText()
        column_feed = Gtk.TreeViewColumn("Feed", renderer, text = 0)
        column_figure = Gtk.TreeViewColumn("new", renderer, text = 1)
        view.append_column(column_feed)
        view.append_column(column_figure)

        new_feed_button = Gtk.Button("add Feed")
        new_feed_button.connect("clicked", self.add_feed)

        self.box.pack_start(view, True, True, 10)
        self.box.pack_end(new_feed_button, False, False, 10)

    def add_feed(self, new_feed_button):
        add_feed_window = AddFeedWindow(self)




