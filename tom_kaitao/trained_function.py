__author__ = 'stefan'
import sqlite3
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from roy_johan_1 import *

wordsDB = sqlite3.connect(os.path.dirname(__file__) +  '/wordsList.db')
wDBquery = wordsDB.cursor()
wDBquery.execute('SELECT name FROM customers')
allGoodWords = []
for i in wDBquery:
    allGoodWords.append(i)

def featureSelection(a):
    derp = dict()
    derp.update(a.tf())
    for i in derp:
        if (i,) not in allGoodWords:
            del a.tf_cache[i]

    return a
