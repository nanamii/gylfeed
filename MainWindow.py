#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GdkPixbuf
from Feedview import Feedview
from FeedOptionsView import FeedOptionsView
from EntryListView import EntryListView


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="gylfeed - Feedreader")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        main_window = Gtk.HeaderBar()
        main_window.set_show_close_button(True)
        main_window.props.title = "gylfeed"
        self.set_titlebar(main_window)

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

        main_window.pack_start(box)

        vbox.add(self.stack)

        self.feed_options = FeedOptionsView()
        self.stack.add_named(self.feed_options.grid, "feed_options")

        self.feedview = Feedview()
        self.stack.add_named(self.feedview.box, "listbox")

        self.entrylist = EntryListView()
        self.stack.add_named(self.entrylist.listbox, "B")

        self.button = Gtk.Button("Hello")
        self.stack.add_named(self.button, "a")

        self.button_left.connect("clicked", self.switch_child)
        self.button_right.connect("clicked", self.switch_child)


    def switch_child(self, direction):
        child = {
            self.feed_options.grid:{
                self.button_left:None,
                self.button_right:self.entrylist.listbox
            },
            self.entrylist.listbox:{
                self.button_left:self.feedview.box,
                self.button_right:self.button
            },
            self.feedview.box:{
                self.button_left:self.feed_options.grid,
                self.button_right:self.entrylist.listbox
            },
            self.button:{
                self.button_left:self.entrylist.listbox,
                self.button_right:None
            }
        }.get(self.stack.get_visible_child()).get(direction)

        if child is not None:
            self.stack.set_visible_child(child)




main_Window = MainWindow()
main_Window.connect("delete-event", Gtk.main_quit)
main_Window.entrylist.new_ListBoxRow("buttonMeth", "Entry aus Methodenaufruf")
main_Window.entrylist.new_ListBoxRow("button2", "2. Entry aus Methodenaufruf")
main_Window.feedview.new_ListBoxRow_Box("default_icon.png","Sueddeutsche", "Sueddeutsche", "new: 12 ")
main_Window.feedview.new_ListBoxRow_Box("default_icon.png","Golem-Feed", "Golem-Feed", "new: 30")
main_Window.show_all()
Gtk.main()
