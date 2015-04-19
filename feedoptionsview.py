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
        self.change_mode = False
        self.current_feed = None
        self.button_apply_changes = None
        self.button_discard = None
        self.button_suggest = None

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

        naming_label = Gtk.Label("Set a Feed name:")
        self.naming_entry = Gtk.Entry()
        self.naming_entry.set_width_chars(40)
        self.naming_entry.set_placeholder_text("Type in the name for Feed ...")
        name_listbox_row = build_listbox_row(naming_label, self.naming_entry)

        update_label = Gtk.Label("Update feed automatic")
        self.update_switch = Gtk.Switch()
        self.update_switch.set_active(True)
        self.update_switch.connect('notify::active', self.set_update_spin_state)
        update_listbox_row = build_listbox_row(update_label, self.update_switch)

        update_interval_label = Gtk.Label("Choose update-interval, in minutes")
        self.update_spin = Gtk.SpinButton()
        adjust_interval = Gtk.Adjustment(0, 1, 120, 1, 0, 0)
        self.update_spin.set_adjustment(adjust_interval)
        self.update_spin.set_value(10) # default update-intervall
        update_interval_listbox_row = build_listbox_row(update_interval_label, self.update_spin)

        delete_label = Gtk.Label("Days, after messages will be deleted")
        self.delete_spin = Gtk.SpinButton()
        adjust_delete = Gtk.Adjustment(0, 1, 360, 1, 10, 0)
        self.delete_spin.set_adjustment(adjust_delete)
        self.delete_spin.set_value(30) # default delete-value
        delete_listbox_row = build_listbox_row(delete_label, self.delete_spin)

        notify_label = Gtk.Label("Enable system-notifications")
        self.notify_switch = Gtk.Switch()
        self.notify_switch.set_active(True)
        notify_listbox_row = build_listbox_row(notify_label, self.notify_switch)

        listbox_entries.add(url_listbox_row)
        listbox_entries.add(build_separator_row())
        listbox_entries.add(name_listbox_row)
        listbox_options.add(update_listbox_row)
        listbox_options.add(build_separator_row())
        listbox_options.add(update_interval_listbox_row)
        listbox_options.add(build_separator_row())
        listbox_options.add(delete_listbox_row)
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

    def get_update_interval(self):
        return self.update_spin.get_value()

    def get_delete_interval(self):
        return self.delete_spin.get_value()

    def set_uswitch_state(self, state):
        self.update_switch.set_active(state)

    def set_nswitch_state(self, state):
        self.notify_switch.set_active(state)

    def set_update_interval(self, interval):
        self.update_spin.set_value(interval)

    def set_delete_interval(self, interval):
        self.delete_spin.set_value(interval)

    def set_change_mode(self, change):
        self.change_mode = change

    def set_current_feed(self, feed):
        self.current_feed = feed

    def empty_form(self):
        self.url_entry.set_text("")
        self.naming_entry.set_text("")

    def set_update_spin_state(self, update_switcher, _):
        if update_switcher.get_state():
            self.update_spin.set_sensitive(False)
        else:
            self.update_spin.set_sensitive(True)

    def on_view_enter(self):
        self.app_window.set_title("Feed Options")
        self.app_window.button_search.set_sensitive(False)

        self.button_apply_changes = Gtk.Button("Apply Changes")
        self.button_apply_changes.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        self.button_suggest = Gtk.Button("Add Feed")
        self.button_suggest.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        self.button_discard = Gtk.Button("Discard")
        self.button_discard.get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)

        self.button_suggest.connect("clicked", self.app_window.set_feedview)
        self.button_discard.connect("clicked", self.app_window.discard_action)
        self.button_apply_changes.connect("clicked", self.change_data)

        self.app_window.add_widget_to_headerbar(self.button_discard, "start")
        self.button_discard.show()

        if self.change_mode is True:
            self.app_window.add_widget_to_headerbar(self.button_apply_changes, "end")
            self.button_apply_changes.show()
            self.naming_entry.set_editable(False)
            self.url_entry.set_editable(False)
        else:
            self.app_window.add_widget_to_headerbar(self.button_suggest, "end")
            self.button_suggest.show()

    def on_view_leave(self):
        if self.button_suggest and self.button_apply_changes and self.button_discard:
            self.app_window.remove_widget_from_headerbar(self.button_suggest)
            self.app_window.remove_widget_from_headerbar(self.button_apply_changes)
            self.app_window.remove_widget_from_headerbar(self.button_discard)
        self.change_mode = False
        self.naming_entry.set_editable(True)
        self.url_entry.set_editable(True)

    # callback_function für button_apply_changes; zum Ändern der settings im feed
    def change_data(self, button):
        feed_to_change = self.current_feed
        feed_to_change.automatic_update = self.get_uswitch_state()
        feed_to_change.notifications = self.get_nswitch_state()
        feed_to_change.update_interval = self.get_update_interval()
        feed_to_change.add_updater(self.get_update_interval())
        feed_to_change.delete_interval = self.get_delete_interval()

        self.app_window.views.switch("feedview")
        self.app_window.infobar.hide()
        self.empty_form()
        self.app.fh.save_to_disk()

    # i.O. call-back-function für feed-optionen-gewählt
    def show_options_filled(self, feedview, feed):
        self.set_change_mode(True)
        self.set_current_feed(feed)
        self.app_window.views.switch("feedoptions")
        self.set_url(feed.get_url())
        self.set_name(feed.get_name())
        self.set_uswitch_state(feed.automatic_update)
        self.set_nswitch_state(feed.notifications)
        self.set_update_interval(feed.update_interval)
        self.set_delete_interval(feed.delete_interval)

    def exception_handling(self, feedhandler, exception):
        self.app_window.infobar_label.set_text(exception)
        self.app_window.infobar_label.show()
        self.app_window.infobar.show()
