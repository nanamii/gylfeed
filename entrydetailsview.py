# usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, WebKit
from jinja2 import Template


class EntryDetailsView():
    def __init__(self):

        self.container = Gtk.ScrolledWindow()

        self.web = WebKit.WebView()
        self.web.grab_focus()
        self.web.set_size_request(300, 200)
        self.container.add(self.web)
        self.headline = ""
        self.plot = ""
        self.author = ""

    def load_headline(self, headline, author, plot):
        with open("template.html", "r") as fd:
            text = fd.read()
        template = Template(text)
        var = template.render(headline=headline, author=author, plot=plot)
        self.web.load_string(var, "text/html", "UTF-8", "/")
