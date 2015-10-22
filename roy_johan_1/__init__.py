__author__ = 'Roy van den Hurk, Johan Munneke'

from random import randint, uniform
import random
from Article import *
from Config import *
from Features import *
from featurextractor import *

WEIGHT_MIN = 0
WEIGHT_MAX = 10


def individual(length, min, max):
    return [uniform(min, max) for x in xrange(length)]


def population(count, length, min, max):
    return [individual(length, min, max) for x in xrange(count)]


def getAuthorValue(articles, features):
    author = features.author
    articlesByAuthor = [a for a in articles if a.author == author]
    pos = sum(1 for a in articlesByAuthor if a.label == 1)
    neg = sum(1 for a in articlesByAuthor if a.label == -1)
    return (pos - neg) / (pos + neg)


def getSentiment(articles, features):
    return features.sentiment.polarity  # * features.sentiment.subjectivity


def getEconomicalSentiment(article, features):
    pass


def getPublisher(articles, features):
    publisher = features.publisher
    articlesByPublisher = [a for a in articles if a.publisher == publisher]
    pos = sum(1 for a in articlesByPublisher if a.label == 1)
    neg = sum(1 for a in articlesByPublisher if a.label == -1)
    return (pos - neg) / (pos + neg)


def getArticleLength(articles, features):
    return 1 / math.log(features.length)


def getTitle(articles, features):
    return sum(words[word] for word in features.title if word in words) / len(features.title)


def getTfIdf(articles, features):
    s = sum(1 for word in features.tf_idf if features.tf_idf[word] > 4) / features.length
    return s



# def getTf(articles, features):
#     contains = False
#     for word in features.text.words:
#         if word in words:
#             contains = True
#     if not contains:
#         print features.text
#     s = sum(words[word] for word in features.text if word in words) / len(features.text.words)
#     return s


def fitness(articles, weigths):
    p = [getAuthorValue, getSentiment, getPublisher, getArticleLength, getTitle, getTfIdf]
    correct = 0
    wrong = 0
    for article in articles:
        sum = 0
        for i in range(0, 6):
            sum += weigths[i] * p[i](articles, article.features)
        for word in range(0,len(words)):
            sum += weigths[i+6] * words[words.keys()[word]] * article.textBlob.word_counts[words.keys()[word]] / article.features.length
        if article.label == 0:
            if -0.1 <= sum <= 0.1:
                correct += 1
        elif sum > 0.1 and article.label == 1:
            correct += 1
        elif sum < -0.1 and article.label == -1:
            correct += 1
        else:
            wrong += 1
    return correct / (float)(len(articles))


def evolve(articles, pop, retain=0.2, random_select=0.5, mutate=0.01):
    sortedList = [(fitness(articles, x), x) for x in pop]
    sortedList = [x[1] for x in sorted(sortedList, reverse=True)]
    retain_length = int(len(sortedList) * retain)
    parentList = sortedList[:retain_length]

    for individual in sortedList[retain_length:]:
        if random_select > random.random():
            parentList.append(individual)

    for individual in parentList:
        if mutate > random.random():
            featureToMutate = randint(0, len(individual) - 1)
            individual[featureToMutate] = uniform(min(individual), max(individual))

    parentListLength = len(parentList)
    desiredParentListLength = len(pop) - parentListLength
    children = []
    while len(children) < desiredParentListLength:
        male = randint(0, parentListLength - 1)
        female = randint(0, parentListLength - 1)
        if male != female:
            children.append(mutator(male, female, parentList))
    parentList.extend(children)
    return parentList


def mutator(male, female, parentList):
    male = parentList[male]
    female = parentList[female]
    half = len(male) / 2
    child = male[:half] + female[half:]
    return child


def grade(articles, pop):
    summed = sum(fitness(articles, x) for x in pop)
    return summed / float(len(pop))


words = {}

if __name__ == '__main__':

    conn2 = sqlite3.connect("data/wordsList.db")
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM customers')
    rows = cursor2.fetchall()
    for row in rows:
        words[row[1]] = row[4]
    conn2.close()

    articles = []
    articles = Article.from_sql()
    featureExtractor = FeatureExtractor()
    featureExtractor.set_training_data(articles)
    random.seed(1)
    for article in articles:
        features = featureExtractor.get_features(article)
        article.features = features
        article.label = -1 if random.random() > 0.5 else 1
    p = population(100, 6 + len(words), 0, 100000)
    progress = 0
    for x in xrange(15):
        progress += 1
        print progress
        p = evolve(articles, p)
        # print population(10, len(features), WEIGHT_MIN, WEIGHT_MAX)
        # Test value extraction
        # print Features.getAuthorValue('dd')
        # test
    sortedList = [(fitness(articles, x), x) for x in p]
    sortedList = [x[1] for x in sorted(sortedList, reverse=True)]
    print 'done'
    print sortedList[0]

    # from textblob.classifiers import NaiveBayesClassifier
    #
    # train = []
    # for article in articles:
    #     for sentence in article.textBlob.sentences:
    #         train.append({"text": sentence, "label": "pos"})
    # print len(train)
    # cl = NaiveBayesClassifier(train)
    # cl.classify("test string test stestasjajsjdj a hahsd ")
    # print 'done'