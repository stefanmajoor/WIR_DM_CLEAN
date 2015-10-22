import sqlite3

class Mapper:
    def __init__(self):
        self.connection = sqlite3.connect('../testCollection.db')

    def getAllArticles(self):
        # See if we already indexed this url
        c = self.connection.cursor()

        c.execute('''
            SELECT * FROM article WHERE isEconomic = 0  ORDER BY id ASC LIMIT 150
        ''')


        while True:
            article = c.fetchone()
            if article == None:
                break
            yield article

        c.close()
        return