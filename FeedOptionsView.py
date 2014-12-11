#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk


class FeedOptionsView():

    def __init__(self):
        self.grid = Gtk.Grid()

        label = Gtk.Label("Please type in your new Feed-URL")
        entry = Gtk.Entry()

        self.grid.add(label)
        self.grid.attach(entry, 1, 0, 2, 1)

