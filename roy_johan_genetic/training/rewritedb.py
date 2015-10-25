import sqlite3

conn = sqlite3.connect("articlesMagic.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM customers WHERE neg != 0')
rows = cursor.fetchall()
rows = []
for row in rows:
    label = 'neg'
    #stupid unicornblood thingy
    articles = row['name'].split(':unicornblood:')
    print articles
conn.close()
print len(words)