#! usr/bin/env python
# encoding:utf8

import feedparser
import pprint

class feed (dict):
    def __init__(self, url, value=0):
        self.url = url
        self.id = value
    def update(self):
        return feedparser.parse(self.url)
    def print_feed(self):
        print(self.id)


sz_feed = feed("http://rss.sueddeutsche.de/rss/Muenchen",99)
feed_content = sz_feed.update()
pprint.pprint(feed_content)
sz_feed.print_feed()

pprint.pprint(feed_content["entries"][0])


