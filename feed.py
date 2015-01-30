# usr/bin/env python3
# encoding:utf8

from gi.repository import GObject
from time import strftime
import feedparser

class Feed(GObject.GObject):
    __gsignals__ = {'updated' : (GObject.SIGNAL_RUN_FIRST, None, ())}


    def __init__(self, url, name, automatic_update=True, notifications=True, raw_feed=None):
        GObject.GObject.__init__(self)
        self.url = url
        self.name = name
        self.automatic_update = automatic_update
        self.notifications = notifications
        self.raw_feed = raw_feed
        if raw_feed is None:
            self.parse()

    def parse(self):
        self.raw_feed = feedparser.parse(self.url)


    def update(self):
        print("update function in feed")
        if self.raw_feed:
            try:
                new_raw_feed = feedparser.parse(self.url, self.raw_feed.etag)
                if self._is_modified(new_raw_feed):
                    new_raw_feed.entries.extend(self.raw_feed.entries)
                    self.raw_feed = new_raw_feed
                #hier noch überlegen, in welchem Fall signal abgesetzt wird !!!
                self.emit('updated')
            except AttributeError as aerror:
                print(aerror)
                self.update_no_etag()

    def update_no_etag(self):
        try:
            new_raw_feed = feedparser.parse(self.url)
            #print(new_raw_feed)
            # Achtung!! Hier noch Vergleichsoperator anpassen, eigentlich >
            if new_raw_feed.feed.published_parsed > self.raw_feed.entries[0].published_parsed:
                print("neue entries!!!")
                self.compare_entries_no_etag(new_raw_feed)
                self.emit('updated')
            else:
                print("keine neuen entries")
        except IOError as error:
            print(error)

    # wird durch update_no_etag aufgerufen
    def compare_entries_no_etag(self, new_raw_feed):
        templist = []
        for new_entry in new_raw_feed.entries:
                if new_entry.id not in [entry.id for entry in self.raw_feed.entries]:
                    templist.append(new_entry)

        templist.sort(key=lambda entry:entry["published_parsed"], reverse=True)
        self.raw_feed.entries = templist + self.raw_feed.entries
        self.raw_feed.feed.published_parsed = new_raw_feed.feed.published_parsed


    def get_entries(self):
        if self.raw_feed:
            entries = []
            for entry in self.raw_feed.entries:
                date_string = self._date_to_string(entry.updated_parsed)
                entries.append((entry.title, entry.summary, date_string))
            return entries

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def _is_modified(self, feed):
        return feed.status != '304' and feed.feed


    def _date_to_string(self, date_struct):
        #return strftime("%FT%T%z", date_struct)
        return strftime("%a, %d.%b.%Y, %R", date_struct)

    def get_serializable_data(self):
        return (self.url, self.name, self.automatic_update, self.notifications, self.raw_feed)



if __name__ == '__main__':
    f = Feed(url="http://rss.golem.de/rss.php?tp=foto&feed=ATOM1.0", name="Golem")
    print(f.get_entries())
    f.parse()
    print(f.get_entries())
    f.update()
