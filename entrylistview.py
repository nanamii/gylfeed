#!usr/bin/env python3
# encoding:utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, Gdk
from view import View

class EntryRow(Gtk.ListBoxRow):
    def __init__(self, logo, title, time, plot, id, feed, feed_name):

        self._plot = plot
        self._time = time
        self._title = title
        self._id = id
        self._feed = feed

        Gtk.ListBoxRow.__init__(self)

        self.container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        headline_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        #if self._feed.has_icon == True:
         #   logo = self._feed.icon

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.HYPER)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        headline_text = GLib.markup_escape_text(self._title, -1)
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

        self.container_box.add(headline_box)
        self.container_box.add(feed_name_box)
        self.container_box.add(time_box)
        self.add(self.container_box)


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


class EntryListView(View):
    def __init__(self, app):
        View.__init__(self, app)
        self.app_window.feedview.listbox.connect('row-activated', self.show_entries)
        self.app_window.feedhandler.connect("feed-updated", self.update_entryview)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

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
                    row.container_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))

    def on_view_enter(self):
        # hier auf None prüfen, wenn von details-Seite aus aufgerufen,
        # nichts an feed_name ändern
        selected_row = self.app_window.feedview.listbox.get_selected_row()
        if selected_row is not None:
            self.app_window.set_title("{feed_name}".format(
                feed_name=selected_row.get_feed().get_name())
            )

    # callback-function um feedentries darzustellen, nach update; Hilfsfunktion
    # für show_entries
    def update_entryview(self, feedhandler, feed):
        self.clear_listbox()
        entries = feed.get_entries()
        print(len(entries))
        feed_name = feed.get_name()
        for title,plot,time,id,feed in entries:
            self.new_ListBoxRow("./graphics/default_icon.png", title, time, plot, id, feed, feed_name)

    # i.O. callback-function für listbox in feedview, Row=feed gewählt
    def show_entries(self, listbox, row):
        selected_row = listbox.get_selected_row()
        selected_row.get_feed().update()
        self.app_window.views.switch("entrylist")
        self.listbox.select_row(self.listbox.get_row_at_index(0))



