#!usr/bin/env python3
# encoding:utf8

""" Testmodule for parsing feeds. """

import feedparser
import pprint


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

fm = Feedhandler()
fm.add_Feed("http://rss.sueddeutsche.de/rss/Muenchen")
fm.add_Feed("http://golem.de.dynamic.feedsportal.com/pf/578068/http://rss.golem.de/rss.php?tp=pol&feed=RSS2.0")
pprint.pprint(fm.feedList)
pprint.pprint(fm.get_FeedURL(0))
#fm.update_Feed(0)
#pprint.pprint(fm.feedList)
print(fm.count_Feeds())
fm.print_FeedTitles()

