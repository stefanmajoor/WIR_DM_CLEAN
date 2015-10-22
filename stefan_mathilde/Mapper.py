import sqlite3

class Mapper:

    def __init__(self):
        self.connection = sqlite3.connect('articles.db')

    def saveArticle(self, article, isEconomic):
        if self.hasUrl(article.url):
            return


        c = self.connection.cursor()
        c.execute('''
            INSERT INTO article (source, url, title, date, author, html, isEconomic)
            VALUES(?,?,?,?,?,?,?)
        ''', [article.sourceId, article.url, article.title, str(article.date), str(article.author), str(article.html), isEconomic])
        self.connection.commit()
        c.close()

    '''
    Check if an url exists in the database
    '''
    def hasUrl(self, url):
        # See if we already indexed this url
        c = self.connection.cursor()
        c.execute('''
            SELECT * FROM article WHERE url = ?
        ''', [url]);

        # we already fetched it -> do not save again
        if c.fetchone() != None:
            c.close()
            return True
        c.close()
        return False
