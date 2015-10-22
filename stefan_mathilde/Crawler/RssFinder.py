import Mapper
import urllib2
from cookielib import CookieJar
import BeautifulSoup
import UrlExtractor
import re
import RssReader
import ContentParser
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import NaiveBayes2.Evaluate as BaseEvaluate



class RssFinder():
    def __init__(self):
        self.mapper = Mapper.Mapper()
        self.urlExtractor = UrlExtractor.UrlExtractor()
        self.evaluator = BaseEvaluate.Evaluate()

    def start(self):
        while True:
            links = self.mapper.findLinksToCheck()
            for link in links:
                print "Start link", link
                self.getRss(link)
                self.mapper.setLinkDone(link)
            time.sleep(5)

    def getRss(self, link):
        rssReader = self.getRssReader(link)
        if rssReader != None:
            print "Found rss", link
            self.addRss(rssReader, link)
            return

        cj = CookieJar()

        try:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            request = opener.open(link, timeout=3)
            rawHtml = request.read()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return

        asciiHtml =  ''.join([i if ord(i) < 128 else '' for i in rawHtml])
        htmlObject = BeautifulSoup.BeautifulSoup(asciiHtml)
        for link in htmlObject.findAll('a') + htmlObject.findAll('link'):
            self.handleLink(link.get('href'))

    def addRss(self, reader, link):
        articles = []
        for item in  reader.getRssItems():
            ## Extract all articles
            parser = ContentParser.ContentParser(item)  
            try:
                articles.append(parser.run())
            except:
                print "Unexpected error:", sys.exc_info()[0]

        print "Done feed", link, " found", len(articles), " articles";

        economicalArticles = self.extractEconomical(articles)
        if len(economicalArticles) > len(reader.getRssItems()) / 2:
            self.mapper.addFeed(link)

        print "Found", len(economicalArticles), " economical articles"

    def getRssReader(self, link):
        rssReader = RssReader.RssReader(link)
        rssReader.run()
        if len(rssReader.getRssItems()) > 0:
            return rssReader
        else:
            return None

    def handleLink(self, link):
        if link == None:
            return

        # filter all ingoing links. They will probably be very few, and they are a pain in the ass
        if re.match('^http[s]*:\/\/', link) == None:
            return

        wordsNotMatched = ['feedback']
        wordsMatched = ['rss', 'feed', '.xml'] # terms that need to be present to maybe consider it a feed

        for word in wordsMatched:
            if word in link.lower():
                for word2 in wordsNotMatched:
                    if word2 not in link.lower():
                        self.mapper.addLink(link)

                        print "Found a possible rss feed", link

    def extractEconomical(self, articles):
        economicalArticles = []

        for a in articles:
            ## check if it is a probable economical erticle
            if a != None and self.evaluator.evaluate(a.getHtml()):
                hasEnoughTokens = self.evaluator.getAmountOfTokens() > 200
                isInEnglish = self.evaluator.getAmountOfTokensInDictionary() / self.evaluator.getAmountOfTokens() > 0.5
                if hasEnoughTokens and isInEnglish:
                    economicalArticles.append(a)
        return economicalArticles

rssFinder = RssFinder()
rssFinder.start()