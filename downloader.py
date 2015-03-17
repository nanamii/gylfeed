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

    def download(self, url):
        message = Soup.Message.new("GET", url)
        stream = self._session.send(message)
        document = Document()
        stream.read_bytes_async(
            self.CHUNK_SIZE, 0, callback=self.a_callback, user_data=document
        )

        return document

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


if __name__ == '__main__':
    loader = Downloader()
    document = loader.download("https://www.google.de")
    document.connect("finish", lambda doc: print(doc.data, type(doc.data)))

    loop = GLib.MainLoop()
    loop.run()
