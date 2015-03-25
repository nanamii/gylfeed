#!/usr/bin/env python3
# encoding:utf8

from gi.repository import GObject, GLib, Notify, GdkPixbuf
from time import strftime, tzset, mktime, timezone, time
import time
from datetime import datetime
import feedparser
import urllib.request
from downloader import Downloader
import tempfile

DOWNLOADER = Downloader()


class Feed(GObject.GObject):
    __gsignals__ = {
        'created' : (GObject.SIGNAL_RUN_FIRST, None, ()),
        'updated' : (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, url=None, name=None, update_interval=None,
        delete_interval=None, automatic_update=True, notifications=True,
        raw_feed=None, has_icon=None, icon=None, feedhandler=None,
        feedtype='usual'):

        GObject.GObject.__init__(self)

        tzset()

        self.url = url
        self.name = name
        self.automatic_update = automatic_update
        self.notifications = notifications
        self.update_interval = update_interval
        self.delete_interval = delete_interval
        self.new_entries = []
        self.has_icon = has_icon
        self.icon = icon
        self.feedtype = feedtype
        self.is_clicked = False
        self.count_new_entries = 0
        self.raw_feed = raw_feed
        if raw_feed is None:
            self.download_data()

        print("update_interval:", update_interval)
        print("delete_interval:", delete_interval)

        self.update_id = None
        self.add_updater(self.update_interval)

    def add_updater(self, new_update_interval=None):
        if self.update_id is not None:
            GLib.source_remove(self.update_id)
            self.update_id = None

        if new_update_interval:
            interval = self.update_interval*60*1000
            self.update_id = GLib.timeout_add(
                interval, self._update_recurring
            )

    def _update_recurring(self):
        if self.automatic_update:
            print("automatic update für Feed:", self.name)
            self.update()
        # TODO: Return settings.do_auto_update
        return True

    def load_icon(self, url):
        document = DOWNLOADER.download(url, check_if_needed=False)
        document.connect('finish', self._load_icon_deferred)

    def _load_icon_deferred(self, document):
        temp_path = tempfile.mktemp(".icon", "gylfeed-")
        with open(temp_path, "wb") as handle:
            handle.write(document.data)

        print(temp_path)
        self.icon = temp_path
        self.emit('created')

    def download_data(self):
        document = DOWNLOADER.download(self.url, check_if_needed=False)
        document.connect('finish', self.parse)

    def parse(self, document):
        self.raw_feed = feedparser.parse(document.data)
        if self.raw_feed.bozo == 0:
            self.set_read_tag(self.raw_feed)
            self.set_delete_tag(self.raw_feed)
            print(self.raw_feed.entries[0].read)

            try:
                if self.raw_feed.feed.icon:
                    self.load_icon(self.raw_feed.feed.icon)
                    self.has_icon = True
                    # url = self.raw_feed.feed.icon
                    # logo_raw = urllib.request.urlretrieve(url)
                    # logo = logo_raw[0]
                    # self.icon = logo
            except AttributeError as aerr:
                print(aerr)

        if not self.has_icon:
            self.emit('created')

    def update(self):
        print("update called", self.url)
        document = DOWNLOADER.download(self.url)
        if document is not None:
            document.connect('finish', self.parse_update)
        else:
            self.emit("updated")

    def parse_update(self, document):
        print("parse_update in feed")
        if self.raw_feed:
            if document:
                try:
                    new_raw_feed = feedparser.parse(document.data)
                    print("before compare_entries Aufruf")
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
        print("compare_entries in Feed", self.get_name(), "!!!!...new_entries:")
        print("Neue Entries in compare_entries:", len(self.new_entries))

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


        print("NEUEEEEEEE Entries im Feed:", len(self.new_entries))
        if len(self.new_entries) > 0:
            self.set_is_clicked(False)
            self.count_new_entries += len(self.new_entries)
            self.send_notification()
            print("COUNT new entries nach Hochsetzen:", self.count_new_entries)

        #getestet, i.O.
        for entry in self.new_entries:
            entry["read"] = False
            entry["deleted"] = False

    def get_entries(self):
        if self.raw_feed:
            entries = []
            for entry in self.raw_feed.entries:
                stamp = mktime(entry.updated_parsed) - timezone
                dt = datetime.fromtimestamp(stamp)
                date_string = self._date_to_string(dt.timetuple())
                entries.append((entry.title, entry.summary, date_string, entry.id, entry.deleted, self, entry.updated_parsed))
            return entries

    def get_num_of_entries(self):
        num_of_entries = 0

        for entry in self.raw_feed.entries:
            if entry.deleted is False:
                num_of_entries += 1
        return num_of_entries

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_num_of_new_entries(self):
        return len(self.new_entries)

    def get_num_of_unread(self):
        num_of_unread = 0
        for entry in self.raw_feed.entries:
            if entry.read == False and entry.deleted == False:
                num_of_unread += 1
        return num_of_unread

    def get_num_of_counted(self):
        return self.count_new_entries

    def _is_modified(self, feed):
        return feed.status != '304' and feed.feed

    def set_is_clicked(self, clicked):
        self.is_clicked = clicked
        if clicked:
            self.count_new_entries = 0

    def _date_to_string(self, date_struct):
        #return strftime("%FT%T%z", date_struct)
        return strftime("%a, %d.%b.%Y, %R", date_struct)

    def get_serializable_data(self):
        return (self.url, self.name, self.update_interval, self.delete_interval,
                self.automatic_update, self.notifications, self.raw_feed, self.has_icon, self.icon)

    def set_read_tag(self, feed):
        for entry in feed.entries:
            entry["read"] = False

    def set_delete_tag(self, feed):
        for entry in feed.entries:
            entry["deleted"] = False

    def send_notification(self):
        Notify.init("gylfeed")
        msg=Notify.Notification.new(self.get_name(), "   "+ str(self.get_num_of_new_entries())+" new Feed-Messages")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("./graphics/default_icon.png")
        msg.set_image_from_pixbuf(pixbuf)
        msg.set_app_name("Gylfees")
        msg.show()

    def delete_old_entries(self, day_range=None):
        if day_range:
            DAY_RANGE = day_range
        else:
            DAY_RANGE = 30*24*60*60

        min_local_time = time.gmtime(time.time() - DAY_RANGE)

        for entry in self.raw_feed.entries:
            try:
                if entry.published_parsed < min_local_time:
                    entry["deleted"] = True
                else:
                    entry["deleted"] = False
                print("deleted? ", entry.deleted)
            except:
                print("delete_old_entries, except")

    def set_entry_is_read(self, entry_id):
        for entry in self.raw_feed.entries:
            if entry.id == entry_id:
                entry["read"] = True
                print("in Feed auf TRUE gesetzt!!")


class SumFeed(Feed):
    def __init__(self, feedhandler):
        Feed.__init__(self, feedhandler=feedhandler, feedtype="summarized")
        self.feedhandler = feedhandler
        print("SumFeed erstellt")

    def get_entries(self):
        entries = []
        feeds = self.feedhandler.get_usual_feed_list()

        for feed in feeds:
            entries.extend(Feed.get_entries(feed))

        return entries

    def get_num_of_entries(self):
        num_of_entries = 0
        feeds = self.feedhandler.get_usual_feed_list()

        for feed in feeds:
            num_of_entries += Feed.get_num_of_entries(feed)

        return num_of_entries

    def get_num_of_new_entries(self):
        new_entries = 0
        feeds = self.feedhandler.get_usual_feed_list()
        for feed in feeds:
            new_entries += Feed.get_num_of_new_entries(feed)

        return new_entries

    def get_num_of_unread(self):
        num_of_unread = 0
        feeds = self.feedhandler.get_usual_feed_list()

        for feed in feeds:
            num_of_unread += Feed.get_num_of_unread(feed)

        return num_of_unread

    def get_num_of_counted(self):
        counted = 0
        feeds = self.feedhandler.get_usual_feed_list()

        for feed in feeds:
            counted += feed.get_num_of_counted()
        return counted

    def _update_recurring(self):
        return True

    def download_data(self):
        pass

    def get_name(self):
        return "All Feeds"
