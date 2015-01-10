# usr/bin/env python3
# encoding:utf8

from gi.repository import GObject

class Feed():
    __gsignals__ = {'feed-init' : (GObject.SIGNAL_RUN_FIRST, None, ())}
    
    def __init__(self, url, name):
        GObject.GObject.__init__(self)
        self.url = url
        self.name = name
        self.entries = []
        self.emit('feed-init')
