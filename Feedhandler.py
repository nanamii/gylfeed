#!usr/bin/env python3
# encoding:utf8

""" Testmodule for parsing feeds. """

import feedparser
import pprint
import pickle


class Feedhandler():
    """ Handles different feeds. """
    def __init__(self):
        self.feedList = []

    def add_Feed(self, url):
        new_Feed = feedparser.parse(url)
        self.feedList.append(new_Feed)

    def update_Feed(self, feed_Num):
        self.feedList.append(feedparser.parse(self.get_FeedURL(feed_Num)))

    def get_FeedURL(self, feed_Num):
        return self.feedList[feed_Num]["feed"]["title_detail"]["base"]

    def count_Feeds(self):
        return len(self.feedList)

    def print_FeedTitles(self):
        for feed in self.feedList:
            for title_num, entry in enumerate(feed["entries"], start=1):
                entry_str = entry["title"]
                print("TitleNr. {nr} -> {entry}".format(
                    nr=title_num, entry=entry_str)
                )

    def update(self):
        latestFeedList = []
        for feed in self.feedList:
            latestFeedList.append(feedparser.parse(feed["href"]))

        for feed in latestFeedList:
            if feed
            for entry in feed["entries"]:
                if entry["id"] not in self.feedList["entries"]:
                    self.feedList.append()


    def save_to_Disk(self):
        try:
            with open ('feeds.pickle', 'wb') as fp:
                pickle.dump(self,fp)
                print("Saving data to disk")
        except IOError as ie:
            print("Fail to save data" + str(ie))


def load_from_Disk():
    try:
        with open('feeds.pickle', 'rb') as fp:
            print("Loading data from disk")
            return pickle.load(fp)
    except IOError as ie:
            print("Fail to load data" +str(ie))

#fm = Feedhandler()
#fm.add_Feed("http://rss.sueddeutsche.de/rss/Muenchen")
#fm.add_Feed("http://golem.de.dynamic.feedsportal.com/pf/578068/http://rss.golem.de/rss.php?tp=pol&feed=RSS2.0")
#pprint.pprint(fm.feedList)
#pprint.pprint(fm.get_FeedURL(0))
#fm.update_Feed(0)
#pprint.pprint(fm.feedList)
#print(fm.count_Feeds())
#fm.print_FeedTitles()
#fm.save_to_Disk()
fh = load_from_Disk()
fh.print_FeedTitles()
pprint.pprint(fh.update())

