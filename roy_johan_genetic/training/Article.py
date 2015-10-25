__author__ = 'Roy van den Hurk, Johan Munneke'

import sqlite3

from bs4 import BeautifulSoup

from textblob import TextBlob

from Config import *


class Article:
    def __init__(self, index, publisher, title, date, author, text, companies, label):
        self.textBlob = TextBlob(self.clean_html(text))
        self.text = self.clean_html(text)
        self.title = title
        self.author = author
        self.date = date
        self.publisher = publisher
        self.index = index
        self.companies = companies
        self.tf_cache = None
        self.label = label

    def tf(self):
        if self.tf_cache:
            return self.tf_cache
        self.tf_cache = {}
        words = self.textBlob.words
        for word in words:
            self.tf_cache[word] = self.tf_cache.get(word, 0) + 1
        return self.tf_cache

    @staticmethod
    def from_sql():
        print 'TODO don"t limit SQL'
        conn = sqlite3.connect(DATABASE_URL)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM article WHERE isEconomic=1 AND date!="None" LIMIT 100')
        rows = cursor.fetchall()
        articles = []
        for row in rows:
            article = Article(row['id'], row['source'], row['title'], row['date'], row['author'], row['html'], row['companies'], row['label'])
            articles.append(article)
        conn.close()
        return articles

    def clean_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.text