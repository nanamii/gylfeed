#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GdkPixbuf, GObject
from feedhandler import Feedhandler, load_from_disk
from feed import Feed
from feedview import Feedview
from feedoptionsview import FeedOptionsView
from entrylistview import EntryListView
from simple_popup_menu import SimplePopupMenu
from entrydetailsview import EntryDetailsView

import os


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app, feedhandler):
        Gtk.ApplicationWindow.__init__(self, title="gylfeed - Feedreader", application=app)
        self.set_default_size(800, 600)
        self.feedhandler = feedhandler
        self.feedhandler.connect("feed-updated", self.update_entryview)
        self.feedhandler.connect("feed-add-exception", self.exception_handling)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "gylfeed"
        self.headerbar.props.subtitle = "the FeeedReader"
        self.set_titlebar(self.headerbar)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        searchbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        infobox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        # headerbar-buttons
        self.button_left = Gtk.Button()
        self.button_left.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.button_left)

        self.button_right = Gtk.Button()
        self.button_right.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.button_right)

         ######### only shown in feed_options_view ##################################
        self.button_suggest = Gtk.Button("Add Feed")
        self.button_suggest.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.button_suggest.set_no_show_all(True)

        self.button_discard = Gtk.Button("Discard")
        self.button_discard.get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)
        self.button_discard.set_no_show_all(True)

        self.button_edit = Gtk.Button("Change Data")
        self.button_edit.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.button_edit.set_no_show_all(True)

        ##############################################################################

        self.button_settings = Gtk.Button.new_from_icon_name('view-sidebar-symbolic', Gtk.IconSize.BUTTON)
        self.button_settings.connect("clicked", self.open_settingsmenu)

        self.button_search = Gtk.Button.new_from_icon_name('system-search', Gtk.IconSize.BUTTON)
        self.button_search.connect("clicked", self.manage_searchbar)
        self.button_search.set_tooltip_text("search for content")

        ########################################################################
        def create_item(name, action, icon):
            item = Gio.MenuItem.new(name, action)
            item.set_icon(Gio.ThemedIcon.new(icon))
            return item

        menu = Gio.Menu()
        menu.append_item(create_item('Add Feed', 'app.add', 'add'))
        menu.append_item(create_item('Update Feeds', 'app.update', 'application-rss+xml'))
        menu.append_item(create_item('About gylfeed', 'app.about','stock-about'))
        menu.append_item(create_item('Quit', 'app.quit', 'window-close'))

        self.popover = Gtk.Popover.new_from_model(self.button_settings, menu)
        self.popover.get_preferred_size()
        self.popover.set_border_width(10)
        ###########################################################################

        self.headerbar.pack_start(box)
        self.headerbar.pack_start(self.button_discard)
        self.headerbar.pack_end(self.button_settings)
        self.headerbar.pack_end(self.button_search)
        self.headerbar.pack_end(self.button_suggest)
        self.headerbar.pack_end(self.button_edit)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.ERROR)
        self.infobar.set_no_show_all(True)
        infobox.add(self.infobar)

        self.searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        self.searchbar.connect_entry(searchentry)
        self.searchbar.add(searchentry)
        searchbox.add(self.searchbar)
        self.searchbar.set_search_mode(False)

        vbox.add(infobox)
        vbox.add(searchbox)
        vbox.pack_start(self.stack, True, True, 0)

        ###### auslagern in eigene View !!!!!!!!!!!!!!1
        self.aboutview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.aboutview.set_margin_top(30)
        about_label = Gtk.Label("Welcome to gylfeed. gylfeed is an simple and quick to use Feed-Reader ...")
        about_label.set_margin_top(20)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("./misc/gylfeed_logo.png", 120, 240)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.aboutview.add(image)
        self.aboutview.add(about_label)
        self.stack.add_named(self.aboutview, "about_view")

        self.feedview = Feedview()
        self.stack.add_named(self.feedview.container, "feedview")
        self.feedview.listbox.connect('row-activated', self.show_entries)
        self.feedview.connect('preferences-clicked', self.show_options_filled)

        self.entrylist = EntryListView()
        self.stack.add_named(self.entrylist.container, "entrylist")
        self.entrylist.listbox.connect('row-activated', self.show_entry_details)

        self.entry_details = EntryDetailsView()
        self.stack.add_named(self.entry_details.container, "entrydetails")

        self.button_left.connect("clicked", self.switch_child)
        self.button_right.connect("clicked", self.switch_child)

        self.feed_options = FeedOptionsView()
        self.stack.add_named(self.feed_options.container, "feedoptions")

        self.button_suggest.connect("clicked", self.set_feedview)
        self.button_discard.connect("clicked", self.discard_action)
        self.button_edit.connect("clicked", self.change_data)


    # callback-function für button_left und button_right
    def switch_child(self, direction):

        old_child = self.stack.get_visible_child()
        selected_row = None
        if old_child == self.feedview.container:
            print("if old_child")
            selected_row = self.feedview.listbox.get_selected_row()

        child = {
            self.feed_options.container:{
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
            self.update_headerbar(selected_row)


    def update_headerbar(self, selected_row=None): # TODO!!!!

        child_name = self.stack.get_visible_child_name()

        if child_name == "feedview":
            self.set_button_sensitive(False, True)
            self.set_title("{num_feeds} Feeds"
            .format (num_feeds = self.feedhandler.count_feeds()))
            self.button_search.set_sensitive(True)
            self.set_disc_sugg_button(False, False)
        elif child_name == "entrylist":
            self.set_button_sensitive(True, True)
            self.set_title("{feed_name}"
                .format (feed_name = selected_row.get_feed().get_name()))
        elif child_name == "entrydetails":
            self.set_button_sensitive(True, False)
        elif child_name == "about_view":
            self.set_title("gylfeed", "the owleee Feedreader")
            self.button_search.set_sensitive(True)
            self.set_disc_sugg_button(False, False)
        else:
            self.set_button_sensitive(False, False)
            self.set_title("Feed Options")
            self.button_search.set_sensitive(False)
            self.set_disc_sugg_button(True, True)

    def set_button_sensitive(self, left_value, right_value):
        self.button_left.set_sensitive(left_value)
        self.button_right.set_sensitive(right_value)

    def set_title(self, title, subtitle = None):
        self.headerbar.set_title(title)
        self.headerbar.set_subtitle(subtitle)

    def set_disc_sugg_button(self, disc_show, sug_show):
        if disc_show:
            self.button_discard.show()
        else:
            self.button_discard.hide()

        if sug_show:
            self.button_suggest.show()
        else:
            self.button_suggest.hide()

    def manage_searchbar(self, button_search):
        if self.searchbar.get_search_mode():
            self.searchbar.set_search_mode(False)
        else:
            self.searchbar.set_search_mode(True)

    def open_settingsmenu(self, button_settings):
        self.popover.show_all()

    # callback-function für update-button
    def update_clicked(self, update):
        self.feedhandler.update()

    # callback-function für add-feed im settings-menu
    def add_feed_clicked(self, add, name):
        self.stack.set_visible_child(self.feed_options.container)
        self.update_headerbar()

    # callback-function für discard-action
    def discard_action(self, discard_button):
        self.stack.set_visible_child(self.feedview.container)
        self.update_headerbar()
        self.infobar.hide()
        self.feed_options.empty_form()

    # callback-function für feedview_add_feed(durch OK-Button ausgelöst)
    def set_feedview(self, ok_button):
        url = self.feed_options.get_url()
        feed_name = self.feed_options.get_name()
        update_switch = self.feed_options.get_uswitch_state()
        notify_switch = self.feed_options.get_nswitch_state()
        new_entries = 0

        new_feed = self.feedhandler.create_feed(url, feed_name, update_switch, notify_switch)
        if new_feed:
            new_entries = len(new_feed.get_entries())
            self.feedview.new_listbox_row("default_icon.png", feed_name, new_entries, new_feed)
            self.show_all()
            self.stack.set_visible_child(self.feedview.container)
            self.update_headerbar()
            self.infobar.hide()
            self.feed_options.empty_form()

    def show_feedview_saved(self, feedlist):
        for feed in feedlist:
            self.feedview.new_listbox_row("default_icon.png", feed.get_name(), len(feed.get_entries()), feed)
            self.show_all()
            self.stack.set_visible_child(self.feedview.container)

    # callback-function für Ausnahmefälle bei add_feed
    def exception_handling(self, feedhandler, exception):
        label = Gtk.Label(exception)
        content = self.infobar.get_content_area()
        content.add(label)
        label.show()
        self.infobar.show()
        print("exception_handling callback")

    # callback-function um feedentries darzustellen, nach update; Hilfsfunktion
    # für show_entries
    def update_entryview(self, feedhandler, feed):
        print("update_entryview function")
        self.entrylist.clear_listbox()
        entries = feed.get_entries()
        print(len(entries))
        feed_name = feed.get_name()
        for title,plot,date in entries:
            self.entrylist.new_ListBoxRow("default_icon.png", title, date, plot, feed_name)

    # i.O. callback-function für listbox in feedview, Row=feed gewählt
    def show_entries(self, listbox, row):
        print("show_entries function")
        selected_row = listbox.get_selected_row()
        selected_row.get_feed().update()
        self.stack.set_visible_child(self.entrylist.container)
        self.update_headerbar(selected_row)


    # i.O. call-back-function für listbox in entryview, Row=entry gewählt
    def show_entry_details(self, listbox, row):
        selected_row = listbox.get_selected_row()
        self.entry_details.load_headline(selected_row.get_feed(),selected_row.get_time(), selected_row.get_plot())
        self.stack.set_visible_child(self.entry_details.container)
        self.update_headerbar(selected_row)


    # i.O. call-back-function für feed-optionen-gewählt
    def show_options_filled(self, feedview, feed):
        self.stack.set_visible_child(self.feed_options.container)
        self.feed_options.set_url(feed.get_url())
        self.feed_options.set_name(feed.get_name())
        self.update_headerbar()
        ########### neue Werte in feed übernehmen ################

    def change_data(self, button):
        print("change button pressed")

    def show_about(self, about_button, action):
        self.stack.set_visible_child(self.aboutview)
        self.update_headerbar()


    def init_main_window(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


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

        fh = Feedhandler()
        if os.path.exists('feeds.pickle'):
            print("pickle vorhanden")
            fh.feeds = [Feed(*ftuple) for ftuple in load_from_disk()]
            fh.connect_feeds()

            print(fh.feeds)
        self.win = MainWindow(self, fh)

        def create_action(name, callback=None):
            action = Gio.SimpleAction.new(name, None)

            if callback is None:
                action.connect('activate', self.action_clicked)
            else:
                action.connect('activate', callback)
            return action

        self.add_action(create_action("add", self.win.add_feed_clicked))
        self.add_action(create_action("update", fh.update_all_feeds))
        self.add_action(create_action("about", self.win.show_about))
        self.add_action(create_action("quit", callback=lambda *_: self.quit()))
        self.add_action(create_action("save"))

        self.set_accels_for_action('app.add', ['<Ctrl>A'])
        self.set_accels_for_action('app.quit', ['<Ctrl>Q'])

        self.win.show_all()
        self.win.show_feedview_saved(fh.feeds)


    def action_clicked(self, *args):
        print(args)
