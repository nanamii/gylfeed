#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, GObject


class View(Gtk.Grid):
    """Default View class that has some utility extras.
    """

    __gsignals__ = {
        'view-enter': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'view-leave': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, app, sub_title=None):
        Gtk.Grid.__init__(self)
        self._app = app
        self._sub_title = sub_title or View.sub_title.default
        self._is_visible = False

        self.connect('view-enter', self._on_view_enter)
        self.connect('view-leave', self._on_view_leave)

        self.app_window.button_search.connect('clicked', self.manage_searchbar)

        self.searchbar = Gtk.SearchBar()
        self.searchentry = Gtk.SearchEntry()
        self.searchentry.connect('search-changed', self.invalidate_filter)
        self.searchbar.connect_entry(self.searchentry)
        self.searchbar.add(self.searchentry)
        self.searchbar.set_hexpand(True)
        self.searchbar.set_search_mode(False)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.props.expand = True
        self.attach(self.searchbar, 1, 0, 1, 1)
        self.attach(self.scrolled_window, 1, 1, 1, 1)

    def add(self, widget):
        self.scrolled_window.add(widget)

    def invalidate_filter(self, searchentry):
        if hasattr(self, 'on_invalidate_filter'):
            self.on_invalidate_filter(searchentry)

    def _on_view_enter(self, _):
        self._is_visible = True
        self.searchbar.set_search_mode(False)

        if hasattr(self, 'on_view_enter'):
            self.on_view_enter()

        # Restore the sub_title.
        # self.sub_title = self._sub_title

    def _on_view_leave(self, _):
        self.searchentry.set_text("")
        self.searchbar.set_search_mode(False)
        self._is_visible = False

        if hasattr(self, 'on_view_leave'):
            self.on_view_leave()

    def manage_searchbar(self, _):
        self.searchbar.set_search_mode(
            not self.searchbar.get_search_mode()
        )

    @property
    def app_window(self):
        return self._app.win

    @property
    def app(self):
        return self._app

    @GObject.Property(type=str, default='')
    def sub_title(self):
        return self._sub_title

    @sub_title.setter
    def sub_title(self, new_sub_title):
        self.app_window.headerbar.set_subtitle(new_sub_title)
        self._sub_title = new_sub_title

    @property
    def is_visible(self):
        return self._is_visible

    @property
    def search_term(self):
        return self.searchentry.get_text()
