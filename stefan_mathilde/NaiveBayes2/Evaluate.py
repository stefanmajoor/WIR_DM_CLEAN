import BeautifulSoup
import nltk
import Mapper
from math import log
import re

import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Evaluation.Evaluator as BaseEvaluator
import Evaluation.Evaluate as BaseEvaluate
import NaiveBayes2.Mapper as Mapper

class Evaluate(BaseEvaluate.Evaluate):

    def __init__(self):
        self.mapper =  Mapper.Mapper()
        self.termCount = [dict(), dict()]
        self.amountOfTokens = 0
        self.tokensInDictionary = 0
        self.confidenceRatio = 0

        for token in self.mapper.getTokens():
            self.termCount[token[0]][token[1]] = token[2]

    def evaluate(self, html):
        classes = {
            0: 0,
            1: 1
        }
        result = self.applyMultinomialNV(html, classes)
        return result

    def getAmountOfTokens(self):
        return self.amountOfTokens

    def getAmountOfTokensInDictionary(self):
        return self.tokensInDictionary

    def getConfidenceRatio(self):
        return self.confidenceRatio

    def applyMultinomialNV(self, html, classes):
        if html == None: ## Non valid html is not economical
            return 0

        tokens = self.tokenize(html)
        self.amountOfTokens = len(tokens)

        prior = self.getPriors(self.mapper, classes)

        wordsInCollection = dict()
        for c in classes:
            wordsInCollection[c] = self.mapper.getWordCountCollection(classes[c])

        score = dict()
        for c in classes:
            score[c] = log(prior[c])
            for t in tokens:
                if t not in self.termCount[c]:
                    denominator = 0
                else:
                    denominator = self.termCount[c][t]
                    self.tokensInDictionary += 1
                nominator = wordsInCollection[c]
                condProbability = log(float(denominator+1)) - log(float(nominator+1))
                score[c] += condProbability


        maxClass = None
        maxClassValue = -float("inf")


        for c in score:
            if score[c] > maxClassValue:
                maxClass = c
                maxClassValue = score[c]

        self.confidenceRatio = score[0] / float(score[1]);

        return maxClass

    def getPriors(self, mapper, classes):
        n = mapper.getArticleCount()
        prior = dict()

        for c in classes:
            prior[c] = mapper.getArticleCountClass(classes[c]) / float(n)

        return prior


    def tokenize(self, html):

        htmlObject = BeautifulSoup.BeautifulSoup(html)
        [s.extract() for s in htmlObject('script')]
        text = htmlObject.getText()
        tokens = re.findall('(?<![0-9a-zA-Z])([a-zA-z]+)(?![0-9a-zA-Z])', text);
        return tokens
#
# evaluator = BaseEvaluator.Evaluator()
# evaluator.start(Evaluate())