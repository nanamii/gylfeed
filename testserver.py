#!/usr/bin/env python3
# encoding: utf8

from flask import Flask, request
from werkzeug.contrib.atom import AtomFeed
from urllib.parse import urljoin
from faker import Factory
import datetime

app = Flask(__name__)
faker = Factory.create('de_DE')
articles = []

class Article:
    def __init__(self):
        self.title = faker.sentence(nb_words=3, variable_nb_words=True)
        self.url = faker.uri()
        self.rendered_text= faker.text()
        self.author = faker.name()
        self.last_update =  datetime.datetime.now()
        self.published = datetime.datetime.now()

def make_external(url):
    return urljoin(request.url_root, url)

@app.route('/')
def recent_feed():
    feed = AtomFeed('My Page', feed_url=request.url, url=request.url_root)
    articles.append(Article())
    for article in articles:
        feed.add(
            article.title, article.rendered_text, content_type='html',
            author=article.author, url=make_external(article.url),
            updated=article.last_update, published=article.published
        )
    return feed.get_response()

if __name__ == '__main__':
    app.run(debug=True)
