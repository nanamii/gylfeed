#!usr/bin/env python3
# encoding:utf8

""" Testmodule for parsing feeds. """

# Stdlib:
import pprint
import pickle

from functools import partial

# Internal:
from feed import Feed

# External:
import feedparser

from gi.repository import Gtk, GObject, GLib


class Feedhandler(GObject.GObject):
    """ Handles different feeds. """
    __gsignals__ = {
        'feed-created': (GObject.SIGNAL_RUN_FIRST, None,(Feed, )),
        'feed-updated' : (GObject.SIGNAL_RUN_FIRST, None,(GObject.GObject, )),
        'feed-add-exception' : (GObject.SIGNAL_RUN_FIRST, None, (str, ))
    }


    def __init__(self):
        GObject.GObject.__init__(self)
        self.feeds = []

        def _update_recurring():
            self.update_all_feeds()

            # TODO: Return settings.do_auto_update
            return True

        GLib.timeout_add(
            5 * 60 * 1000, _update_recurring

        )

    def create_feed(self, url, feed_name, update_switch, notify_switch):
        print("create_feed in Feedhandler:")
        print(len(self.feeds))
        feed = Feed(url, feed_name, update_switch, notify_switch)
        feed.connect(
            'created',
            self._create_feed_deferred,
            url, feed_name
        )

    def _create_feed_deferred(self, feed, url, feed_name):
        import pprint
        print('rawfeed ppritn')
        pprint.pprint(feed)

        if self.no_entry_text(url, feed_name):
            if len(feed_name) == 0:
                self.emit('feed-add-exception', "Keinen Feednamen eingetragen, bitte eintragen!")
            if len(url) == 0:
                self.emit('feed-add-exception', "Keine URL eingetragen, bitte eintragen!")
            return

        if feed.raw_feed.bozo == 1:
            self.emit('feed-add-exception', "URL liefert kein Ergebnis, bitte erneut eingeben.")
            return

        if self.feed_exists(url):
            print("Feed bereits vorhanden!!")
            self.emit('feed-add-exception', "Feed bereits vorhanden!")
            return

        if self.feed_name_exists(feed_name):
            print("Es ist bereits ein Feed mit diesem Namen vorhanden, bitte anderen Namen wählen!")
            self.emit('feed-add-exception', "Es ist bereits ein Feed mit diesem Namen vorhanden, bitte anderen Namen wählen!")
            return

        feed.connect('updated', self.sig_feed_updated)
        self.feeds.append(feed)

        # TODO: Fraglich ob update nötig ist.
        #feed.update()

        self.emit('feed-created', feed)

    def feed_exists(self, url):
        for feed in self.feeds:
            if feed.get_url() == url:
                return True
        return False

    def feed_name_exists(self, feed_name):
        for feed in self.feeds:
            if feed.get_name() == feed_name:
                return True
        return False

    def no_entry_text(self, url, feed_name):
        if len(url) == 0 or len(feed_name) == 0:
            return True
        return False

    def get_feed_list(self):
        return self.feeds

    def count_feeds(self):
        return len(self.feeds)

    def update_all_feeds(self, btn=None, action=None):
        print("UPDATE")
        # TODO: save after update done.
        self.save_to_disk()
        print(self.feeds)
        for feed in self.feeds:
            print(feed.get_name(), "feedprint in update_all_feeds, feedhanlder")

            GLib.idle_add(partial(Feed.update, self=feed))


    # TODO: warum so gelöst?
    def connect_feeds(self):
        for feed in self.feeds:
            feed.connect('updated', self.sig_feed_updated)

    def delete_feed(self, feed):
        for f in self.feeds:
            if f.get_url() == feed.get_url():
                self.feeds.pop(self.feeds.index(f))

    def save_to_disk(self):
        try:
            with open ('feeds.pickle', 'wb') as fp:
                pickle.dump([f.get_serializable_data() for f in self.feeds], fp)
                print("Saving data to disk")
        except IOError as ie:
            print("Fail to save data {ie}".format(ie=ie))

    # callback-function zu update von feed,
    #löst selbst Signal aus --> MainWindow
    def sig_feed_updated(self, feed):
        self.emit('feed-updated', feed)


def load_from_disk():
    try:
        with open('feeds.pickle', 'rb') as fp:
            print("Loading data from disk")
            return pickle.load(fp)
    except IOError as ie:
            print("Fail to load data {ie}".format(ie=ie))
