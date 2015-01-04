# usr/bin/env python3
# encoding:utf8



class Feed():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.entries = []
