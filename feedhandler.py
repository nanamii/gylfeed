#!usr/bin/env python3
# encoding:utf8

# Stdlib:
import pprint
import pickle

from functools import partial

# Internal:
from feed import Feed
from feed import SumFeed

# External:
import feedparser

from gi.repository import Gtk, GObject, GLib


class Feedhandler(GObject.GObject):

    """ Handles different feeds. """

    __gsignals__ = {
        'feed-created': (GObject.SIGNAL_RUN_FIRST, None, (Feed, )),
        'feed-updated': (GObject.SIGNAL_RUN_FIRST, None, (GObject.GObject, )),
        'feed-add-exception': (GObject.SIGNAL_RUN_FIRST, None, (str, ))
    }

    def __init__(self):

        GObject.GObject.__init__(self)
        self.feeds = []

    def create_feed(self, init_data):
        """ Create a feed-object by given parameters. """
        feed = Feed(init_data, feedhandler=self)

        feed.connect(
            'created',
            self._create_feed_deferred,
            init_data["url"], init_data["feed_name"]
        )

    def _create_feed_deferred(self, feed, url, feed_name):
        """ Helper-Function of create_feed, checks errors of userinput.

        :param feed: Feed which should be created.
        :param url: URL of feed.
        :param feed_name: Name of feed.
        """
        if self._no_entry_text(url, feed_name):
            if len(feed_name) == 0:
                self.emit(
                    'feed-add-exception',
                    "Keinen Feednamen eingetragen, bitte eintragen!"
                )
            if len(url) == 0:
                self.emit(
                    'feed-add-exception',
                    "Keine URL eingetragen, bitte eintragen!"
                )
            return

        if feed.raw_feed.bozo == 1:
            self.emit(
                'feed-add-exception',
                "URL liefert kein Ergebnis, bitte erneut eingeben."
            )
            return

        if self._feed_exists(url):
            self.emit('feed-add-exception', "Feed bereits vorhanden!")
            return

        if self._feed_name_exists(feed_name):
            self.emit(
                'feed-add-exception',
                "Es ist bereits ein Feed mit diesem Namen vorhanden, bitte anderen Namen wählen!"
            )
            return

        feed.connect('updated', self.sig_feed_updated)
        self.feeds.append(feed)
        self.emit('feed-created', feed)

    def _feed_exists(self, url):
        """ Return True if given url exists, False otherwise.

        :param url: The URL of Feed to check if exists.
        :return: True or False.
        """
        for feed in self.feeds:
            if feed.get_url() == url:
                return True
        return False

    def _feed_name_exists(self, feed_name):
        """ Return True if name of feed exists, False otherwise. """
        for feed in self.feeds:
            if feed.get_name() == feed_name:
                return True
        return False

    def _no_entry_text(self, url, feed_name):
        """ Return True if url or name of feed are empty, False otherwise. """
        if len(url) == 0 or len(feed_name) == 0:
            return True
        return False

    def get_feed_list(self):
        """ Return list with feeds. """
        return self.feeds

    def get_usual_feed_list(self):
        """ Return list with regular feeds, not SumFeed. """
        return [f for f in self.feeds if f.feedtype == 'usual']

    def count_feeds(self):
        """ Return number of regular feeds. """
        return len(self.feeds)-1

    def update_all_feeds(self, btn=None, action=None):
        """ Update all feeds, holding in feedlist. """
        # TODO: save after update done.
        self.save_to_disk()

        feeds = self.get_usual_feed_list()
        feed_list = feeds

        for feed in feed_list:
            print(feed.get_name(), "feedprint in update_all_feeds, feedhandler")

            GLib.idle_add(partial(Feed.update, self=feed))

    def delete_feed(self, feed):
        """ Delete given feed.
        :param feed: Feed which should be deleted.
        """
        for f in self.feeds:
            if f.get_url() == feed.get_url():
                self.feeds.pop(self.feeds.index(f))

    def delete_old_entries(self):
        """ Delete old entries, delegating to delete_old_entries
            function of single feed.
        """
        for feed in self.feeds:
            feed.delete_old_entries()

    def save_to_disk(self):
        """ Save data to disk, using function get_serializable_data()."""
        feeds = self.get_usual_feed_list()

        try:
            with open('feeds.pickle', 'wb') as fp:
                pickle.dump([f.get_serializable_data() for f in feeds], fp)
                print("Saving data to disk")
        except IOError as ie:
            print("Fail to save data {ie}".format(ie=ie))

    def sig_feed_updated(self, feed):
        """ Callback-function to signal 'updated' from class Feed.
            Emits signal 'feed-updated'.
        """
        self.emit('feed-updated', feed)


def load_from_disk():
    """ Load data from disk.
    :return:
    """
    try:
        with open('feeds.pickle', 'rb') as fp:
            print("Loading data from disk")
            return pickle.load(fp)
    except IOError as ie:
            print("Fail to load data {ie}".format(ie=ie))
