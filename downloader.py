# usr/bin/env python3
# encoding:utf8

from gi.repository import Soup
from gi.repository import GLib
from gi.repository import GObject


class Document(GObject.Object):
    __gsignals__ = {
        'finish': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        GObject.Object.__init__(self)
        self._document = b''

    def _append(self, chunk):
        self._document += chunk

    def _finish(self):
        self.emit('finish')

    @property
    def data(self):
        return self._document


class Downloader():
    def __init__(self):
        self._session = Soup.Session()
        self.CHUNK_SIZE = 16 * 1024
        self.dict_etag = {}
        self.dict_lastmodi = {}

    def download(self, url, check_if_needed=True):
        if check_if_needed:
            # TODO: Async header check.
            header = Soup.Message.new("HEAD", url)
            stream = self._session.send(header)
            stream.read_bytes(self.CHUNK_SIZE)

            etag = self.get_etag(header)
            print("checking etag for ", url)
            if etag and etag == self.dict_etag.get(url):
                return None

            self.dict_etag[url] = etag

            print("checking lastmodi for ", url)
            lastmodi = self.get_lastmodified(header)
            if lastmodi and lastmodi == self.dict_lastmodi.get(url):
                return None

            print("Okay, fucked up.")
            self.dict_lastmodi[url] = lastmodi

        return self.get_data(url)

    def get_data(self, url):
        message = Soup.Message.new("GET", url)
        document = Document()
        stream = self._session.send_async(
            message, callback=self._get_data_deferred, user_data=document
        )
        return document


    def _get_data_deferred(self, session, result, document):
        stream = session.send_finish(result)
        stream.read_bytes_async(
            self.CHUNK_SIZE, 0, callback=self.a_callback, user_data=document
        )

    def a_callback(self, source, result, document):
        bytes_ =  source.read_bytes_finish(result)
        data = bytes_.get_data()
        if not data:
            document._finish()
            return

        document._append(data)
        source.read_bytes_async(
            self.CHUNK_SIZE, 0, callback=self.a_callback, user_data=document
        )

    def get_etag(self, header):
        return header.response_headers.get("Etag")

    def get_lastmodified(self, header):
        return header.response_headers.get("Last-Modified")


if __name__ == '__main__':
    loader = Downloader()
    document = loader.download("https://www.google.de")
    document.connect("finish", lambda doc: print(doc.data, type(doc.data)))

    loop = GLib.MainLoop()
    loop.run()
