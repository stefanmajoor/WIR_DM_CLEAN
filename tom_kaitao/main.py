__author__ = 'Tom Nijhof'


from featureextraction import *
from pprint import pprint
import sqlite3
from Function_stock_indexes_V0_4 import *

wordsDB = sqlite3.connect('wordsList.db')
wDBquery = wordsDB.cursor()
wDBquery2 = wordsDB.cursor()

artDB = sqlite3.connect('articlesMagic.db')
artDBquery = artDB.cursor()
artDBquery2 = artDB.cursor()

newArt = sqlite3.connect('articles.db')
anDBquery = newArt.cursor()

newArt2 = sqlite3.connect('articlesTest.db')
anDBquery2 = newArt.cursor()

wordsDB.execute('''create table customers (id INTEGER PRIMARY KEY, name TEXT, pos INTEGER, neg INTEGER, neu INTERGER, value INTEGER, isthisshitpos TEXT)''')
artDB.execute('''create table customers (id INTEGER PRIMARY KEY, realID TEXT, name INTEGER, pos INTEGER, neg INTEGER, neu INTERGER)''')
	
def addWord(name, pos):
		_x = wDBquery.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchone()

		if _x:
			_x = _x[0]
			if pos is 2:
				
				_y=int(wDBquery.execute("SELECT pos FROM customers WHERE name = ?", (name,)).fetchone()[0]) +1
				wDBquery.execute("UPDATE customers SET pos =? WHERE name = ?", (_y, name))
			elif pos is 0:
				_y=int(wDBquery.execute("SELECT neg FROM customers WHERE name = ?", (name,)).fetchone()[0]) +1
				wDBquery.execute("UPDATE customers SET neg =? WHERE name = ?", (_y, name))
			else:
				_y=int(wDBquery.execute("SELECT neu FROM customers WHERE name = ?", (name,)).fetchone()[0]) +1
				wDBquery.execute("UPDATE customers SET neu =? WHERE name = ?", (_y, name))
		else:
			if pos is 2:
				wDBquery.execute('''INSERT INTO customers (name, pos, neg, neu, value, isthisshitpos) VALUES (?, ?, ?, ?, ?,?)''',(name, 1, 0, 0, 0, "POS"))
			elif pos is 1:
				wDBquery.execute('''INSERT INTO customers (name, pos, neg, neu, value, isthisshitpos) VALUES (?, ?, ?, ?, ?,?)''',(name, 0, 0, 1, 0, "NEUT"))
			else:
				wDBquery.execute('''INSERT INTO customers (name, pos, neg, neu, value, isthisshitpos) VALUES (?, ?, ?, ?, ?,?)''',(name, 0, 1, 0, 0, "NEG"))
			_x = wDBquery.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchone()[0]

		return int(_x)

def addArticle(realID, names, pos):
	_x = artDBquery.execute("SELECT name FROM customers WHERE realID = ?", (realID,)).fetchone()
	if _x:
		_y = ":unicornblood:".join([str(_x[0]), str(names)]);
		artDBquery.execute("UPDATE customers SET name =? WHERE realID = ?", (_y, realID))
	else:
		if pos is 2:
			artDBquery.execute('''INSERT INTO customers (realID, name, pos,neg, neu) VALUES (?, ?, ?, ?,?)''',(realID, names, 1,0,0))
		elif pos is 0:
			artDBquery.execute('''INSERT INTO customers (realID, name, pos,neg,neu) VALUES (?, ?, ?, ?,?)''',(realID, names, 0,1,0))
		else:
			artDBquery.execute('''INSERT INTO customers (realID, name, pos,neg,neu) VALUES (?, ?, ?, ?,?)''',(realID, names, 0,0,1))
    

articles = Article.from_sql()
featureExtractor = FeatureExtractor()
featureExtractor.set_training_data(articles)
print 'Done loading articles'
dkdfk = 0
countPos = 200
countNeg = 200
countNeu = 200
oldDate = ""
print len(articles), " articles wil be scanned"
maanden = {"Jan": 1,"Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,"Oct":10,"Nov":11,"Dec": 12}
for article in articles:
	dkdfk += 1
	_var = vars(featureExtractor.get_features(article));
	_artID = _var['article_id']
	_pos = False;
	_run = False
	_words = _var['tf'].keys()
	_articleN = 0;
	_date = _var['date']
	_companie = _var['companies']
	_dateList = _date.split()
	_day = int(_dateList[1])
	_moth = int(maanden[_dateList[2]])
	_year = int(_dateList[3])
	if _date is oldDate:
		continue
	else:
		oldDate = _date[:]
	if _year > _day:
		try:
			_koers = StockIR(_day, _moth, _year, "^NDX")[0]["today"]
		except:
			_koers = 0;
	else:
		try:
			_koers = StockIR(_year, _moth, _day, "^NDX")[0]["today"]
		except:
			_koers = 0
	if _koers >= 0.01:
		_pos = 2;
		
		if countPos > 100:
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("POS", _artID))
			_run = True
			countPos -= 1
		elif countPos > 0:
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("POS", _artID))
			countPos -= 1
		else:
			continue
	elif _koers <= -0.01:
		_pos = 0;
		
		if countNeg > 100:
			countNeg -= 1
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("NEG", _artID))
			_run = True
		if countNeg > 0:
			countNeg -= 1
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("NEG", _artID))
		else:
			continue
	elif float(_koers) is not 0.0:
		_pos = 1
		
		if countNeu > 100:
			countNeu -= 1
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("NEUT", _artID))
			_run = True
		elif countNeu > 0:
			countNeu -= 1
			anDBquery.execute("UPDATE article SET label =? WHERE id = ?", ("NEUT", _artID))
		else:
			continue
	else:
		continue
	if  _run:
		for i in _words:
			try:
				if _pos is 2:
					_articleN=_articleN+pow(3,addWord(str(i), _pos))
				elif _pos is 1:
					_articleN=_articleN+pow(3,addWord(str(i), _pos))-1
			except:
				print "cannot make a string out of ", i
				
		addArticle(str(_articleN),str(_artID), _pos);

wordsDB.commit()
artDB.commit()
newArt.commit()
print "done with part 1"


