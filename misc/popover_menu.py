#!/usr/bin/env python
# encoding: utf-8

from gi.repository import Gtk, Gio
import sys


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to Gylfeed", application=app)
        self.set_default_size(400, 250)

        def create_item(name, action, icon):
            item = Gio.MenuItem.new(name, action)
            item.set_icon(Gio.ThemedIcon.new(icon))
            return item

        button = Gtk.Button('Popover')
        button.set_border_width(30)
        button.set_valign(Gtk.Align.START)

        menu = Gio.Menu()
        menu.append_item(create_item('Speichern', 'app.save', 'document-save'))
        menu.append_item(create_item('Feed hinzufÃ¼gen', 'app.add', 'add'))
        menu.append_item(create_item('Feedupdate', 'app.update', 'application-rss+xml'))
        menu.append_item(create_item('Beenden', 'app.quit', 'window-close'))

        popover = Gtk.Popover.new_from_model(button, menu)
        popover.set_position(Gtk.PositionType.BOTTOM)
        button.connect('clicked', lambda _: popover.show_all())
        self.add(button)


class MainApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id='org.test.gylfeed',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_activate(self):
        self.win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        def create_action(name):
            action = Gio.SimpleAction.new(name, None)
            action.connect('activate', self.action_clicked)
            return action

        self.add_action(create_action("add"))
        self.add_action(create_action("update"))
        self.add_action(create_action("quit"))
        self.add_action(create_action("save"))

        self.win = MainWindow(self)
        self.win.show_all()

    def action_clicked(self, *args):
        print(args)


sys.exit(MainApplication().run(sys.argv))
