# usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, WebKit
from jinja2 import Template
from view import View

class EntryDetailsView(View):
    def __init__(self, app):
        View.__init__(self, app)
        self.app_window.entrylist.listbox.connect('row-activated', self.show_entry_details)

        self.web = WebKit.WebView()
        self.web.grab_focus()
        self.web.set_size_request(300, 200)
        self.add(self.web)
        self.headline = ""
        self.plot = ""
        self.author = ""
        self.prev_listbox = None
        self.entry_id = None

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

    def on_view_leave(self):
        self.app_window.button_search.set_sensitive(True)

    # i.O. call-back-function für listbox in entryview, Row=entry gewählt
    def show_entry_details(self, listbox, row):
        selected_row = listbox.get_selected_row()
        self.load_headline(selected_row.get_title(),selected_row.get_time(),
            selected_row.get_plot(), selected_row.get_id())
        self.app_window.views.switch("entrydetails")
        selected_row.get_feed().set_entry_is_read(selected_row.get_id())
        self.set_prev_listbox(listbox)
        self.set_entry_id(selected_row.get_id())


