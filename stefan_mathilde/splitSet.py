'''
Split the set of articles in two databases: the database with test articles, and the database with trainings articles
'''

import sqlite3
import random

connectionAll = sqlite3.connect('articles.db')
connectionTest = sqlite3.connect('testCollection.db')
connectionTraining = sqlite3.connect('trainingsCollection.db')
dropSql = '''
DROP TABLE IF EXISTS "article";
'''


createSql = '''
CREATE TABLE "article" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "source" text NOT NULL,
  "url" text NOT NULL,
  "title" text NOT NULL,
  "date" text NOT NULL,
  "author" text NOT NULL,
  "html" text NOT NULL,
  "isEconomic" integer NOT NULL
);
'''

# create empty database
for connection in [connectionTest, connectionTraining]:
    c = connection.cursor()
    c.execute(dropSql)
    c.execute(createSql)
    connection.commit()
    c.close()

c = connectionAll.cursor()

c.execute('''
    SELECT * FROM article
''')

cursorTest = connectionTest.cursor()
cursorTraining = connectionTraining.cursor()

i = 0
while True:
    article = c.fetchone()
    if article == None:
        break

    if random.random() < 0.3:
        articleCursor = cursorTest
    else:
        articleCursor = cursorTraining

    articleCursor.execute('''
        INSERT INTO article (id, source, url, title, date, author, html, isEconomic)
        VALUES(?,?,?,?,?,?,?,?)
    ''', article)

    i += 1
    print str(i) + "\n"

connectionTest.commit()
connectionTraining.commit()
cursorTraining.close()
cursorTest.close()

