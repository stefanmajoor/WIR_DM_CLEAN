import urllib2
from cookielib import CookieJar
import BeautifulSoup
import CompanyFinder
import Article
from boilerpipe.extract import Extractor
import sys

class ContentParser():

    def __init__(self, item):
        self.item = item
        self.rawHtml = ''

    def run(self):
        url = self.item.getUrl()

        try:
            ## USe cookiejar because NYT needs cookie
            cj = CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            request = opener.open(url)
            self.rawHtml = request.read()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return None
        author = self.getAuthor()
        date = self.getDate()
        title = self.getTitle()
        html = self.getHtml()

        companies = self.getCompanies(html)

        return Article.Article(self.item.getRssUrl(), url,  title, date, author, html, companies)

    def getCompanies(self, html):
        htmlObject = BeautifulSoup.BeautifulSoup(html)
        text = htmlObject.getText()
        return CompanyFinder.findCompanies(text)

    def getTitle(self):
        return self.item.getTitle()

    def getDate(self):
        return self.item.getDate()

    def getHtml(self):
        try:
            #Somehow fails sometimee
            extractor = Extractor(extractor='ArticleExtractor', html=self.rawHtml)
            return ''.join([i if ord(i) < 128 else '' for i in extractor.getHTML()])
        except:
            return None

    def getAuthor(self):
        return self.item.getAuthor()