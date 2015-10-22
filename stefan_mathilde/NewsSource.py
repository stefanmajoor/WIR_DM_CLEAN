import urllib2
from cookielib import CookieJar

import BeautifulSoup
import Article
import Mapper


'''
All information for one news source
'''
class NewsSource(object):
    def __init__(self, sourceId):
        self.articles = [];
        self.sourceId = sourceId
        self.urls = [] # urls that are already fetched
        self.newArticles = [] # Items since last call to getNewItems
        self.mapper = Mapper.Mapper();


    '''
    Retrieve an article object from a url
    '''
    def makeArticle(self, url):
        ## USe cookiejar because NYT needs cookie
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        request = opener.open(url)
        rawHtml = request.read()

        url = request.geturl()

        # Fix encoding to make it ascii compatible. Because otherwise our program crashes
        # http://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
        asciiHtml =  ''.join([i if ord(i) < 128 else '' for i in rawHtml])

        htmlObject = BeautifulSoup.BeautifulSoup(asciiHtml)
        title = ''
        if htmlObject.h1 != None:
            title = htmlObject.h1.text

        # I have no clue why join does not work
        html = ""
        htmlParts = self.getHtml(htmlObject)
        for p in htmlParts:
            html += str(p) + "\n"

        if len(html) == 0:
            print "No html found", url, "\n"
            return None

        author = self.getAuthor(htmlObject)
        date = self.getDate(htmlObject)
        isEconomical = self.isEconomical(htmlObject, url)

        if isEconomical == -1:
            return None

        return Article.Article(self.sourceId, url,  title, date, author, html, isEconomical)

    def getAuthor(self, htmlObject):
        authorCollection = htmlObject.findAll("span", {"class": "byline__name"})
        if len(authorCollection) == 0:
            return None
        else:
            return authorCollection[0].text

    def getHtml(self, htmlObject):
        return htmlObject.findAll("div", {"class": "story-body__inner"})

    def isEconomical(self, htmlObject, url):
        return -1

    def getDate(self, htmlObject):
        return None
