__author__ = 'Roy van den Hurk'

import json
import sqlite3
import os

#This stuff should loaded from a DB exported from trainings
words = {}
authorValues = {}
publisherValues = {}

def calculateSentiment(words, features, weights):
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
    value += (features.sentiment[0] * features.sentiment[1]) * weights[3]
    return value
    

def evaluate(features):
    #words = json.loads(WORDS)
    conn = sqlite3.connect(os.path.dirname(__file__) + '/results.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM result')
    row = cursor.fetchone() #should only be 1 row
    words = json.loads(row['words'])
    weights = json.loads(row['weights'])
    publisherValues = json.loads(row['publisher'])
    authorValues = json.loads(row['author'])
    conn.close()
    sentiment = calculateSentiment(words, features, weights)
    return sentiment
    
    