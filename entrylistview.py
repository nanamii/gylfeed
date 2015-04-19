#!usr/bin/env python3
# encoding:utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, Gdk
from view import View

class EntryRow(Gtk.ListBoxRow):
    def __init__(self, logo, title, time, plot, id, feed, updated_parsed, feed_name="FeedName"):
        Gtk.ListBoxRow.__init__(self)

        self.set_name("GylfeedEntryRow")

        self._plot = plot
        self._time = time
        self._title = title
        self._id = id
        self._feed = feed
        self._updated_parsed = updated_parsed

        self.container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        headline_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        if self._feed.has_icon == True:
            logo = self._feed.icon

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.HYPER)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image.set_margin_top(10)

        headline_text = GLib.markup_escape_text(self._title, -1)
        headline = Gtk.Label(headline_text)
        headline.set_markup("<b>{htext}</b>".format(htext=headline_text))
        headline_box.pack_start(image, False, False, 10)
        headline_box.add(headline)
        headline.set_margin_top(10)

        self.check_read = Gtk.Label("✓")
        self.check_read.set_no_show_all(True)
        headline_box.pack_end(self.check_read, False, False, 10)

        feed_name = Gtk.Label(feed.get_name())
        feed_name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        feed_name_box.pack_start(feed_name, False, False, 40)

        time = Gtk.Label(self._time)
        time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        time_box.pack_start(time, False, False, 40)

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

    def get_entrylink(self):
        return self._entrylink

    def get_id(self):
        return self._id

    def get_feed(self):
        return self._feed

    def get_updated_parsed(self):
        return self._updated_parsed


class EntryListView(View):
    def __init__(self, app):
        View.__init__(self, app)
        self.app_window.feedview.listbox.connect('row-activated', self.show_entries)
        self.app_window.feedhandler.connect("feed-updated", self.update_entryview)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

    def _new_listboxrow(self, logo, title, time, plot, id, feed, updated_parsed,feed_name):
        row = EntryRow(logo, title, time, plot, id, feed, updated_parsed, feed_name)
        self._mark_read_entries(feed, row, id)
        self.listbox.add(row)
        self.listbox.set_sort_func(self._sort_function)
        self.listbox.set_filter_func(self._filter_function)
        row.show_all()

    def _sort_function(self, row_1, row_2):
        if row_1.get_updated_parsed() > row_2.get_updated_parsed():
            return -1
        elif row_1.get_updated_parsed() == row_2.get_updated_parsed():
            return 0
        else:
            return 1

    def _filter_function(self, row):
        query = self.search_term.lower()
        if not query:
            return True
        return query in row.get_title().lower()

    def _on_invalidate_filter(self, searchentry):
        self.listbox.invalidate_filter()

    def clear_listbox(self):
        for entry in self.listbox:
            self.listbox.remove(entry)

    def get_listbox(self):
        return self.listbox

    def _mark_read_entries(self, feed, row, id):
        for entry in feed.raw_feed.entries:
            if id == entry.id:
                if entry.read == True:
                    row.get_style_context().add_class("read")
                    row.check_read.show()
                    # row.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,.5))

    def on_view_enter(self):
        selected_row = self.app_window.feedview.listbox.get_selected_row()
        subtitle = str(selected_row.get_feed().get_num_of_entries())+ " Entries, "+ str(selected_row.get_feed().get_num_of_unread()) + " unread"

        if selected_row is not None:
            self.app_window.set_title("{feed_name}".format(
                feed_name=selected_row.get_feed().get_name()), subtitle
                )

        GLib.idle_add(
            lambda: self.app_window.views.go_right.set_sensitive(False))

        # gelesene entries anders darstellen lassen
        for row in self.listbox:
            self._mark_read_entries(row.get_feed(), row, row.get_id())

    # callback-function um feedentries darzustellen, nach update; Hilfsfunktion
    # für show_entries
    def update_entryview(self, feedhandler=None, feed=None):
        self.clear_listbox()
        entries = feed.get_entries()
        feed_name = feed.get_name()
        for title,plot,time,id,deleted,feed,updated_parsed in entries:
            if deleted is False:
                self._new_listboxrow("./graphics/default_icon.png",
                    title, time, plot, id, feed, updated_parsed, feed_name
                    )

    # i.O. callback-function für listbox in feedview, Row=feed gewählt
    def show_entries(self, listbox, row):
        selected_row = listbox.get_selected_row()
        self.update_entryview(None, selected_row.get_feed())
        self.app_window.views.switch("entrylist")
        self.listbox.select_row(self.listbox.get_row_at_index(0))
