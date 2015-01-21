#!usr/bin/env python3
# encoding: utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, GObject

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


        feed_label_text = GLib.markup_escape_text(feed_name, -1)
        feed_label = Gtk.Label(feed_label_text)
        feed_label.set_markup("<b>{flabel}</b>".format(flabel=feed_label_text))

        self._opt_button = Gtk.Button.new_from_icon_name('view-more-symbolic', Gtk.IconSize.BUTTON)
        self._opt_button.set_relief(Gtk.ReliefStyle.NONE)

        delete_button = Gtk.Button.new_from_icon_name('window-close-symbolic', Gtk.IconSize.BUTTON)
        delete_button.set_relief(Gtk.ReliefStyle.NONE)

        hbox1.pack_start(image, False, False, 10)
        hbox1.add(feed_label)
        hbox1.pack_end(self._opt_button, False, False, 10)
        hbox1.pack_end(delete_button, False, False, 10)
        vbox.add(hbox1)

        new_entries_label = Gtk.Label(new_entries)
        hbox2.pack_start(new_entries_label, False, False, 37)
        vbox.add(hbox2)
        self.add(vbox)

    def get_pref_button(self):
        return self._opt_button

    def get_feed(self):
        return self._feed


class Feedview(GObject.GObject):
    __gsignals__ = { 'preferences-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.GObject,))}

    def __init__(self):
        GObject.GObject.__init__(self)
        self.container = Gtk.ScrolledWindow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.listbox = Gtk.ListBox()
        self.box.pack_start(self.listbox, True, True, 0)
        self.container.add(self.box)

    def new_listbox_row(self, logo, feed_name, new_entries, feed):
        row = FeedRow(logo, feed_name, new_entries, feed)
        row.grab_focus()
        row.get_pref_button().connect("clicked", self._on_options_clicked, feed)

        self.listbox.add(row)

    def _on_options_clicked(self, button, feed):
        self.emit('preferences-clicked', feed)













