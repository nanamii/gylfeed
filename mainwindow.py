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
        infobox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

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

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.ERROR)
        infobar_label = Gtk.Label("There is an Error while loading the URL. Please try again")
        infobar_content = self.infobar.get_content_area()
        infobar_content.add(infobar_label)
        self.infobar.set_no_show_all(True)
        infobar_label.show()
        infobox.add(self.infobar)

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

        vbox.add(infobox)
        vbox.add(searchbox)
        vbox.pack_start(self.stack, True, True, 0)

        self.feedview = Feedview(self)
        self.stack.add_named(self.feedview.container, "feedview")
        self.feedview.listbox.connect('row-activated', self.show_entries)

        self.entrylist = EntryListView()
        self.stack.add_named(self.entrylist.container, "entrylist")
        self.entrylist.listbox.connect('row-activated', self.show_entry_details)

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
            self.update_headerbar(child)


    def update_headerbar(self, child, selected_row=None):

        child_name = self.stack.get_visible_child_name()

        if child_name == "feedview":
            self.set_button_sensitive(False, True)
            self.set_title("{num_feeds} Feeds"
            .format (num_feeds = self.feedhandler.count_feeds()))
        elif child_name == "entrylist":
            self.set_button_sensitive(True, True)
            self.set_title("{feed_name}"
                           .format (feed_name = selected_row.get_feed().get_name()))
        elif child_name == "entrydetails":
            self.set_button_sensitive(True, False)
        else:
            self.set_button_sensitive(False, False)

    def set_button_sensitive(self, left_value, right_value):
        self.button_left.set_sensitive(left_value)
        self.button_right.set_sensitive(right_value)

    def set_title(self, title, subtitle = None):
        self.headerbar.set_title(title)
        self.headerbar.set_subtitle(subtitle)

    def manage_searchbar(self, button_search):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)

    def open_settingsmenu(self, button_settings):
        self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        self.menu.show_all()

    # callback-function für update-button
    def update_clicked(self, update):
        self.feedhandler.update()

    # callback-function für addfeed-button
    def add_feed_clicked(self, add):
        self.stack.set_visible_child(self.feed_options.grid)

    # callback-function für feedview_add_feed(durch OK-Button ausgelöst)
    def set_feedview(self, options, url, feed_name, new_entries):
        new_feed = self.feedhandler.create_feed(url, feed_name)
        if new_feed:
            self.feedview.new_listbox_row("default_icon.png", feed_name, new_entries, new_feed)
            self.show_all()
            self.stack.set_visible_child(self.feedview.container)
            self.update_headerbar(self.stack.get_visible_child)
            self.infobar.hide()
            self.feed_options.empty_form()
        else:
            self.infobar.show()

    # callback-function um feedentries darzustellen, nach update
    def update_entryview(self, feedhandler, feed):
        entries = feed.get_entries()
        for title,plot,date in entries:
            self.entrylist.new_ListBoxRow("default_icon.png", title, date, plot)

    # callback-function für listbox in feedview, Row=feed gewählt
    def show_entries(self, listbox, row):
        selected_row = listbox.get_selected_row()
        selected_row.get_feed().update()
        self.stack.set_visible_child(self.entrylist.container)
        self.update_headerbar(self.stack.get_visible_child, selected_row)


    # call-back-function für listbox in entryview, Row=entry gewählt
    def show_entry_details(self, listbox, row):
        selected_row = listbox.get_selected_row()
        self.entry_details.load_headline(selected_row.get_feed(),selected_row.get_time(), selected_row.get_plot())
        self.stack.set_visible_child(self.entry_details.container)
        self.update_headerbar(self.stack.get_visible_child)


    def init_main_window(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
