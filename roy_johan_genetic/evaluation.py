__author__ = 'Roy van den Hurk'

import json

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
    
#This stuff should definitely be loaded from a  DB exported from training
weights = [95.83380390580004, 93.16458293907283, 43.14583028775809, 31.156434913389575, -65.56159717217369, 84.80178594653788, 62.646163623040735, -35.297034382662915, 27.137223287937886, -52.619916497417464, 29.456790181731407, -71.07775713162093, -49.737330792992296, -26.415492378237886, -10.01207228561691, 34.17852474807253, 28.664483796507596, -89.60615749427087, 53.888957356132295, -42.931542530071276, 54.938360942302154, -15.226341086317944, 22.257818047633975, -93.60189789864882, -33.5983079201451, -67.935368660903, 93.26314591946735, -78.60464775596637, -45.965753825939636, 59.94926267749631, 83.9564789264391, -5.833726726861002, 96.19439433171456, -73.45805971521611, -0.5182441053803473, 29.711491490170403, -98.44304952985159, 35.66496560971041, -32.222327200004486, 97.69283827535767, 72.15016605583483, 72.1516471788905, 41.732120780974185, -49.32127539918119, 24.406894625084448, 84.08136992534762]
WORDS = '{ \
"Even": 29 , \
"United": 25 ,\
"For": 13 ,\
"people": 7 ,\
"correction": 45 ,\
"global": 42 ,\
"helped": 15 ,\
"ended": 44 ,\
"economic": 27 ,\
"investors": 43 ,\
"measure": 18 ,\
"need": 33 ,\
"market": 34 ,\
"later": 28 ,\
"what": 39 ,\
"raise": 6 ,\
"when": 38 ,\
"China": 31 ,\
"York": 22 ,\
"falling": 20 ,\
"public": 4 ,\
"too": 5 ,\
"week": 30 ,\
"his": 10 ,\
"business": 8 ,\
"company": 9 ,\
"million": 14 ,\
"monetary": 19 ,\
"average": 41 ,\
"American": 32 ,\
"world": 26 ,\
"day": 21 ,\
"recent": 23 ,\
"down": 40 ,\
"lower": 24 ,\
"could": 36 ,\
"losses": 17 ,\
"or": 11 ,\
"chief": 37 ,\
"selling": 35 ,\
"stock": 16 ,\
"called": 12 \
}'

def evaluate(features):
    words = json.loads(WORDS)
    sentiment = calculateSentiment(words, features, weights)
    return sentiment
    
    