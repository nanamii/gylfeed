#!usr/bin/env python3
# encoding:utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, Gdk

class EntryRow(Gtk.ListBoxRow):
    def __init__(self, logo, title, time, plot, id, feed, feed_name):
        self._plot = plot
        self._time = time
        self._title = title
        self._id = id
        self._feed = feed

        Gtk.ListBoxRow.__init__(self)

        container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.headline_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        headline_text = GLib.markup_escape_text(self._title, -1)
        headline = Gtk.Label(headline_text)
        headline.set_markup("<b>{htext}</b>".format(htext=headline_text))
        self.headline_box.pack_start(image, False, False, 10)
        self.headline_box.add(headline)

        feed_name = Gtk.Label(feed_name)
        feed_name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        feed_name_box.pack_start(feed_name, False, False, 35)

        time = Gtk.Label(self._time)
        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_box.pack_start(time, False, False, 35)

        container_box.add(self.headline_box)
        container_box.add(feed_name_box)
        container_box.add(time_box)
        self.add(container_box)


    def get_plot(self):
        return self._plot

    def get_title(self):
        return self._title

    def get_time(self):
        return self._time

    def get_id(self):
        return self._id

    def get_feed(self):
        return self._feed


class EntryListView():
    def __init__(self):
        self.container = Gtk.ScrolledWindow()
        self.listbox = Gtk.ListBox()
        self.container.add(self.listbox)

    def new_ListBoxRow(self, logo, title, time, plot, id, feed, feed_name="FeedName"):
        row = EntryRow(logo, title, time, plot, id, feed, feed_name)
        row.set_margin_top(10)
        row.set_margin_bottom(10)
        self.mark_read_entries(feed, row, id)
        self.listbox.add(row)
        row.show_all()

    def clear_listbox(self):
        for entry in self.listbox:
            self.listbox.remove(entry)

    def get_listbox(self):
        return self.listbox

    def mark_read_entries(self, feed, row, id):
        for entry in feed.raw_feed.entries:
            if id == entry.id:
                if entry.read == True:
                    print(entry.read)
                    print([entry['read'] for entry in feed.raw_feed.entries])
                    row.headline_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))



