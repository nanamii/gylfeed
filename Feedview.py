#!usr/bin/env python3
# encoding: utf8

from gi.repository import Gtk, Gio, GdkPixbuf


class Feedview():
    def __init__(self, mainview):
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        update_button = Gtk.Button.new_from_icon_name('view-refresh-symbolic', Gtk.IconSize.BUTTON)


        new_feed_button = Gtk.Button.new_from_icon_name('list-add', Gtk.IconSize.BUTTON)
        new_feed_button.connect("clicked", self.show_feed_options, mainview)

        self.listbox = Gtk.ListBox()

        #self.box.pack_start(view, True, True, 10)
        self.top_box.pack_end(new_feed_button, False, False, 15)
        self.top_box.pack_start(update_button, False, False, 15)
        self.box.pack_end(self.listbox, True, True, 20)
        self.box.pack_start(self.top_box, False, False, 10)

    def new_ListBoxRow(self, buttonlabel, entry):
        grid = Gtk.Grid()
        row = Gtk.ListBoxRow()
        row.add(grid)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('logo_sz.png')
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        grid.add(image)
        label = Gtk.Label(entry)
        grid.attach(label, 2, 0, 6, 1)
        opt_button = Gtk.Button("options")
        grid.attach(opt_button, 3,1 , 1, 2)
        self.listbox.add(row)

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

    def show_feed_options(self, new_feed_button, mainview):
        mainview.stack.set_visible_child(mainview.feed_options.grid)













