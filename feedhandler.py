#!usr/bin/env python3
# encoding:utf8

""" Testmodule for parsing feeds. """


from gi.repository import Gtk, GObject
import feedparser
import pprint
import pickle
from feed import Feed


class Feedhandler(GObject.GObject):
    """ Handles different feeds. """
    __gsignals__ = {'feed-updated' : (GObject.SIGNAL_RUN_FIRST, None,(GObject.GObject, )),
                    'feed-add-exception' : (GObject.SIGNAL_RUN_FIRST, None, (str, ))}


    def __init__(self):
        GObject.GObject.__init__(self)
        self.feeds = []

    def create_feed(self, url, feed_name, update_switch, notify_switch):
        feed = Feed(url, feed_name, update_switch, notify_switch)
        if feed.raw_feed.bozo == 1:
            self.emit('feed-add-exception', "URL liefert kein Ergebnis, bitte erneut eingeben.")
        if self.feed_exists(url):
            print("Feed bereits vorhanden!!")
            self.emit('feed-add-exception', "Feed bereits vorhanden!")
        else:
            feed.connect('updated', self.sig_feed_updated)
            self.feeds.append(feed)
            feed.update()
            return feed

    def feed_exists(self, url):
        for feed in self.feeds:
            if feed.get_url() == url:
                return True
        return False

    def count_feeds(self):
        return len(self.feeds)


    def update_all_feeds(self, update_button, action):
        for feed in self.feeds:
            feed.update()
        self.save_to_disk()

    def connect_feeds(self):
        for feed in self.feeds:
            feed.connect('updated', self.sig_feed_updated)

    def delete_feed(self, feed):
        for f in self.feeds:
            if f.get_url() == feed.get_url():
                print(self.feeds.index(f))
                self.feeds.pop(self.feeds.index(f))
                print("Feed gelöscht!!!!!")
                print(len(self.feeds))


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


