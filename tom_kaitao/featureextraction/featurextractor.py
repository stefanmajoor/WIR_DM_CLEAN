import math
import sqlite3

from Config import *


class FeatureExtractor:
    def __init__(self):
        self.articles = []
        self.blobs = []  # TODO: create blobs
        self.conn = sqlite3.connect(DATABASE_URL)
        self.idf = {}

    def set_training_data(self, articles):
        self.articles = articles
        self.blobs = []
        for article in articles:
            self.blobs.append(article.textBlob)
            for word in article.tf():
                self.idf[word] = self.idf.get(word, 0) + 1
        for word in self.idf:
            self.idf[word] = 1 + math.log(len(self.blobs) / float((1 + self.idf[word])))


    def get_features(self, article):
        features = Features()
        features.article_id = article.index
        features.author = article.author
        features.date = article.date
        features.title = article.title
        features.length = len(article.textBlob)
        features.publisher = article.publisher
        features.companies = article.companies
        features.tf = article.tf()
        features.tf_idf = self.tf_idf(article)
        return features

    def tf_idf(self, article):
        tf_idf = {}
        tf = article.tf()
        for word in tf:
            tf_idf[word] = self.idf[word] * tf[word]
        return tf_idf


class Features:
    def __init__(self):
        self.article_id = None
        self.tf_idf = None
        self.author = None
        self.date = None
        self.title = None
        self.length = None
        self.publisher = None
        self.companies = None
        self.tf = None