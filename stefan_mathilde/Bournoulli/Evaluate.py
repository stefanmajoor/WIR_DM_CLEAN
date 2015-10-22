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

class Evaluate(BaseEvaluate.Evaluate):

    def __init__(self):
        self.mapper =  Mapper.Mapper()
        self.termCount = [dict(), dict()]

        for token in self.mapper.getTokens():
            self.termCount[token[0]][token[1]] = token[2]

    def evaluate(self, html):
        classes = {
            0: 0,
            1: 1
        }
        result = self.applyMultinomialNV(html, classes)
        return result


    def applyMultinomialNV(self, html, classes):
        tokens = self.tokenize(html)

        prior = self.getPriors(self.mapper, classes)

        countCollection = dict()
        for c in classes:
            countCollection[c] = self.mapper.getArticleCountClass(classes[c])

        score = dict()

        for c in classes:
            score[c] = log(prior[c])

            for r in  self.mapper.getUniqueTokens():
                t = r[0]
                if t in self.termCount[c]:
                    nominator = self.termCount[c][t] + 1
                    denominator =  countCollection[c] + 2
                else:
                    nominator = 1
                    denominator = countCollection[c] + 2


                if t in tokens:
                    score[c] += log(nominator) - log(denominator)
                else:
                    score[c] += log(denominator - nominator) - log(denominator)

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
        [s.extract() for s in htmlObject('script')]


        text = htmlObject.getText()
        tokens = re.findall('(?<![0-9a-zA-Z])([a-zA-z]+)(?![0-9a-zA-Z])', text);

        uniqueTokens = [];

        for t in tokens:
            if t.lower() not in uniqueTokens:
                uniqueTokens.append(t.lower())
        return uniqueTokens


evaluator = BaseEvaluator.Evaluator()
evaluator.start(Evaluate())