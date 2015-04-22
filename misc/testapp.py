from gi.repository import Gtk, Gio

class TestApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id='org.test.app',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_startup(self):
        # create a window with a button in the corner with space for a popover
        Gtk.Application.do_startup(self)
        self.win = Gtk.ApplicationWindow(application=self, title='Test')
        self.win.set_default_size(800, 480)
        grid = Gtk.Grid()
        button = Gtk.Button(label='Click Me')
        button.connect('clicked', self.on_button_clicked)
        grid.add(button)
        grid.show_all()
        self.win.add(grid)

        menu = Gio.Menu()
        self.popover = Gtk.Popover.new_from_model(button, menu)

        # Add 4 items to the menu. Each of them will use the same action
        # but from a different action group.

        # 1. the app action group. works fine.
        test_action = Gio.SimpleAction.new('test-action', None)
        self.add_action(test_action)
        menu.append("App Action", 'app.test-action')

        # 2. the win action group. works fine
        self.win.add_action(test_action)
        menu.append('Window Action', 'win.test-action')

        # 3. a group inserted into the button the popover is attached to
        # this one doesn't work.
        button_action_group = Gio.SimpleActionGroup()
        button_action_group.add_action(test_action)
        button.insert_action_group('button', button_action_group)
        menu.append('Button Action', 'button.test-action')

        # 4. a group inserted into the popover itself. works fine
        popover_action_group = Gio.SimpleActionGroup()
        popover_action_group.add_action(test_action)
        self.popover.insert_action_group('popover', popover_action_group)
        menu.append('Popover Action', 'popover.test-action')

    def do_activate(self):
        self.win.present()

    def on_button_clicked(self, button):
        self.popover.show_all()

app = TestApp()
app.run()
