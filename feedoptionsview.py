#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, GObject
from feed import Feed



class FeedOptionsView(GObject.GObject):
    __gsignals__ = { 'feed-options': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (str,str,int))}

    def __init__(self):
        GObject.GObject.__init__(self)

        listbox_entries = Gtk.ListBox()
        listbox_entries.set_selection_mode(Gtk.SelectionMode.NONE)
        listbox_options = Gtk.ListBox()
        listbox_options.set_selection_mode(Gtk.SelectionMode.NONE)

        def build_listbox_row(start_element, end_element):
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            box.pack_start(start_element, False, False, 15)
            box.pack_end(end_element, False, False, 15)
            box.set_border_width(6)
            listbox_row = Gtk.ListBoxRow()
            listbox_row.add(box)
            return listbox_row

        url_label = Gtk.Label("Feed-URL:")
        self.url_entry = Gtk.Entry()
        self.url_entry.set_width_chars(30)
        self.url_entry.set_placeholder_text("Type in the URL of Feed ...")
        url_listbox_row = build_listbox_row(url_label, self.url_entry)

        naming_label = Gtk.Label("Set a feed name:")
        self.naming_entry = Gtk.Entry()
        self.naming_entry.set_width_chars(30)
        name_listbox_row = build_listbox_row(naming_label, self.naming_entry)

        update_label = Gtk.Label("Update feed automatic")
        self.update_switch = Gtk.Switch()
        update_listbox_row = build_listbox_row(update_label, self.update_switch)

        notify_label = Gtk.Label("Enable system-notifications")
        self.notify_switch = Gtk.Switch()
        notify_listbox_row = build_listbox_row(notify_label, self.notify_switch)

        listbox_entries.add(url_listbox_row)
        listbox_entries.add(name_listbox_row)
        listbox_options.add(update_listbox_row)
        listbox_options.add(notify_listbox_row)
        listbox_entries.set_margin_bottom(30)

        listbox_label_entries = Gtk.Label()
        listbox_label_entries.set_markup("<b>{dates}</b>".format(dates="Dates of Feed"))

        listbox_label_options = Gtk.Label()
        listbox_label_options.set_markup("<b>{options}</b>".format(options="More Options"))

        listbox_label_entries.set_halign(Gtk.Align.START)
        listbox_label_options.set_halign(Gtk.Align.START)
        listbox_label_entries.set_margin_bottom(15)
        listbox_label_options.set_margin_bottom(15)

        self.container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.container.add(listbox_label_entries)
        self.container.add(listbox_entries)
        self.container.add(listbox_label_options)
        self.container.add(listbox_options)
        self.container.set_border_width(50)


    def get_url(self):
        return self.url_entry.get_text()

    def get_name(self):
        return self.naming_entry.get_text()

    def empty_form(self):
        self.url_entry.set_text("")
        self.naming_entry.set_text("")



