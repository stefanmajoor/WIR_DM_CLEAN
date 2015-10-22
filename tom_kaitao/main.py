import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from roy_johan_1 import *

from pprint import pprint
import sqlite3
from Function_stock_indexes_V0_4 import *

wordsDB = sqlite3.connect('wordsList.db')
wDBquery = wordsDB.cursor()
wDBquery2 = wordsDB.cursor()

artDB = sqlite3.connect('articlesMagic.db')
artDBquery = artDB.cursor()
artDBquery2 = artDB.cursor()

'''
Creating tables in the database wordsList and articlesMagic.
*wordsList: A list of all the words with 2 counter; appierence in positief articles and appierence in negatief articels.
*articlesMagic: has an realID, this ID is unique for the every combination of words.
'''
wordsDB.execute('''create table customers (id INTEGER PRIMARY KEY, name TEXT, pos INTEGER, neg INTEGER, value INTEGER)''')
artDB.execute('''create table customers (id INTEGER PRIMARY KEY, realID TEXT, name INTEGER, pos INTEGER, neg INTEGER)''')

def addWord(name, pos):
        _x = wDBquery.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchone()

        if _x:
            _x = _x[0]
            if pos:

                _y=int(wDBquery.execute("SELECT pos FROM customers WHERE name = ?", (name,)).fetchone()[0]) +1
                wDBquery.execute("UPDATE customers SET pos =? WHERE name = ?", (_y, name))
            else:
                _y=int(wDBquery.execute("SELECT neg FROM customers WHERE name = ?", (name,)).fetchone()[0]) +1
                wDBquery.execute("UPDATE customers SET neg =? WHERE name = ?", (_y, name))
        else:
            if pos:
                wDBquery.execute('''INSERT INTO customers (name, pos, neg, value) VALUES (?, ?, ?, ?)''',(name, 1, 0, 0))
            else:
                wDBquery.execute('''INSERT INTO customers (name, pos, neg, value) VALUES (?, ?, ?, ?)''',(name, 0, 1, 0))
            _x = wDBquery.execute("SELECT id FROM customers WHERE name = ?", (name,)).fetchone()[0]

        return int(_x)

def addArticle(realID, names, pos):
    _x = artDBquery.execute("SELECT name FROM customers WHERE realID = ?", (realID,)).fetchone()
    if _x:
        _y = ":unicornblood:".join([str(_x[0]), str(names)]);
        artDBquery.execute("UPDATE customers SET name =? WHERE realID = ?", (_y, realID))
    else:
        if pos:
            artDBquery.execute('''INSERT INTO customers (realID, name, pos,neg) VALUES (?, ?, ?, ?)''',(realID, names, 1,0))
        else:
            artDBquery.execute('''INSERT INTO customers (realID, name, pos,neg) VALUES (?, ?, ?, ?)''',(realID, names, 0,1))
    

articles = Article.from_sql()
featureExtractor = FeatureExtractor()
featureExtractor.set_training_data(articles)

print 'Done loading articles'
print len(articles), " articles wil be scanned"
for article in articles:
    _var = vars(featureExtractor.get_features(article));
    _artID = _var['article_id']
    _pos = False;
    _words = _var['tf'].keys()
    _articleN = 0;
    _date = _var['date']
    _companie = _var['companies']
    _dateList = _date.split()[0].split('-')
    _day = int(_dateList[2])
    _moth = int(_dateList[1])
    _year = int(_dateList[0])

    if _year > _day:
        try:
            _koers = StockIR(_day, _moth, _year, "GOOG")[0]["today"]
        except:
            _koers = 0;
    else:
        try:
            _koers = StockIR(_year, _moth, _day, "GOOG")[0]["today"]
        except:
            _koers = 0
    if _koers >= 0.02:
        _pos = True;
    else:
        _neg = False;
    if  _koers is not 0:
        for i in _words:
            try:
                _articleN=_articleN+pow(2,addWord(str(i), _pos))
            except:
                print "cannot make a string out of ", i

        addArticle(str(_articleN),str(_artID), _pos);

wordsDB.commit()
artDB.commit()
print "done with part 1"

'''
Every article is its own object. In that object is a list of all words that apair in the article and a uniqe value based on these apair words.
The value will only be the same for 2 article if and only if the article have the same words in them.
If
'''

#Look how many articles are positief and how many are negatief
artDBquery.execute('SELECT pos from customers')
_ptot= 0
for i in artDBquery:
    _ptot += i[0]

artDBquery.execute('SELECT neg from customers')
_ntot= 0
for i in artDBquery:
    _ntot += i[0]

#Validated every word. This is done be taking the difference in ratio pos articels with the word with the ratio neg. art. with the word
wDBquery.execute('SELECT id, pos, neg FROM customers')
for i in wDBquery:
        _pp = float(i[1])
        _nn = float(i[2])
        x=abs(_pp/_ptot - _nn/_ntot)
        _l = (x,i[0])
        wDBquery2.execute('UPDATE customers SET value = ?  WHERE id = ?', _l)





#We take the maximum ID and sort the words by smallest value first
lenOfValWor = wDBquery.execute('SELECT id FROM customers ORDER BY id DESC LIMIT 1').fetchone()[0]
wDBquery.execute('SELECT id, name FROM customers ORDER BY value')

for u in wDBquery:
    canIDeleteThis = True;
    artDBquery.execute('SELECT realID, pos, neg, id FROM customers')
    for i in artDBquery:
        _goingDown = int(i[0])%pow(2,u[0]+1)
        if _goingDown >= pow(2,u[0]):
            _val = (str(int(i[0])-int(pow(2,u[0]))),)
            if _val[0] is '0':
                    canIDeleteThis = False
                    break
            try:
                _posN, _negN = artDBquery2.execute('SELECT pos, neg FROM customers WHERE realID = ?', _val).fetchone()

                if (min(_posN, _negN) + min(i[1] , i[2])) is not (min(_posN+i[1], _negN+i[2])):
                    canIDeleteThis = False
                    break


            except:
                pass

    if canIDeleteThis:
        wDBquery2.execute('DELETE FROM customers WHERE id = ?', (u[0],))
        artDBquery.execute('SELECT realID, pos, neg, id FROM customers')
        for i in artDBquery:
            _goingDown = int(i[0])%pow(2,u[0]+1)
            if _goingDown >= pow(2,u[0]):
                _newVal = (str(int(i[0])-int(pow(2,u[0]))),)
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
    '''
    for i in range(0,pow(2,lenOfValWor-u-1)):
        for t in range(i*pow(2,u),i*pow(2,u+1)-1):
            cError= min(dictSort[t][0],dictSort[t][1])+min(dictSort[t+pow(2,u+1)][0],dictSort[t+pow(2,u+1)][1]);
            nError = min(dictSort[t][0]+dictSort[t+pow(2,u+1)][0],dictSort[t][1]+dictSort[t+pow(2,u+1)][1]);
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
