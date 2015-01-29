#!usr/bin/env python3
# encoding:utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf

class EntryRow(Gtk.ListBoxRow):
    def __init__(self, logo, feed, time, plot, feed_name):
        self._plot = plot
        self._time = time
        self._feed = feed

        Gtk.ListBoxRow.__init__(self)

        container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        headline_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        headline_text = GLib.markup_escape_text(feed, -1)
        headline = Gtk.Label(headline_text)
        headline.set_markup("<b>{htext}</b>".format(htext=headline_text))
        headline_box.pack_start(image, False, False, 10)
        headline_box.add(headline)

        feed_name = Gtk.Label(feed_name)
        feed_name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        feed_name_box.pack_start(feed_name, False, False, 35)

        time = Gtk.Label(self._time)
        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_box.pack_start(time, False, False, 35)

        container_box.add(headline_box)
        container_box.add(feed_name_box)
        container_box.add(time_box)
        self.add(container_box)


    def get_plot(self):
        return self._plot

    def get_feed(self):
        return self._feed

    def get_time(self):
        return self._time


class EntryListView():
    def __init__(self):
        self.container = Gtk.ScrolledWindow()
        self.listbox = Gtk.ListBox()
        self.container.add(self.listbox)

    def new_ListBoxRow(self, logo, feed, time, entry, feed_name="FeedName"):
        row = EntryRow(logo, feed, time, entry, feed_name)
        row.set_margin_top(10)
        row.set_margin_bottom(10)
        self.listbox.add(row)
        row.show_all()

    def clear_listbox(self):
        for entry in self.listbox:
            self.listbox.remove(entry)

    def get_listbox(self):
        return self.listbox



