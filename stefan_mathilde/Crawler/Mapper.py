import sqlite3
import os
import sys
import os

class Mapper:

    def __init__(self):
        self.feedConnection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/feeds.db')
        self.articleConnection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/articles.db')


    def getFeeds(self):
        c = self.feedConnection.cursor()
        c.execute('SELECT * FROM feeds')

        feeds = c.fetchall()
        c.close()
        

        for feed in feeds:
            yield feed[1]

    def addFeed(self, feed):
        c = self.feedConnection.cursor()
        c.execute('SELECT * FROM feeds WHERE url = ?', [feed])

        if c.fetchone() != None:

            print "already in database"
            c.close()
            return

        c.execute('''
        INSERT INTO "feeds" ("url")
        VALUES (?);''', [feed])

        self.feedConnection.commit()
        c.close()

    def saveArticles(self, articles):
            c = self.articleConnection.cursor()
            for article in articles:
                try:
                    c.execute('''
                        INSERT INTO article (source, url, title, date, author, html, isEconomic, confidence, companies) VALUES (?,?,?,?,?,?, 1, ?, ?)
                    ''', [article.sourceId, article.url, article.title, str(article.date), str(article.author), str(article.html), article.confidence, str(article.companies)])
                except:
                    print "Unexpected error:", sys.exc_info()[0]

            self.articleConnection.commit()

            c.close()

    '''
    Check if an url exists in the database
    '''
    def hasUrl(self, url):
        # See if we already indexed this url
        c = self.articleConnection.cursor()
        c.execute('''
            SELECT * FROM article WHERE url = ?
        ''', [url]);

        # we already fetched it -> do not save again
        if c.fetchone() != None:
            c.close()
            return True
        c.close()
        return False

    def addLink(self, link):
        c = self.feedConnection.cursor()
        c.execute(''' SELECT * from urls WHERE url = ?''', [link]);

        # Link is already added -> so dont add anymore
        if c.fetchone() != None:
            return

        c.execute('''
            INSERT INTO urls (url, done) VALUES (?, 0)
        ''', [link])
        self.feedConnection.commit()
        c.close()

    def findLinksToCheck(self):
        # See if we already indexed this url
        c = self.feedConnection.cursor()
        c.execute('''
            SELECT * FROM urls WHERE done = 0 LIMIT 100
        ''');

        links = c.fetchall()
        c.close()

        for link in links:
            yield link[1]
        return

    def setLinkDone(self, link):
        c = self.feedConnection.cursor()
        c.execute('''update urls SET done = 1 WHERE url = ?''', [link]);
        self.feedConnection.commit()
        c.close()