# usr/bin/env python3
# encoding:utf8

from gi.repository import GObject
from time import strftime
import feedparser

class Feed(GObject.GObject):
    __gsignals__ = {'updated' : (GObject.SIGNAL_RUN_FIRST, None, ())}


    def __init__(self, url, name):
        GObject.GObject.__init__(self)
        self.url = url
        self.name = name
        self.raw_feed = ''
        self.parse()


    def parse(self):
        self.raw_feed = feedparser.parse(self.url)


    def update(self):
        if self.raw_feed:
            new_raw_feed = feedparser.parse(self.url, self.raw_feed.etag)
            if self._is_modified(new_raw_feed):
                new_raw_feed.entries.extend(self.raw_feed.entries)
                self.raw_feed = new_raw_feed
        #hier noch überlegen, in welchem Fall signal abgesetzt wird !!!
        self.emit('updated')


    def get_entries(self):
        if self.raw_feed:
            entries = []
            for entry in self.raw_feed.entries:
                date_string = self._date_to_string(entry.updated_parsed)
                entries.append((entry.title, entry.summary, date_string))
            return entries



    def _is_modified(self, feed):
        return feed.status != '304' and feed.feed


    def _date_to_string(self, date_struct):
        return strftime("%FT%T%z", date_struct)


if __name__ == '__main__':
    f = Feed(url="http://rss.golem.de/rss.php?tp=foto&feed=ATOM1.0", name="Golem")
    print(f.get_entries())
    f.parse()
    print(f.get_entries())
    f.update()
