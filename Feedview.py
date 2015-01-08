#!usr/bin/env python3
# encoding: utf8

from gi.repository import Gtk, Gio, GdkPixbuf


class Feedview():
    def __init__(self, mainview):
        self.container = Gtk.ScrolledWindow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.listbox = Gtk.ListBox()
        self.box.pack_start(self.listbox, True, True, 10)
        self.container.add(self.box)

    def new_ListBoxRow_Box(self, logo, buttonlabel, feed, new_entries):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        label = Gtk.Label(feed)
        label.set_markup("<b>{feed}</b>".format(feed=feed))
        opt_button = Gtk.Button.new_from_icon_name('view-more-symbolic', Gtk.IconSize.BUTTON)
        opt_button.set_relief(Gtk.ReliefStyle.NONE)
        hbox1.pack_start(image, False, False, 10)
        hbox1.add(label)
        hbox1.pack_end(opt_button, False, False, 10)
        vbox.add(hbox1)

        new_entries_label = Gtk.Label(new_entries)
        hbox2.pack_start(new_entries_label, False, False, 37)
        vbox.add(hbox2)

        row = Gtk.ListBoxRow()
        row.add(vbox)
        self.listbox.add(row)














