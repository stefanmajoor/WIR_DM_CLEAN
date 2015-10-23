import sqlite3

conn = sqlite3.connect("articles.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM article')
rows = cursor.fetchall()
words = []
for row in rows:
    source = row['html']
    words.extend(source.split())
conn.close()
print len(words)