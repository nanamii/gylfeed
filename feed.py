# usr/bin/env python3
# encoding:utf8

from gi.repository import GObject
from time import strftime
import feedparser
import urllib.request
from downloader import Downloader

class Feed(GObject.GObject):
    __gsignals__ = {'updated' : (GObject.SIGNAL_RUN_FIRST, None, ())}

    def __init__(self, url, name, automatic_update=True, notifications=True, raw_feed=None, has_icon=None, icon=None):
        GObject.GObject.__init__(self)
        self.url = url
        self.name = name
        self.automatic_update = automatic_update
        self.notifications = notifications
        self.new_entries = []
        self.has_icon = has_icon
        self.icon = icon
        self.raw_feed = raw_feed
        if raw_feed is None:
            self.download_data()

    def download_data(self):
        downloader = Downloader()
        document = downloader.download(self.url)
        document.connect('finish', self.parse)

    def parse(self, document):
        self.raw_feed = feedparser.parse(document.data)
        if self.raw_feed.bozo == 0:
            self.set_readtag(self.raw_feed)
            print(self.raw_feed.entries[0].read)

            try:
                if self.raw_feed.feed.icon:
                    self.has_icon = True
                    url = self.raw_feed.feed.icon
                    logo_raw = urllib.request.urlretrieve(url)
                    logo = logo_raw[0]
                    self.icon = logo
            except AttributeError as aerr:
                print(aerr)


    def update(self):
        downloader = Downloader()
        document = downloader.download(self.url)
        document.connect('finish', self.parse_update)

    def parse_update(self, document):
        print("parse_update in feed")
        if self.raw_feed:
            if document:
                try:
                    new_raw_feed = feedparser.parse(document.data)
                    self.compare_entries(new_raw_feed)
                    #hier noch überlegen, in welchem Fall signal abgesetzt wird !!!
                    self.emit('updated')
                except AttributeError as aerror:
                    print(aerror)

    # wird durch update aufgerufen
    def compare_entries(self, new_raw_feed):

        self.new_entries = []
        for new_entry in new_raw_feed.entries:
                if new_entry.id not in [entry.id for entry in self.raw_feed.entries]:
                    self.new_entries.append(new_entry)

        try:
            if new_raw_feed.entries[0].published_parsed:
                self.new_entries.sort(key=lambda entry:entry["published_parsed"], reverse=True)
                self.raw_feed.entries = self.new_entries + self.raw_feed.entries
                self.raw_feed.feed.published_parsed = new_raw_feed.feed.published_parsed

            else:
                self.new_entries.sort(key=lambda entry:entry["updated_parsed"], reverse=True)
                self.raw_feed.entries = self.new_entries + self.raw_feed.entries
                self.raw_feed.feed.updated_parsed = new_raw_feed.feed.updated_parsed
        except AttributeError as ae:
            print(ae)

        # getestet, i.O.
        for entry in self.new_entries:
            entry["read"] = False

    def get_entries(self):
        if self.raw_feed:
            entries = []
            for entry in self.raw_feed.entries:
                date_string = self._date_to_string(entry.updated_parsed)
                entries.append((entry.title, entry.summary, date_string, entry.id, self))
            return entries

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_num_of_new_entries(self):
        return len(self.new_entries)

    def get_num_of_unread(self):
        num=0
        for entry in self.raw_feed.entries:
            if entry.read == False:
                num = num+1
        return num

    def _is_modified(self, feed):
        return feed.status != '304' and feed.feed

    def _date_to_string(self, date_struct):
        #return strftime("%FT%T%z", date_struct)
        return strftime("%a, %d.%b.%Y, %R", date_struct)

    def get_serializable_data(self):
        return (self.url, self.name, self.automatic_update, self.notifications, self.raw_feed, self.has_icon, self.icon)

    def set_readtag(self, feed):
        for entry in feed.entries:
            entry["read"] = False

    def set_entry_is_read(self, entry_id):
        for entry in self.raw_feed.entries:
            if entry.id == entry_id:
                entry["read"] = True
                print("in Feed auf TRUE gesetzt!!")
