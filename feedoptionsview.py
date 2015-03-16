#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, GObject
from feed import Feed
from view import View


class FeedOptionsView(View):
    __gsignals__ = { 'feed-options': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (str,str,int))}

    def __init__(self, app):
        View.__init__(self, app)

        self.app_window.feedhandler.connect(
            "feed-add-exception",
            self.exception_handling
        )

        listbox_entries = Gtk.ListBox()
        listbox_entries.set_selection_mode(Gtk.SelectionMode.NONE)
        frame_entries = Gtk.Frame()
        frame_entries.add(listbox_entries)
        listbox_options = Gtk.ListBox()
        listbox_options.set_selection_mode(Gtk.SelectionMode.NONE)
        frame_options = Gtk.Frame()
        frame_options.add(listbox_options)

        def build_listbox_row(start_element, end_element):
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            box.pack_start(start_element, False, False, 15)
            box.pack_end(end_element, False, False, 15)
            box.set_border_width(6)
            listbox_row = Gtk.ListBoxRow()
            listbox_row.add(box)
            return listbox_row

        def build_separator_row():
            sep = Gtk.Separator()
            listbox_row = Gtk.ListBoxRow()
            listbox_row.add(sep)
            return sep

        url_label = Gtk.Label("Feed-URL:")
        self.url_entry = Gtk.Entry()
        self.url_entry.set_width_chars(40)
        self.url_entry.set_placeholder_text("Type in the URL of Feed ...")
        url_listbox_row = build_listbox_row(url_label, self.url_entry)

        naming_label = Gtk.Label("Set a feed name:")
        self.naming_entry = Gtk.Entry()
        self.naming_entry.set_width_chars(40)
        self.naming_entry.set_placeholder_text("Type in the name for Feed. max. 10 chars")
        name_listbox_row = build_listbox_row(naming_label, self.naming_entry)

        update_label = Gtk.Label("Update feed automatic")
        self.update_switch = Gtk.Switch()
        self.update_switch.set_active(True)
        update_listbox_row = build_listbox_row(update_label, self.update_switch)

        notify_label = Gtk.Label("Enable system-notifications")
        self.notify_switch = Gtk.Switch()
        self.notify_switch.set_active(True)
        notify_listbox_row = build_listbox_row(notify_label, self.notify_switch)

        listbox_entries.add(url_listbox_row)
        listbox_entries.add(build_separator_row())
        listbox_entries.add(name_listbox_row)
        listbox_options.add(update_listbox_row)
        listbox_options.add(build_separator_row())
        listbox_options.add(notify_listbox_row)

        listbox_label_entries = Gtk.Label()
        listbox_label_entries.set_markup("<b>{dates}</b>".format(dates="Dates of Feed"))

        listbox_label_options = Gtk.Label()
        listbox_label_options.set_markup("<b>{options}</b>".format(options="More Options"))

        listbox_label_entries.set_halign(Gtk.Align.START)
        listbox_label_options.set_halign(Gtk.Align.START)
        listbox_label_entries.set_margin_bottom(15)
        listbox_label_options.set_margin_bottom(15)
        listbox_label_options.set_margin_top(30)

        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._container.add(listbox_label_entries)
        self._container.add(frame_entries)
        self._container.add(listbox_label_options)
        self._container.add(frame_options)
        self._container.set_border_width(50)
        self.add(self._container)


    def get_url(self):
        return self.url_entry.get_text()

    def get_name(self):
        return self.naming_entry.get_text()

    def set_url(self, url):
        self.url_entry.set_text(url)

    def set_name(self, name):
        self.naming_entry.set_text(name)

    def get_uswitch_state(self):
        return self.update_switch.get_active()

    def get_nswitch_state(self):
        return self.notify_switch.get_active()

    def empty_form(self):
        self.url_entry.set_text("")
        self.naming_entry.set_text("")

    def on_view_enter(self):
        self.app_window.set_title("Feed Options")
        self.app_window.button_search.set_sensitive(False)

        self.app_window.button_suggest.show()
        self.app_window.button_discard.show()

    def on_view_leave(self):
        self.app_window.button_suggest.hide()
        self.app_window.button_discard.hide()

    def exception_handling(self, feedhandler, exception):
        self.app_window.infobar_label.set_text(exception)
        self.app_window.infobar_label.show()
        self.app_window.infobar.show()
