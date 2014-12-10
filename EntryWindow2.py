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

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)

        self.button_left = Gtk.Button()
        self.button_left.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.button_left)

        self.button_right = Gtk.Button()
        self.button_right.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.button_right)

        ewindow.pack_start(box)

        vbox.add(self.stack)

        self.button1 = Gtk.Button("Feeds")
        self.stack.add_named(self.button1, "A")

        self.listbox = Gtk.ListBox()
        self.stack.add_named(self.listbox, "B")

        self.button = Gtk.Button("Hello")
        self.stack.add_named(self.button, "a")

        self.button_left.connect("clicked", self.switch_child)
        self.button_right.connect("clicked", self.switch_child)


    def switch_child(self, direction):
        child = {
            self.listbox:{
                self.button_left:self.button1,
                self.button_right:self.button
            },
            self.button1:{
                self.button_left:self.button1,
                self.button_right:self.listbox
            },
            self.button:{
                self.button_left:self.listbox,
                self.button_right:self.button
            }
        }.get(self.stack.get_visible_child()).get(direction)


        if child is not None:
            self.stack.set_visible_child(child)


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
