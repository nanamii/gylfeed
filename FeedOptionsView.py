#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk


class FeedOptionsView():

    def __init__(self):
        self.grid = Gtk.Grid()

        url_label = Gtk.Label("Feed-URL:")
        url_entry = Gtk.Entry()

        naming_label = Gtk.Label("Set a feed name, if you want:")
        naming_entry = Gtk.Entry()

        auto_label = Gtk.Label("Update feed automatic")
        auto_switch = Gtk.Switch()

        news_label = Gtk.Label("Show only new feed-entries")
        news_switch = Gtk.Switch()

        self.grid.set_column_spacing(30)
        self.grid.set_row_spacing(20)
        self.grid.attach(url_label, 0, 1, 2, 1)

        self.grid.insert_row(2)
        self.grid.attach_next_to(url_entry,url_label,Gtk.PositionType.RIGHT, 4, 1)
        self.grid.attach(naming_label, 0, 2, 2, 1)
        self.grid.attach_next_to(naming_entry, naming_label, Gtk.PositionType.RIGHT, 6, 1)

        self.grid.insert_row(3)
        self.grid.attach(auto_label,0, 3, 2, 1 )
        self.grid.attach_next_to(auto_switch, auto_label, Gtk.PositionType.RIGHT, 1,1)

        self.grid.attach(news_label, 0, 4, 2, 1)
        self.grid.attach_next_to(news_switch, news_label, Gtk.PositionType.RIGHT, 1,1)
