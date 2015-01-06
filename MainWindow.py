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

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        headerbar.props.title = "gylfeed"
        headerbar.props.subtitle = "the FeeedReader"
        self.set_titlebar(headerbar)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        searchbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

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

        self.button_settings = Gtk.Button.new_from_icon_name('view-sidebar-symbolic', Gtk.IconSize.BUTTON)
        self.button_settings.connect("clicked", self.open_settingsmenu)

        self.button_search = Gtk.Button.new_from_icon_name('system-search', Gtk.IconSize.BUTTON)
        self.button_search.connect("clicked", self.manage_searchbar)
        self.button_search.set_tooltip_text("search for content")

        headerbar.pack_start(box)
        headerbar.pack_end(self.button_search)
        headerbar.pack_end(self.button_settings)

        self.searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        self.searchbar.connect_entry(searchentry)
        self.searchbar.add(searchentry)
        searchbox.add(self.searchbar)
        self.searchbar.set_search_mode(False)

        self.menu = Gtk.Menu()
        menuitem = Gtk.MenuItem(label="update")
        self.menu.append(menuitem)

        vbox.add(searchbox)
        vbox.add(self.stack)

        self.feedview = Feedview(self)
        self.stack.add_named(self.feedview.box, "listbox")

        self.entrylist = EntryListView()
        self.stack.add_named(self.entrylist.listbox, "B")

        self.button = Gtk.Button("Hello")
        self.stack.add_named(self.button, "a")

        self.button_left.connect("clicked", self.switch_child)
        self.button_right.connect("clicked", self.switch_child)

        self.feed_options = FeedOptionsView()
        self.stack.add_named(self.feed_options.grid, "feed_options")


    def switch_child(self, direction):
        child = {
            self.feed_options.grid:{
                self.button_left:None,
                self.button_right:self.feedview.box,
            },
            self.entrylist.listbox:{
                self.button_left:self.feedview.box,
                self.button_right:self.button
            },
            self.feedview.box:{
                self.button_left:None,
                self.button_right:self.entrylist.listbox
            },
            self.button:{
                self.button_left:self.entrylist.listbox,
                self.button_right:None
            }
        }.get(self.stack.get_visible_child()).get(direction)

        if child is not None:
            self.stack.set_visible_child(child)


    def manage_searchbar(self, button_search):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)


    def open_settingsmenu(self, button_settings):
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        self.menu.show_all()



main_Window = MainWindow()
main_Window.connect("delete-event", Gtk.main_quit)
main_Window.entrylist.new_ListBoxRow("default_icon.png", "Entry aus Methodenaufruf", "Entry Methodenaufrauf", "fldldld")
main_Window.entrylist.new_ListBoxRow("default_icon.png", "2. Entry aus Methodenaufruf", "Entry 2 Methonen...", "fkfkfk")
main_Window.feedview.new_ListBoxRow_Box("default_icon.png","Sueddeutsche", "Sueddeutsche", "new: 12 ")
main_Window.feedview.new_ListBoxRow_Box("default_icon.png","Golem-Feed", "Golem-Feed", "new: 30")
main_Window.show_all()
Gtk.main()
