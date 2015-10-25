__author__ = 'Roy van den Hurk, Johan Munneke'

import sqlite3

from  bs4 import BeautifulSoup

from textblob import TextBlob

from Config import *


class Article:
    def __init__(self, index, publisher, title, date, author, text, companies):
        self.textBlob = TextBlob(self.clean_html(text))
        self.title = title
        self.author = author
        self.date = date
        self.publisher = publisher
        self.index = index
        self.companies = companies
        self.tf_cache = None

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
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM article WHERE isEconomic=1 AND date!="None"')
        rows = cursor.fetchall()
        articles = []
        for row in rows:
            article = Article(row[0], row[1], row[3], row[4], row[5], row[6], row[8])
            articles.append(article)
        conn.close()
        return articles

    def clean_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.text