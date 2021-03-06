#!usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, Gio, GLib, GdkPixbuf, GObject, Gdk
from feedhandler import Feedhandler, load_from_disk
from feed import Feed
from feed import SumFeed
from feedview import Feedview
from feedoptionsview import FeedOptionsView
from entrylistview import EntryListView
from entrydetailsview import EntryDetailsView
from functools import partial
import os


class ViewSwitcher(Gtk.Box):
    def __init__(self, stack):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self._stack = stack
        self._prev = None

        self.get_style_context().add_class('linked')

        self.go_left, self.go_right = Gtk.Button(), Gtk.Button()
        for btn, arrow, direction in (
            (self.go_left, Gtk.ArrowType.LEFT, -1),
            (self.go_right, Gtk.ArrowType.RIGHT, +1)
        ):
            btn.add(Gtk.Arrow(arrow, Gtk.ShadowType.NONE))
            btn.connect('clicked', partial(self._set_widget_at, step=direction))
            btn.set_sensitive(False)
            self.add(btn)

        self.show_all()

    def _find_curr_index(self):
        visible = self._stack.get_visible_child()
        widgets = list(self._stack)

        try:
            return widgets.index(visible)
        except ValueError:
            return 0

    def _get_widget_at(self, idx):
        idx = max(0, min(len(self._stack) - 1, idx))
        return list(self._stack)[idx]

    def _set_widget_at(self, _, step):
        current_idx = self._find_curr_index()
        next_widget = self._get_widget_at(current_idx + step)
        self._set_visible_child(next_widget)
        self._update_sensitivness()

    def _set_visible_child(self, child, update_prev=True):
        prev = self._stack.get_visible_child()
        self._stack.set_visible_child(child)

        try:
            child.emit('view-enter')
        except TypeError:
            pass

        try:
            prev.emit('view-leave')
        except TypeError:
            pass

        prev._is_visible = False
        child._is_visible = True

        # setzt aktuelle prev als neue prev
        if update_prev:
            self._prev = prev

    def _update_sensitivness(self):
        idx = self._find_curr_index()
        self.go_left.set_sensitive(idx != 0)
        self.go_right.set_sensitive(idx != len(self._stack) - 1)

    def add_view(self, view, name):
        view.set_hexpand(True)
        view.set_vexpand(True)
        view.set_halign(Gtk.Align.FILL)
        view.set_valign(Gtk.Align.FILL)
        view.show_all()

        self._stack.add_named(view, name)

    def switch(self, name):
        widget = self._stack.get_child_by_name(name)
        self._set_visible_child(widget)
        self._update_sensitivness()

    def switch_to_previous(self):
        if self._prev is None:
            return

        self._set_visible_child(self._prev, update_prev=False)
        self._update_sensitivness()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app, feedhandler):
        Gtk.ApplicationWindow.__init__(self, title="gylfeed - Feedreader", application=app)
        app.win = self
        self.set_default_size(800, 600)
        self.set_default_icon(self._load_application_icon())
        self.feedhandler = feedhandler

        feedhandler.connect('feed-created', self.on_feed_created)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "gylfeed"
        self.headerbar.props.subtitle = "the FeeedReader"
        self.set_titlebar(self.headerbar)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        infobox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        ##############################################################################

        self.button_settings = Gtk.Button.new_from_icon_name('view-sidebar-symbolic', Gtk.IconSize.BUTTON)
        self.button_settings.connect("clicked", self._open_settingsmenu)
        self.button_settings.set_tooltip_text("General Options \n -Add Feed \n -Update")

        self.button_search = Gtk.Button.new_from_icon_name('system-search', Gtk.IconSize.BUTTON)
        self.button_search.set_tooltip_text("Search for Content")

        ########################################################################
        def create_item(name, action, icon):
            item = Gio.MenuItem.new(name, action)
            item.set_icon(Gio.ThemedIcon.new(icon))
            item.set_attribute_value("accel", GLib.Variant("s","<F5>"))
            return item


        menu = Gio.Menu()
        menu.append_item(create_item('Add Feed              <Ctrl>+A', 'app.add', 'add'))
        menu.append_item(create_item('Update Feeds       <Ctrl>+R', 'app.update', 'reload'))
        menu.append_item(create_item('About gylfeed', 'app.about','help-about'))
        menu.append_item(create_item('Quit                      <Ctrl>+Q', 'app.quit', 'window-close'))

        self.popover = Gtk.Popover.new_from_model(self.button_settings, menu)
        self.popover.get_preferred_size()
        self.popover.set_border_width(10)
        ###########################################################################

        self.views = ViewSwitcher(self.stack)
        self.headerbar.pack_start(self.views)
        self.headerbar.pack_end(self.button_settings)
        self.headerbar.pack_end(self.button_search)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_message_type(Gtk.MessageType.ERROR)
        self.infobar_label = Gtk.Label("")
        content = self.infobar.get_content_area()
        content.add(self.infobar_label)
        self.infobar.set_no_show_all(True)
        infobox.add(self.infobar)

        vbox.add(infobox)
        vbox.pack_start(self.stack, True, True, 0)

        self.feed_options = FeedOptionsView(app)
        self.views.add_view(self.feed_options, "feedoptions")

        self.feedview = Feedview(app)
        self.views.add_view(self.feedview, "feedview")
        self.feedview.connect('ok-delete-clicked', self.delete_feed_actions)

        self.entrylist = EntryListView(app)
        self.views.add_view(self.entrylist, "entrylist")

        self.entry_details = EntryDetailsView(app)
        self.views.add_view(self.entry_details, "entrydetails")

        self.views.switch("feedview")

        self.connect("key-press-event", self._key_navigation)


    def _load_application_icon(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("./graphics/gylfeed_logo_blank.png")
        return pixbuf

    def _key_navigation(self, window, event):
        key = event.keyval

        vis_child = self.stack.get_visible_child()
        child_name = self.stack.get_visible_child_name()

        if key == Gdk.KEY_Right:
            if (child_name == "entrylist"):
                self.entry_details.show_entry_details(self.entrylist.listbox,
                    self.entrylist.listbox.get_selected_row()
                    )
            else:
                self.entrylist.show_entries(self.feedview.listbox,
                    self.feedview.listbox.get_selected_row()
                )
        if key == Gdk.KEY_Left:
            if (child_name == "entrydetails"):
                self.entrylist.show_entries(self.feedview.listbox, self.feedview.listbox.get_selected_row())
                for row in self.entrylist.listbox:
                    if row.get_id() == self.entry_details.get_entry_id():
                        self.entrylist.listbox.select_row(row)

            elif (child_name == "feedview"):
                return
            else:
                self.views.go_left.emit("clicked")

    def show_about(self, about_button, action):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("./graphics/gylfeed_logo.png", 120, 240)
        about = Gtk.AboutDialog()
        about.set_modal(True)
        about.set_transient_for(self)
        about.set_authors(["Susanne Kießling <susanne.kiessling@nullcat.de>"])
        about.set_logo(pixbuf)
        about.set_program_name("gylfeed")
        about.set_version("1.0")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_wrap_license(True)
        about.set_comments("gylfeed is a simple to use Feedreader")
        about.set_copyright("by S. Kießling")
        about.show()

    def set_title(self, title=None, subtitle=None):
        self.headerbar.set_title(title)
        self.headerbar.set_subtitle(subtitle)

    def _open_settingsmenu(self, _):
        self.popover.show_all()

    # callback-function für add-feed im settings-menu
    def add_feed_clicked(self, add, name):
        self.views.switch("feedoptions")

    # callback-function für discard-action
    def discard_action(self, discard_button):
        self.views.switch("feedview")
        self.infobar.hide()
        self.feed_options.empty_form()

    # callback-function für feedview_add_feed(durch OK-Button ausgelöst)
    def set_feedview(self, ok_button):
        init_data = {"url":self.feed_options.get_url(),
                     "feed_name":self.feed_options.get_name(),
                     "update_spin":self.feed_options.get_update_interval(),
                     "delete_spin":self.feed_options.get_delete_interval(),
                     "update_switch":self.feed_options.get_uswitch_state(),
                     "notify_switch":self.feed_options.get_nswitch_state()
                     }
        self.feedhandler.create_feed(init_data)

    def on_feed_created(self, feed_handler, new_feed):
        new_entries = len(new_feed.get_entries())
        self.feedview.new_listbox_row(
            "./graphics/default_icon.png", new_feed
        )
        self.show_all()
        self.views.switch("feedview")
        self.infobar.hide()
        self.feed_options.empty_form()

    # callback-function für delete-feed, ok-button in ActionBar gewählt
    def delete_feed_actions(self, feedview, feed):
        self.feedhandler.delete_feed(feed)
        self.feedview.remove_feedrow(feed)
        self.entrylist.clear_listbox()
        self.feedview.action_bar.hide()

    def add_widget_to_headerbar(self, widget, start_or_end):
        if start_or_end == "start":
            self.headerbar.pack_start(widget)
        else:
            self.headerbar.pack_end(widget)

    def remove_widget_from_headerbar(self, widget):
        widget.destroy()

    def emit_search_signal(self, _, __):
        self.button_search.emit('clicked')



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

        self.fh = Feedhandler()
        if os.path.exists('feeds.pickle'):
            self.fh.feeds = [Feed(*ftuple) for ftuple in load_from_disk()]
            self.fh._connect_feeds()
            self.fh.update_all_feeds()
            self.fh.delete_old_entries()

        sumFeed = SumFeed(self.fh)
        self.fh.feeds.insert(0, sumFeed)
        self.win = MainWindow(self, self.fh)

        def create_action(name, callback=None):
            action = Gio.SimpleAction.new(name, None)

            if callback is None:
                    action.connect('activate', self.action_clicked)
            else:
                action.connect('activate', callback)
            return action

        self.add_action(create_action("add", self.win.add_feed_clicked))
        self.add_action(create_action("update", self.fh.update_all_feeds))
        self.add_action(create_action("about", self.win.show_about))
        self.add_action(create_action("quit", lambda *_: self.quit()))
        self.add_action(create_action("search", self.win.emit_search_signal))

        self.set_accels_for_action('app.add', ['<Ctrl>A'])
        self.set_accels_for_action('app.quit', ['<Ctrl>Q'])
        self.set_accels_for_action('app.update', ['<Ctrl>R'])
        self.set_accels_for_action('app.search', ['<Ctrl>F'])


        self.win.show_all()
        self.win.feedview.show_feedview(self.fh.feeds)
        self.connect('shutdown', MainApplication.on_shutdown)

    def on_shutdown(self):
        print("quitting!")
        self.fh.save_to_disk()
        Gtk.Application.quit(self)

    def action_clicked(self, *args):
        print(args)
