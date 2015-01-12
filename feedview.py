#!usr/bin/env python3
# encoding: utf8

from gi.repository import Gtk, Gio, GdkPixbuf

class FeedRow(Gtk.ListBoxRow):
    def __init__(self, logo, feed_name, new_entries, feed):
        self._feed = feed
        Gtk.ListBoxRow.__init__(self)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        label = Gtk.Label(feed)
        label.set_markup("<b>{feed_name}</b>".format(feed_name=feed_name))
        opt_button = Gtk.Button.new_from_icon_name('view-more-symbolic', Gtk.IconSize.BUTTON)
        opt_button.set_relief(Gtk.ReliefStyle.NONE)
        hbox1.pack_start(image, False, False, 10)
        hbox1.add(label)
        hbox1.pack_end(opt_button, False, False, 10)
        vbox.add(hbox1)

        new_entries_label = Gtk.Label(new_entries)
        hbox2.pack_start(new_entries_label, False, False, 37)
        vbox.add(hbox2)
        self.add(vbox)


    def get_feed(self):
        return self._feed


class Feedview():
    def __init__(self, mainview):
        self.container = Gtk.ScrolledWindow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.listbox = Gtk.ListBox()
        self.box.pack_start(self.listbox, True, True, 10)
        self.container.add(self.box)

    def new_listbox_row(self, logo, feed_name, new_entries, feed):
        row = FeedRow(logo, feed_name, new_entries, feed)
        self.listbox.add(row)













