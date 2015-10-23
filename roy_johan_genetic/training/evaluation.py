__author__ = 'Roy van den Hurk, Johan Munneke'

import csv
import threading
import sqlite3
import sys
import json

from mutators import *
from genetic import *
from tokenizers import *
from Article import *
from featurextractor import *

from nltk.stem.snowball import *

def loadDataSet(limit):
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM article WHERE isEconomic=1 AND date!="None" LIMIT 10') #Tom: verander dit limit
    rows = cursor.fetchall()
    articles = []
    for row in rows:
        #Tom: Hier mis label laden
        article = Article(row['id'], row['source'], row['title'], row['date'], row['author'], row['html'], row['companies'], 'pos' )
        articles.append(article)
    conn.close()
    return articles

def loadWords():
    words = []
    words.extend(loadWordsFromDB('neg.db'))
    words.extend(loadWordsFromDB('neu.db'))
    words.extend(loadWordsFromDB('pos.db'))
    return words

def loadWordsFromDB(db):
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')
    rows = cursor.fetchall()
    words = []
    for row in rows:
        words.append(row['name'])
    conn.close()
    return words
    
def calculateSentiment(features, weights):
    sentiment = 0
    #Words
    for word in features.text:
        try:
            index = words[word]
            sentiment += weights[index]
        except Exception as e:
            #Word has no sentiment value attached, so ignore
            pass
    #The other features
    sentiment += calculateSentimentArticle(features, weights)
    return sentiment
 
def calculateSentimentArticle(features, weights):
    value = 0
    if features.author in authorValues:
        authorValue = authorValues[features.author]
        value += authorValue * weights[0]
    if features.publisher in publisherValues:
        publisherValue = publisherValues[features.publisher]
        value += publisherValue * weights[1]
    value += features.length * weights[2]
    value += (features.sentiment.polarity * features.sentiment.subjectivity) * weights[3]
    return value

def classify(features,weights):
   posCutoff = 0.01
   negCutoff = -0.01
   sentiment = calculateSentiment(features,weights)
   label = 'neu'
   if sentiment > posCutoff:
        label = 'pos'
   elif sentiment < negCutoff:
        label =  'neg'
   return (label, sentiment)    
    
def fitnessFunction(individual):
    correct = 0 
    for features, l in train:
        label, sentiment = classify(features, individual)
        if label == l:
            correct += 1
        else:
            pass
            #print 'Wrongly classified', tokens, ' as ', (label, sentiment)
    return correct / float(len(train))

#TODO: code dup
def evaluate(individual):
    correct = 0 
    for tokens, l in test:
        label, sentiment = classify(tokens, individual)
        if label == l:
            correct += 1
        else:
            pass
            #print 'Wrongly classified', tokens, ' as ', (label, sentiment)
    return correct / float(len(test))
        
def runTest(mutator, fitness, populationSize, length, min , max, retain, random_select, mutate):
    results = []
    genetic = Genetic(mutator, fitness)
    population = genetic.population(populationSize, length, min, max)
    run = 0 
    for iteration in iterations:
        run += 1
        print 'Starting run ', run
        population = genetic.population(populationSize, length, min, max)
        newPop = genetic.evolve(iteration, population)
        ranked = [(genetic.fitness(x), x) for x in newPop]
        ranked = [x[1] for x in sorted(ranked, reverse=True)]
        results.append((genetic.grade(newPop), genetic.fitness(ranked[0]), ranked[0]))
    return results

train = []
test = []
words = {}
iterations = [500]
authorValues = {}
publisherValues = {}

if __name__ == '__main__' :
    print 'loading dataset'
    numNonWordsFeatures = 4
    mWords = loadWords()
    articles = loadDataSet(10)
    train = []
    print 'extracting features'
    featureextractor = FeatureExtractor()
    for article in articles:
        features = featureextractor.get_features(article)
        #Tom: mWords moet alle belangrijke woorden bevatten hier dan worden de andere woorden eruitgegooid
        #features.text = tokenize(features.text, tokenizer=RegexpTokenizer('[a-zA-Z]\w+'), stemmer=PorterStemmer())
        features.text = [x for x in features.text if x in mWords]
        features = (features, features.label)
        train.append(features)
    l = int(len(train) * 0.8)
    test = train[l:]
    train = train[:l]
    wordId = 4
    print 'generating data cache'
    for word in mWords:
        if not word in words:
            words[word] = wordId
            wordId += 1
    
    for features, label in train:
        author = features.author
        if author not in authorValues:
            articlesByAuthor = [a for a, label in train if a.author == author]
            pos = sum(1 for a in articlesByAuthor if a.label == 'pos')
            neg = sum(1 for a in articlesByAuthor if a.label == 'neg')
            authorValue = (pos - neg) / float((pos + neg))
            authorValues[author] =  authorValue
        publisher = features.publisher
        if publisher not in publisherValues:
            articlesByPublisher = [a for a, label in train if a.publisher == publisher]
            pos = sum(1 for a in articlesByPublisher if a.label == 'pos')
            neg = sum(1 for a in articlesByPublisher if a.label == 'neg')
            publisherValue = (pos - neg) / float((pos + neg))
            publisherValues[publisher] = publisherValue
    print '#features=', wordId
    print '#articles=', len(train)
    
    
    results = runTest(RandomMutator(), fitnessFunction, 100, wordId, -100, 250, 0.2, 0.5 , 0.05)
    sys.stdout = open('accuracy.txt', 'w')
    print 'accuracy: ', evaluate(results[len(results) - 1][2])
    print 'done'
    weights = results[len(results) - 1][2]
    #Create DB of results (JSON)
    conn=sqlite3.connect('results.db')
    c = conn.cursor()
    c.execute('DELETE FROM result')
    c.execute('INSERT INTO result VALUES (?,?,?,?)', (json.dumps(authorValues),json.dumps(publisherValues) ,json.dumps(weights),json.dumps(words)))
    conn.commit()
    conn.close()


   
