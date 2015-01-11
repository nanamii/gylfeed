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
    __gsignals__ = {'feed-updated' : (GObject.SIGNAL_RUN_FIRST, None, ())}


    def __init__(self):
        GObject.GObject.__init__(self)
        self.feeds = []

    def create_feed(self, url, feed_name):
        feed = Feed(url, feed_name)
        feed.connect('updated', self.sig_feed_updated)
        self.feeds.append(feed)
        feed.update()

    def count_Feeds(self):
        return len(self.feeds)

    def print_FeedTitles(self):
        for feed in self.raw_feeds:
            for title_num, entry in enumerate(feed.entries, start=1):
                entry_str = entry.title
                print("TitleNr. {nr} -> {entry} \n".format(
                    nr=title_num, entry=entry_str))
                print("published: {date} \n".format(date= entry.published))


    def update(self):
        latestFeedList = []
        for feed in self.raw_feeds:
            latestFeedList.append(feedparser.parse(feed.href))

        for feed in latestFeedList:
            for xfeed in self.raw_feeds:
                if feed.href == xfeed.href:
                    self.compare_entries(feed, xfeed)
                else:
                    print("Keinen übereinstimmenden Feed gefunden")


    def compare_entries(self, latest_feed, safed_feed):
        print(latest_feed.href, safed_feed.href)
        templist = []
        for cur_entry in latest_feed.entries:
                if cur_entry["id"] not in [entry["id"] for entry in safed_feed.entries]:
                    templist.append(cur_entry)
                    print(cur_entry["id"])

        templist.sort(key=lambda entry:entry["published_parsed"], reverse=True)
        safed_feed.entries = templist + safed_feed.entries


    def save_to_Disk(self):
        try:
            with open ('feeds.pickle', 'wb') as fp:
                pickle.dump(self,fp)
                print("Saving data to disk")
        except IOError as ie:
            print("Fail to save data {ie}".format(ie=ie))

    def sig_feed_updated(self, feed):
        self.emit('feed-updated')


def load_from_Disk():
    try:
        with open('feeds.pickle', 'rb') as fp:
            print("Loading data from disk")
            return pickle.load(fp)
    except IOError as ie:
            print("Fail to load data {ie}".format(ie=ie))


