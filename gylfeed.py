#!/usr/bin/env python3
# encoding: utf8


from mainwindow import MainApplication
from gi.repository import Gtk, Gio, GdkPixbuf, GObject

import os
import feedhandler
import feed
import sys

if __name__ == '__main__':

    app = MainApplication()
    sys.exit(app.run(sys.argv))
