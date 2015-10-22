import Mapper
import nltk
import BeautifulSoup
import re

classes = {
    'notEconomical': 0,
    'economical':1
}

def trainMultinomialNB(classes):
    mapper = Mapper.Mapper()
    mapper.createTable()
    n = mapper.getArticleCount()

    prior = dict()

    for c in classes:
        prior[c] = mapper.getArticleCountClass(classes[c]) / float(n)

    articles = dict()
    for c in classes:
        articles[c] = mapper.getArticles(classes[c])
        articles[c].next()

    for c in classes:
        # print classes[c]
        # articles = mapper.getArticles(classes[c])

        vocabulary = dict()
        for article in articles[c]:
            html = article[6]
            tokens = tokenize(html)
            for t in tokens:
                if not vocabulary.has_key(t):
                    vocabulary[t] = 0
                vocabulary[t] += 1

            # if len(vocabulary) > 1000:
            #     mapper.saveVocabulary(vocabulary, classes[c])
            #     vocabulary = dict()

            print "Done article ", article[0], " Vocabulary length:", len(vocabulary), "\n"

        mapper.saveVocabulary(vocabulary, classes[c])

def tokenize(html):
    htmlObject = BeautifulSoup.BeautifulSoup(html)
    [s.extract() for s in htmlObject('script')]


    text = htmlObject.getText()
    tokens = re.findall('(?<![0-9a-zA-Z])([a-zA-z]+)(?![0-9a-zA-Z])', text);
    return tokens

trainMultinomialNB(classes)