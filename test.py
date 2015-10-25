import stefan_mathilde.Crawler.Article as A1
import roy_johan_1.Article as A2
import roy_johan_1.Features as f
import roy_johan_1.featurextractor as extraction
import tom_kaitao.trained_function as tf
import roy_johan_genetic.evaluation as e
import sqlite3

artTest = sqlite3.connect('articlesTest.db')
artCurTest = artTest.cursor()

testArticles = [{}]
count = 0
artCurTest.execute('''SELECT source, title, author, date, html, companies, label FROM articles''')
for i in artCurTest:
	testArticles[count] = A2(1, i[0],i[1],i[2],i[3],i[4],i[5],i[6])
	count += 1
extractor = extraction.FeatureExtractor()
'''
For Tom (This part):
use extractor.get_features(b) to get a features object
throw out all bad words from the features.text array
pass that into e.evaluate
For Tom(Training the genetic algorithm):
Goto roy_johan_genetic\training folder in evaluation.py
on line 25 the label should be taken from the database and the limit should be changed to something higher
Then run evaluation.py
Copy results.db to the roy_johan_genetic folder
'''
correct = 0.0
total = 0.0
for i in testArticles
	features = extractor.get_features(i)
	new = e.evaluate(features)
	total += 1
	if new is features['label']:
		correct += 1
		
print "Accuraty is: ", correct/total
