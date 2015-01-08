# usr/bin/env python3
# encoding:utf8

from gi.repository import Gtk, WebKit


class EntryDetailsView():
    def __init__(self):

        self.container = Gtk.ScrolledWindow()

        web = WebKit.WebView()
        web.load_string(
            "<html><body><center><h1>Hallo Eule!</h1><center></body></html>",
            "text/html",
            "UTF-8",
            "/"
            )
        web.grab_focus()
        web.set_size_request(300, 200)

        self.container.add(web)


