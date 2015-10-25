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

'''
Every article is its own object. In that object is a list of all words that apair in the article and a uniqe value based on these apair words.
The value will only be the same for 2 article if and only if the article have the same words in them.
If
'''

#Look how many articles are positief and how many are negatief
artDBquery.execute('SELECT pos from customers')
_ptot= 1
for i in artDBquery:
	_ptot += i[0]

artDBquery.execute('SELECT neg from customers')
_ntot= 1
for i in artDBquery:
	_ntot += i[0]

artDBquery.execute('SELECT neu from customers')
_nntot= 1
for i in artDBquery:
	_ntot += i[0]
	
#Validated every word. This is done be taking the difference in ratio pos articels with the word with the ratio neg. art. with the word
wDBquery.execute('SELECT id, pos, neg, neu FROM customers')
for i in wDBquery:
	_pp = float(i[1])+1
	_nn = float(i[2])+1
	_nnn = float(i[3])+1
	eP = _pp/_ptot * log(_ptot/_pp)
	eN = _nn/_ntot * log(_ntot/_nn)
	eNN = _nnn/_nntot * log(_nntot/_nnn)
	x=abs(eP + eN + eNN)
	state = ""
	if eP > eN and eP > eNN:
		state = "POS"
	elif eN > eP and eN > eNN:
		state = "NEG"
	else:
		state = "NEUT"
	_l = (x,state,i[0])
	wDBquery2.execute('UPDATE customers SET value = ?, isthisshitpos=? WHERE id = ?', _l)





#We take the maximum ID and sort the words by smallest value first
lenOfValWor = wDBquery.execute('SELECT id FROM customers ORDER BY id DESC LIMIT 1').fetchone()[0]
for u in wDBquery:
	print "first Value:", u
wDBquery.execute('SELECT id, name FROM customers ORDER BY value DESC')
isThisTheStart = True
count = 0

print "we will scan ", lenOfValWor, " words"
count = 0
for u in wDBquery:
	count += 1
	canIDeleteThis = True;
	artDBquery.execute('SELECT realID, pos, neg, neu, id FROM customers')
	for i in artDBquery:
		_goingDown = int(i[0])%pow(3,u[0]+1)
		if _goingDown >= pow(3,u[0]):
			_val = (str(int(i[0])-int(pow(3,u[0]))),)
			if _val[0] is '0':
					canIDeleteThis = False
					break
			try:
				_posN, _negN, _neuN = artDBquery2.execute('SELECT pos, neg, neu FROM customers WHERE realID = ?', _val).fetchone()
				
				if (min(_posN, _negN, _neuN) + min(i[1] , i[2], i[3])) is not (min(_posN+i[1], _negN+i[2], _neuN+i[3])):
					canIDeleteThis = False
					break
			except:
				pass
	
	if canIDeleteThis:
		wDBquery2.execute('DELETE FROM customers WHERE id = ?', (u[0],))
		artDBquery.execute('SELECT realID, pos, neg, neu FROM customers')
		for i in artDBquery:
			_goingDown = int(i[0])%pow(3,u[0]+1)
			if _goingDown >= pow(3,u[0]):
				_newVal = (str(int(i[0])-int(pow(3,u[0]))),)
				try:
					art1, pos1, neg1 =artDBquery2.execute('SELECT name, pos, neg FROM customers WHERE realID = ? ', (str(i[0]),)).fetchone()
					oldID, art2, pos2, neg2 =artDBquery2.execute('SELECT id, name, pos, neg FROM customers WHERE realID = ? ', _newVal).fetchone()
					_updatedvalue = (":unicornblood:".join([str(art1), str(art2)]),pos1+pos2,neg1+neg2,_newVal[0],i[0])
					artDBquery2.execute('UPDATE customers SET name = ?, pos = ?, neg = ?, realID =? WHERE realID = ? ', _updatedvalue)
					artDBquery2.execute('DELETE FROM customers WHERE id = ?', (oldID,))
				except:
					artDBquery2.execute('UPDATE customers SET realID =? WHERE realID = ? ', (_newVal[0], i[0]))
	else:
		print "KEEPING ", u
		
	if count % 100 is 0:
		print "we have scanned: ", count, " words"
		print "the time is: ", datetime.datetime.now()
	'''
	for i in range(0,pow(3,lenOfValWor-u-1)):
		for t in range(i*pow(3,u),i*pow(3,u+1)-1):
			cError= min(dictSort[t][0],dictSort[t][1])+min(dictSort[t+pow(3,u+1)][0],dictSort[t+pow(3,u+1)][1]);
			nError = min(dictSort[t][0]+dictSort[t+pow(3,u+1)][0],dictSort[t][1]+dictSort[t+pow(3,u+1)][1]);
			if cError is not nError:
				canIDeleteThis = False;
				break;
		if not canIDeleteThis:
			break;
	#''
	if canIDeleteThis:
			for i in articles:
				i.removeWord(u);
	'''

wordsDB.commit()
artDB.commit()
