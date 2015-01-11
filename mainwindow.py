#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GdkPixbuf, GObject
from feedhandler import Feedhandler
from feedview import Feedview
from feedoptionsview import FeedOptionsView
from entrylistview import EntryListView
from simple_popup_menu import SimplePopupMenu
from entrydetailsview import EntryDetailsView


class MainWindow(Gtk.Window):

    def __init__(self, feedhandler):

        Gtk.Window.__init__(self, title="gylfeed - Feedreader")
        self.set_border_width(10)
        self.set_default_size(800, 600)
        self.feedhandler = feedhandler
        self.feedhandler.connect("feed-updated", self.update_entryview)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "gylfeed"
        self.headerbar.props.subtitle = "the FeeedReader"
        self.set_titlebar(self.headerbar)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        searchbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

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

        self.headerbar.pack_start(box)
        self.headerbar.pack_end(self.button_search)
        self.headerbar.pack_end(self.button_settings)

        self.searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        self.searchbar.connect_entry(searchentry)
        self.searchbar.add(searchentry)
        searchbox.add(self.searchbar)
        self.searchbar.set_search_mode(False)

        self.menu = SimplePopupMenu()
        self.menu.simple_add('update', self.update_clicked, stock_id='view-refresh-symbolic')
        self.menu.simple_add('add feed', self.add_feed_clicked, stock_id='gtk-new' )
        self.menu.simple_add_separator()

        vbox.add(searchbox)
        vbox.pack_start(self.stack, True, True, 0)

        self.feedview = Feedview(self)
        self.stack.add_named(self.feedview.container, "feedview")

        self.entrylist = EntryListView()
        self.stack.add_named(self.entrylist.container, "entrylist")

        self.entry_details = EntryDetailsView()
        self.stack.add_named(self.entry_details.container, "entrydetails")

        self.button_left.connect("clicked", self.switch_child)
        self.button_right.connect("clicked", self.switch_child)

        self.feed_options = FeedOptionsView()
        self.stack.add_named(self.feed_options.grid, "feedoptions")
        self.feed_options.connect('feed-options', self.set_feedview)


    def switch_child(self, direction):
        child = {
            self.feed_options.grid:{
                self.button_left:None,
                self.button_right:self.feedview.container,
            },
            self.entrylist.container:{
                self.button_left:self.feedview.container,
                self.button_right:self.entry_details.container
            },
            self.feedview.container:{
                self.button_left:None,
                self.button_right:self.entrylist.container
            },
            self.entry_details.container:{
                self.button_left:self.entrylist.container,
                self.button_right:None
            }
        }.get(self.stack.get_visible_child()).get(direction)

        if child is not None:
            self.stack.set_visible_child(child)
            self.update_childview(child)


    def update_childview(self, child):

        child_name = self.stack.get_visible_child_name()

        if child_name == "feedview":
            self.set_button_sensitive(False, True)
        elif child_name == "entrylist":
            self.set_button_sensitive(True, True)
        elif child_name == "entrydetails":
            self.set_button_sensitive(True, False)
        else:
            self.set_button_sensitive(False, False)

    def set_button_sensitive(self, left_value, right_value):
        self.button_left.set_sensitive(left_value)
        self.button_right.set_sensitive(right_value)

    def set_title(title, subtitle = None):
        self.headerbar.props.title = title
        self.headerbar.props.subtitle = subtitle

    def manage_searchbar(self, button_search):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)

    def open_settingsmenu(self, button_settings):
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        self.menu.show_all()

    def update_clicked(self, update):
        self.feedhandler.update()

    def add_feed_clicked(self, add):
        self.stack.set_visible_child(self.feed_options.grid)

    # call-back-function für feedview_add_feed
    def set_feedview(self, options, url, name, new_entries):
        self.feedhandler.create_feed(url, name)
        self.feedview.new_listbox_row("default_icon.png", url, name, new_entries)
        self.show_all()
        print("callback set_feedview in MainWindow")

    # call-back-function um feedentries darzustellen, nach update
    def update_entryview(self, feedhandler):
        # hier noch feste Werte, ändern!!
        feed = feedhandler.feeds[0]
        entries = feed.get_entries()
        for title,plot,date in entries:
            self.entrylist.new_ListBoxRow("default_icon.png", title, date)


    def init_main_window(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
