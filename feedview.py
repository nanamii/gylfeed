#!usr/bin/env python3
# encoding: utf8

from gi.repository import GLib, Gtk, Gio, GdkPixbuf, GObject, Gdk
from indicatorlabel import IndicatorLabel
import urllib.request

class FeedRow(Gtk.ListBoxRow):
    def __init__(self, logo, feed):
        self._feed = feed
        self._num_of_entries = len(feed.get_entries())
        self._num_of_new_entries = feed.get_num_of_new_entries()
        self._num_of_unread_entries = feed.get_num_of_unread()
        self._feed_name = feed.get_name()
        Gtk.ListBoxRow.__init__(self)

        container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        feed_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        try:
            if self._feed.raw_feed.feed.icon:
                url = self._feed.raw_feed.feed.icon
                print(url)
                logo_raw = urllib.request.urlretrieve(url)
                logo = logo_raw[0]
        except AttributeError as aerr:
            print(aerr)

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

        new_entries_label = IndicatorLabel(" {num_new}★".format(num_new=self._num_of_new_entries))
        new_entries_label.set_color(IndicatorLabel.THEME)
        new_label = Gtk.Label("new:")
        #info_box.pack_start(new_label, False, False, 0)

        new_entries_label.set_margin_left(35)
        new_entries_label.set_margin_right(5)

        #colored_label = Gtk.Label("21", name='colored_label')
        #colored_label.set_size_request(40,30)
        #colored_label.set_margin_left(1)
        #colored_label.set_margin_right(10)
        #info_box.pack_start(colored_label, False, False, 0)
        info_box.add(new_entries_label)

        self.indi_label = IndicatorLabel("<b>{num_all}</b> ✓".format(num_all=self._num_of_entries))
        self.indi_label.set_color(IndicatorLabel.SUCCESS)
        self.indi_label.set_margin_right(5)
        self.indi_label.set_no_show_all(True)
        info_box.add(self.indi_label)

        unread_label = IndicatorLabel(" {num_unread}".format(num_unread=self._num_of_unread_entries))
        unread_label.set_color(IndicatorLabel.WARNING)
        info_box.add(unread_label)

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

    def get_pref_button(self):
        return self._opt_button

    def get_set_button(self):
        return self.settings_button

    def get_delete_button(self):
        return self.delete_button

    def get_feed(self):
        print(self._feed)
        return self._feed

    def show_revealer(self, button):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
        else:
            self.revealer.set_reveal_child(True)


class Feedview(GObject.GObject):
    __gsignals__ = { 'preferences-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.GObject,)),
                    'ok-delete-clicked': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.GObject,))}

    def __init__(self):
        GObject.GObject.__init__(self)

        self.container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scr_window = Gtk.ScrolledWindow()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.listbox = Gtk.ListBox()
        self.listbox.set_border_width(0)
        self.listbox.set_vexpand(True)
        self.listbox.connect('row-selected', self.show_all_labels)
        self.box.pack_start(self.listbox, True, True, 0)
        self.scr_window.add(self.box)
        self.container.add(self.scr_window)

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
        self.container.add(self.action_bar)


    def new_listbox_row(self, logo, feed):
        row = FeedRow(logo, feed)
        row.grab_focus()
        row.get_set_button().connect("clicked", self._on_options_clicked, feed)
        row.get_pref_button().connect("clicked", row.show_revealer)
        row.get_delete_button().connect("clicked", self.show_actionbar)
        self.listbox.add(row)

    def _on_options_clicked(self, button, feed):
        self.emit('preferences-clicked', feed)

    def show_actionbar(self, button):
        self.action_bar.show()

    def ok_delete_clicked(self, button):
        row = self.listbox.get_selected_row()
        self.emit('ok-delete-clicked', row.get_feed())

    def clear_listbox(self):
        for feed in self.listbox:
            self.listbox.remove(feed)

    def hide_action_bar(self, discard_button):
        self.action_bar.hide()

    def show_all_labels(self, listbox, label):
        if listbox.get_selected_row().indi_label.show():
            listbox.get_selected_row().indi_label.hide()
        else:
            listbox.get_selected_row().indi_label.show()



