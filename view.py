#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, GObject


class View(Gtk.ScrolledWindow):
    """Default View class that has some utility extras.
    """

    __gsignals__ = {
        'view-enter': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'view-leave': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, app, sub_title=None):
        Gtk.ScrolledWindow.__init__(self)
        self._app = app
        self._sub_title = sub_title or View.sub_title.default
        self._is_visible = False

        self.connect('view-enter', self._on_view_enter)
        self.connect('view-leave', self._on_view_leave)

    def _on_view_enter(self, _):
        self._is_visible = True

        if hasattr(self, 'on_view_enter'):
            self.on_view_enter()

        # Restore the sub_title.
        self.sub_title = self._sub_title

    def _on_view_leave(self, _):
        self._is_visible = False
        if hasattr(self, 'on_view_leave'):
            self.on_view_leave()

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
