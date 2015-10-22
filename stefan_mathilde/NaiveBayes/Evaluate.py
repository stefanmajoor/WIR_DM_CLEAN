import BeautifulSoup
import nltk
import Mapper
from math import log


import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Evaluation.Evaluator as BaseEvaluator
import Evaluation.Evaluate as BaseEvaluate

class Evaluate(BaseEvaluate.Evaluate):

    def __init__(self):
        self.mapper =  Mapper.Mapper('../trainingsCollection.db')
        self.termCount = [dict(), dict()]

        for token in self.mapper.getTokens():
            self.termCount[token[0]][token[1]] = token[2]



    def evaluate(self, html):
        print "Start"
        classes = {
            0: 0,
            1: 1
        }
        result = self.applyMultinomialNV(html, classes)
        print "end"
        return result


    def applyMultinomialNV(self, html, classes):
        tokens = self.tokenize(html)

        prior = self.getPriors(self.mapper, classes)

        wordsInCollection = dict()
        for c in classes:
            wordsInCollection[c] = self.mapper.getWordCountCollection(classes[c])

        score = dict()
        for c in classes:
            score[c] = log(prior[c])
            for t in tokens:
                if t.lower() not in self.termCount[c]:
                    denominator = 0
                else:
                    denominator = self.termCount[c][t.lower()]
                nominator = wordsInCollection[c]
                condProbability = log(float(denominator+1)) - log(float(nominator+1))
                score[c] += condProbability


        maxClass = None
        maxClassValue = -float("inf")


        for c in score:
            print c, score[c]
            if score[c] > maxClassValue:
                maxClass = c
                maxClassValue = score[c]
        return maxClass

    def getPriors(self, mapper, classes):
        n = mapper.getArticleCount()
        prior = dict()

        for c in classes:
            prior[c] = mapper.getArticleCountClass(classes[c]) / float(n)

        return prior


    def tokenize(self, html):
        htmlObject = BeautifulSoup.BeautifulSoup(html)
        text =  htmlObject.getText()
        tokens = nltk.word_tokenize(text)
        return tokens

# evaluator = BaseEvaluator.Evaluator()
# evaluator.start(Evaluate())