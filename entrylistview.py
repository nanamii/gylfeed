#!usr/bin/env python3
# encoding:utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf

class EntryRow(Gtk.ListBoxRow):
    def __init__(self, logo, feed, time, plot, feed_name):
        self._plot = plot
        self._time = time
        self._feed = feed

        Gtk.ListBoxRow.__init__(self)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        headline_text = GLib.markup_escape_text(feed, -1)
        headline = Gtk.Label(headline_text)
        headline.set_markup("<b>{htext}</b>".format(htext=headline_text))

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

        feed_name = Gtk.Label(feed_name)
        feed_name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        feed_name_box.pack_start(feed_name, False, False, 10)

        vbox.add(feed_name_box)
        vbox.add(hbox2)
        self.add(vbox)


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
        self.listbox.add(row)
        row.show_all()

    def clear_listbox(self):
        for entry in self.listbox:
            self.listbox.remove(entry)



