from gi.repository import Gtk, Gio

class EntryWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="gylfeed - Feedreader")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        ewindow = Gtk.HeaderBar()
        ewindow.set_show_close_button(True)
        ewindow.props.title = "gylfeed"
        self.set_titlebar(ewindow)

        #button = Gtk.Button()
        #icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        #button.add(image)
        #ewindow.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        #button = Gtk.Button()
        #button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        #box.add(button)

        #button = Gtk.Button()
        #button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        #box.add(button)

        ewindow.pack_start(box)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        box.add(stack_switcher)

        vbox.add(self.stack)
        self.listbox = Gtk.ListBox()
        self.stack.add_titled(self.listbox, "B", Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))

        button = Gtk.Button("Hello")
        self.stack.add_named(button, "a")



    def new_ListBoxRow(self, buttonlabel, entry):
        grid = Gtk.Grid()
        row = Gtk.ListBoxRow()
        row.add(grid)
        button = Gtk.Button(label=buttonlabel)
        grid.add(button)
        label = Gtk.Label(entry)
        grid.attach(label, 1, 0, 2, 1)
        self.listbox.add(row)



entry_Window = EntryWindow()
entry_Window.connect("delete-event", Gtk.main_quit)
entry_Window.new_ListBoxRow("buttonMeth", "Entry aus Methodenaufruf")
entry_Window.new_ListBoxRow("button2", "2. Entry aus Methodenaufruf")
entry_Window.show_all()
Gtk.main()
