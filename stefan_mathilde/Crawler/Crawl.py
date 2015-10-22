import Mapper
import RssReader
import ContentParser
import sys
import os
import UrlExtractor
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import NaiveBayes2.Evaluate as BaseEvaluate


class Crawl:

    def __init__(self):
        self.mapper = Mapper.Mapper()
        self.evaluator = BaseEvaluate.Evaluate()
        self.urlExtractor = UrlExtractor.UrlExtractor()

    def _extractEconomical(self, articles):
        economicalArticles = []

        for a in articles:
            if a != None:
                if self.evaluator.evaluate(a.getHtml()):
                    a.setConfidence(self.evaluator.getConfidenceRatio())
                    economicalArticles.append(a)
        return economicalArticles

    def crawl(self):
        i = 1
        while True:
            ### Find all feeds
            for feed in self.mapper.getFeeds():
                reader = RssReader.RssReader(feed)
                reader.run()
                articles = []
                for item in  reader.getRssItems():
                    ## Extract all articles
                    parser = ContentParser.ContentParser(item)
                    articles.append(parser.run())

                economicalArticles = self._extractEconomical(articles)

                print "Extracted a total of ", len(economicalArticles), " economical articles"
                #self.mapper.saveArticles(economicalArticles)

                for article in economicalArticles:
                    self.handleArticle(article)

                ## extract the urls
                for article in economicalArticles:
                    self.urlExtractor.extract(article)
                time.sleep(60)
            print "Done Iteration", i

    def handleArticle(self, article):
        pass