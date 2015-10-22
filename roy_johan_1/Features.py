__author__ = 'Roy van den Hurk, Johan Munneke'

import sqlite3
from Config import *
import random


class Features:
    def __init__(self):
        pass  # for testing
        self.authors = {}
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM article WHERE isEconomic=1')
        rows = cursor.fetchall()
        # TODO: use actual rows
        for row in rows:
            author = self.authors[row['author']] or {}
            author.count = (author.count or 0) + 1
            author.value = (author.value or 0) + row['pos/neg']
            self.authors[row['author']] = author

    def getAuthorValue(self, author):
        return (random.random() - 0.5) * 2

    def getTfIdfValue(self, article):
        sum = sum([1 for x in article.tf_idf if article.tf_idf[x] > MIN_TF_IDF]) * self.econimcalSentiment(
            article) / article.length

    def getTitleValue(self, article):
        pass

    def econimcalSentiment(self, article):
        return 1


'''
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM article WHERE author=?',(author))
        rows = cursor.fetchall()
'''

