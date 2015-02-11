#!usr/bin/env python3:
#encoding: UTF8

from gi.repository import Gtk

class IndicatorLabel(Gtk.Label):
    """A label that has a rounded, colored background.

    It is mainly useful for showing new entries or indicate errors.
    There are 3 colors available, plus a color derived from the
    theme's main color. In case of Adwaita blue.
    """
    SUCCESS, WARNING, ERROR, THEME = range(1, 5)

    def __init__(self, *args):
        Gtk.Label.__init__(self, *args)
        self.set_use_markup(True)

        # Do not expand space.
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)
        self.set_vexpand(False)
        self.set_hexpand(False)

        # Use the theme's color by default.
        self.set_color(IndicatorLabel.THEME)

    def set_color(self, state):
        classes = {
            IndicatorLabel.ERROR: 'AppIndicatorLabelError',
            IndicatorLabel.SUCCESS: 'AppIndicatorLabelSuccess',
            IndicatorLabel.WARNING: 'AppIndicatorLabelWarning',
            IndicatorLabel.THEME: 'AppIndicatorLabelTheme'
        }

        # Will act as normal label for invalid states.
        # Useful for highlighting problematic input.
        self.set_name(classes.get(state, 'AppIndicatorLabelEmpty'))
