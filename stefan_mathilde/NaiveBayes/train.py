import Mapper
import nltk
import BeautifulSoup

classes = {
    'notEconomical': 0,
    'economical':1
}

def trainMultinomialNB(classes):
    mapper = Mapper.Mapper('../trainingsCollection.db')
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
                if not vocabulary.has_key(t.lower()):
                    vocabulary[t.lower()] = 0
                vocabulary[t.lower()] += 1

            # if len(vocabulary) > 100000000:
            #     mapper.saveVocabulary(vocabulary, classes[c])
            #     vocabulary = dict()

            print "Done article ", article[0], " Vocabulary length:", len(vocabulary), "\n"

        mapper.saveVocabulary(vocabulary, classes[c])

def tokenize(html):
    htmlObject = BeautifulSoup.BeautifulSoup(html)
    text =  htmlObject.getText()
    tokens = nltk.word_tokenize(text)

    return tokens




trainMultinomialNB(classes)