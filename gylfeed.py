#!/usr/bin/env python3
# encoding: utf8


from mainwindow import MainApplication
from gi.repository import Gtk, Gio, GdkPixbuf, GObject

import os
import feedhandler
import feed
import sys

if __name__ == '__main__':

    #feed_list = []

    #if os.path.exists('feeds.pickle'):
    #    fh = feedhandler.load_from_Disk()
    #else:
    #    fh = feedhandler.Feedhandler()
    #    feed_list = fh.create_feed("http://rss.sueddeutsche.de/rss/Muenchen", "sueddeutschE")

    #for feed in feed_list:
    #    feed.update()

    #fh.save_to_Disk()

#    mw = MainWindow(fh)
#    mw.init_main_window()
#
    sys.exit(MainApplication().run(sys.argv))
    Gtk.main()
