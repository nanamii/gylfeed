#!/usr/bin/env python3
# encoding: utf8


from mainwindow import MainWindow
from gi.repository import Gtk, Gio, GdkPixbuf, GObject

import os
import feedhandler

if __name__ == '__main__':

    if os.path.exists('feeds.pickle'):
        fp = feedhandler.load_from_Disk()
    else:
        fp = feedhandler.Feedhandler()
        fp.add_Feed("http://rss.sueddeutsche.de/rss/Muenchen")

    fp.update()
    fp.save_to_Disk()

    mw = MainWindow(fp)
    mw.init_main_window()

    Gtk.main()
