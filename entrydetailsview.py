# usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, WebKit
from jinja2 import Template
from view import View

class EntryDetailsView(View):
    def __init__(self, app):
        View.__init__(self, app)
        self.app_window.entrylist.listbox.connect('row-activated', self.show_entry_details)

        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)

        self.overlay = Gtk.Overlay()
        self.web = WebKit.WebView()
        self.web.grab_focus()
        self.web.set_size_request(300, 200)

        scw = Gtk.ScrolledWindow()
        scw.add(self.web)
        self.overlay.add(scw)
        self.add(self.overlay)
        self.headline = ""
        self.plot = ""
        self.author = ""
        self.prev_listbox = None
        self.entry_id = None

        self.browse_button = Gtk.Button("Browse Source")
        self.browse_button.set_valign(Gtk.Align.END)
        self.browse_button.set_halign(Gtk.Align.START)
        self.browse_button.set_margin_start(15)
        self.browse_button.set_margin_bottom(15)
        self.browse_button.set_relief(Gtk.ReliefStyle.NONE)
        self.browse_button.connect("clicked", self.browse_link)

        self.overlay.add_overlay(self.browse_button)
        self.overlay.show()

    def load_headline(self, headline, time, plot, link):
        with open("template.html", "r") as fd:
            text = fd.read()
        template = Template(text)
        var = template.render(headline=headline, time=time, plot=plot,
            link=link)
        self.web.load_string(var, "text/html", "UTF-8", "/")

    def set_prev_listbox(self, prev_listbox):
        self.prev_listbox = prev_listbox

    def set_entry_id(self, entry_id):
        self.entry_id = entry_id

    def get_entry_id(self):
        return self.entry_id

    def on_view_enter(self):
        self.app_window.button_search.set_sensitive(False)
        self.browse_button.show_all()

    def on_view_leave(self):
        self.app_window.button_search.set_sensitive(True)

    def browse_link(self, _):
        self.web.load_uri(self.entry_id)
        self.browse_button.hide()

    # i.O. call-back-function für listbox in entryview, Row=entry gewählt
    def show_entry_details(self, listbox, row):
        selected_row = listbox.get_selected_row()
        self.load_headline(selected_row.get_title(),selected_row.get_time(),
            selected_row.get_plot(), selected_row.get_id())
        self.app_window.views.switch("entrydetails")
        selected_row.get_feed().set_entry_is_read(selected_row.get_id())
        self.set_prev_listbox(listbox)
        self.set_entry_id(selected_row.get_id())
