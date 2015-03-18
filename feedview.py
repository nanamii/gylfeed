#!usr/bin/env python3
# encoding: utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, GObject, Gdk
from indicatorlabel import IndicatorLabel
import urllib.request
from view import View

class FeedRow(Gtk.ListBoxRow):
    def __init__(self, logo, feed):
        Gtk.ListBoxRow.__init__(self)
        self._feed = feed
        self._num_of_entries = len(feed.get_entries())
        self._num_of_new_entries = feed.get_num_of_new_entries()
        self._num_of_unread_entries = feed.get_num_of_unread()
        self._feed_name = feed.get_name()
        self.connect('state-flags-changed', self._on_state_flags_changed)

        container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        feed_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        if feed.has_icon is True:
            logo = feed.icon

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(logo)
        pixbuf = pixbuf.scale_simple(20, 20, GdkPixbuf.InterpType.HYPER)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        feed_label_text = GLib.markup_escape_text(self._feed_name, -1)
        feed_label = Gtk.Label(feed_label_text)
        feed_label.set_markup("<b>{flabel}</b>".format(flabel=feed_label_text))

        self._opt_button = Gtk.Button.new_from_icon_name('content-loading-symbolic', Gtk.IconSize.BUTTON)
        self._opt_button.set_relief(Gtk.ReliefStyle.NONE)

        feed_box.pack_start(image, False, False, 10)
        feed_box.add(feed_label)
        feed_box.pack_end(self._opt_button, False, False, 10)
        container_box.add(feed_box)


        ####################################################
        css_provider = Gtk.CssProvider()

        try:
            css_provider.load_from_path("./label_color.css")
        except IOError as e:
            print(e)

        screen = Gdk.Screen.get_default()

        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        #######################################################

        new_entries_label = IndicatorLabel(" {num_new} ★".format(num_new=self._num_of_new_entries))
        new_entries_label.set_color(IndicatorLabel.SUCCESS)
        new_entries_label.set_margin_left(35)
        new_entries_label.set_margin_right(5)
        new_entries_label.set_margin_bottom(10)

        self.indi_label = IndicatorLabel("<b> all {num_all} </b>  ∑".format(num_all=self._num_of_entries))
        self.indi_label.set_color(IndicatorLabel.THEME)
        self.indi_label.set_margin_right(5)
        self.indi_label.set_no_show_all(True)
        self.indi_label.set_margin_bottom(10)

        self.unread_label = IndicatorLabel(" unread {num_unread} ".format(num_unread=self._num_of_unread_entries))
        self.unread_label.set_color(IndicatorLabel.THEME)
        self.unread_label.set_margin_right(5)
        self.unread_label.set_no_show_all(True)
        self.unread_label.set_margin_bottom(10)

        info_box.add(new_entries_label)
        info_box.add(self.unread_label)
        info_box.add(self.indi_label)
        container_box.add(info_box)

        self.delete_button = Gtk.Button.new_from_icon_name('window-close-symbolic', Gtk.IconSize.BUTTON)
        self.delete_button.set_label("delete")
        self.delete_button.set_relief(Gtk.ReliefStyle.NONE)

        self.settings_button = Gtk.Button.new_from_icon_name('view-more-symbolic', Gtk.IconSize.BUTTON)
        self.settings_button.set_label("Settings")
        self.settings_button.set_relief(Gtk.ReliefStyle.NONE)

        self.revealer = Gtk.Revealer()
        self.revealer.set_reveal_child(False)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.pack_end(self.delete_button, False, False, 10)
        button_box.pack_end(self.settings_button, False, False, 10)
        self.revealer.add(button_box)

        container_box.add(self.revealer)
        separator = Gtk.Separator()
        container_box.add(separator)

        self.add(container_box)

    def _on_state_flags_changed(self, _, prev_state_flags):
        state_flags = self.get_state_flags()
        self.indi_label.set_visible(state_flags & (Gtk.StateFlags.PRELIGHT |
        Gtk.StateFlags.SELECTED))
        self.unread_label.set_visible(state_flags & (Gtk.StateFlags.PRELIGHT |
        Gtk.StateFlags.SELECTED))

    def get_pref_button(self):
        return self._opt_button

    def get_set_button(self):
        return self.settings_button

    def get_delete_button(self):
        return self.delete_button

    def get_feed(self):
        return self._feed

    def show_revealer(self, button):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
        else:
            self.revealer.set_reveal_child(True)


class Feedview(View):
    __gsignals__ = { 'preferences-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.GObject,)),
                    'ok-delete-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.GObject,))}

    def __init__(self, app):
        View.__init__(self, app)

        # TODO: long time todo: remove .container in favour of View.
        self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scr_window = Gtk.ScrolledWindow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.listbox = Gtk.ListBox()
        self.listbox.set_border_width(0)
        self.listbox.set_vexpand(True)
        self.box.pack_start(self.listbox, True, True, 0)
        self.scr_window.add(self.box)
        self._container.add(self.scr_window)
        self.add(self._container)

        def build_action_bar():
            self.action_bar = Gtk.ActionBar()
            self.ok_button = Gtk.Button.new_from_icon_name('dialog-ok', Gtk.IconSize.BUTTON)
            self.ok_button.set_label("Delete")
            self.ok_button.connect("clicked", self.ok_delete_clicked)
            self.ok_button.show()
            discard_button = Gtk.Button("Discard")
            discard_button.connect("clicked", self.hide_action_bar)
            discard_button.show()
            self.action_bar.pack_start(self.ok_button)
            self.action_bar.pack_start(discard_button)
            self.action_bar.set_no_show_all(True)
            return self.action_bar

        self.action_bar = build_action_bar()
        self._container.add(self.action_bar)

        # row, für die aktuell die ActionBar angezeigt wird
        self.temp_row = None


    def new_listbox_row(self, logo, feed):
        row = FeedRow(logo, feed)
        row.grab_focus()
        row.get_set_button().connect("clicked", self._on_options_clicked, feed)
        row.get_pref_button().connect("clicked", row.show_revealer)
        row.get_delete_button().connect("clicked", self.show_actionbar, row)
        self.listbox.add(row)

    def _on_options_clicked(self, button, feed):
        self.emit('preferences-clicked', feed)

    def show_actionbar(self, button, row):
        self.action_bar.show()
        self.temp_row = row

    def ok_delete_clicked(self, button):
        self.emit('ok-delete-clicked', self.temp_row.get_feed())

    def clear_listbox(self):
        for feed in self.listbox:
            self.listbox.remove(feed)

    def hide_action_bar(self, discard_button):
        self.action_bar.hide()

    def on_view_enter(self):
        self.app_window.set_title("{num_feeds} Feeds".format(
            num_feeds=self.app_window.feedhandler.count_feeds())
        )
        self.app_window.button_search.set_sensitive(True)
        GLib.idle_add(
            lambda: self.app_window.views.go_right.set_sensitive(False)
        )
        GLib.idle_add(
            lambda: self.app_window.views.go_left.set_sensitive(False)
        )

    def on_view_leave(self):
        self.app_window.views.go_right.set_sensitive(True)

    def show_feedview(self, feedlist):
        self.clear_listbox()
        for feed in feedlist:
            if feed.raw_feed.bozo == 0:
                self.new_listbox_row("./graphics/default_icon.png",  feed)
                self.show_all()
                self.app_window.views.switch("feedview")
        #self.feedview.listbox.set_can_focus(True)
        #self.feedview.listbox.get_row_at_index(0).set_can_focus(True)
        #self.feedview.listbox.get_row_at_index(0).grab_focus()
        #self.feedview.listbox.get_row_at_index(0).set_activatable(True)
        self.listbox.select_row(self.listbox.get_row_at_index(0))


