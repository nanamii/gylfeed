#!/usr/bin/env python3
# encoding: utf8


from mainwindow import MainWindow
from gi.repository import Gtk, Gio, GdkPixbuf, GObject

import os
import feedhandler
import feed

if __name__ == '__main__':

    feed_list = []


    #if os.path.exists('feeds.pickle'):
    #    fh = feedhandler.load_from_Disk()
    #else:
    #    fh = feedhandler.Feedhandler()
    #    feed_list = fh.create_feed("http://rss.sueddeutsche.de/rss/Muenchen", "sueddeutschE")

    #for feed in feed_list:
    #    feed.update()

    #fh.save_to_Disk()

    fh = feedhandler.Feedhandler()
    mw = MainWindow(fh)
    mw.init_main_window()

    Gtk.main()
