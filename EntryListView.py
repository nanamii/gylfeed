#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GdkPixbuf


class EntryListView():
    def __init__(self):
        self.listbox = Gtk.ListBox()

    def new_ListBoxRow_old(self, buttonlabel, entry):
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

    def new_ListBoxRow(self, logo, feed, time):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        headline = Gtk.Label(feed)
        headline.set_markup("<b>{feed}</b>".format(feed=feed))

        time = Gtk.Label(time)

        hbox1.pack_start(image, False, False, 10)
        hbox1.add(headline)
        hbox1.pack_end(time, False, False, 10)
        vbox.add(hbox1)


        open_button = Gtk.Button()
        open_button.set_label("open")
        browse_button = Gtk.Button(label = "browse")
        open_button.set_relief(Gtk.ReliefStyle.NONE)
        browse_button.set_relief(Gtk.ReliefStyle.NONE)
        hbox2.pack_start(open_button, False, False, 37)
        hbox2.add(browse_button)
        vbox.add(hbox2)

        row = Gtk.ListBoxRow()
        row.add(vbox)
        self.listbox.add(row)



