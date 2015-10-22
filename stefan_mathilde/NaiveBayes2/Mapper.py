import sqlite3
import os

class Mapper:

    def __init__(self):

        self.connection = sqlite3.connect(os.path.dirname(__file__) + '/trainingsCollection.db')
        self.cursor = self.connection.cursor()

    def createTable(self):
        c = self.connection.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "terms" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "token" text NOT NULL,
              "isEconomic" integer NOT NULL,
              "count" integer NOT NULL
            );
        ''')
        c.execute('''DELETE FROM terms''')
        self.connection.commit()
        c.close()

    def getArticleCount(self):
        c = self.connection.cursor()
        c.execute('''SELECT COUNT(*) from article''')
        count = c.fetchone()
        self.connection.commit()
        c.close()
        return count[0]

    def getArticleCountClass(self, _class):
        c = self.connection.cursor()
        c.execute('''SELECT COUNT(*) from article WHERE isEconomic = ?''', [_class])
        count = c.fetchone()
        self.connection.commit()
        c.close()
        return count[0]

    def getArticles(self, _class):
        # See if we already indexed this url
        c = self.connection.cursor()

        c.execute('''
            SELECT * FROM article WHERE isEconomic = ? ORDER BY id ASC
        ''', [int(_class)])

        while True:
            article = c.fetchone()
            if article == None:
                break
            yield article

        c.close()
        return


    def saveVocabulary(self, vocabulary, _class):
        c = self.connection.cursor()

        for v in vocabulary:
            c.execute("INSERT INTO terms (token, isEconomic, count) values (?,?,?)", [v, _class, vocabulary[v]])

        self.connection.commit();

    def getTokenCount(self, token, _class):
        c = self.connection.cursor()
        c.execute("SELECT sum(terms.count) FROM terms WHERE token = ? AND isEconomic = ?", [token, _class])

        item = c.fetchone()

        if item[0] == None:
            return 0
        else:
            return item[0]

    def getWordCountCollection(self, _class):
        c = self.connection.cursor()
        c.execute("SELECT sum(terms.count) FROM terms WHERE isEconomic = ?", [_class])

        item = c.fetchone()
        if item[0] == None:
            return 0
        else:
            return item[0]

    def getTokens(self):
        c = self.connection.cursor()
        c.execute('''SELECT isEconomic, token, count FROM terms''')

        while True:
            token = c.fetchone()
            if token == None:
                break
            yield token

        c.close()
        return

