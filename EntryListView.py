#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GdkPixbuf


class EntryListView():
    def __init__(self):
        self.listbox = Gtk.ListBox()

    def new_ListBoxRow(self, buttonlabel, entry):
        grid = Gtk.Grid()
        row = Gtk.ListBoxRow()
        row.add(grid)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('logo_sz.png')
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        grid.add(image)
        label = Gtk.Label(entry)
        grid.attach(label, 2, 0, 2, 1)
        self.listbox.add(row)


