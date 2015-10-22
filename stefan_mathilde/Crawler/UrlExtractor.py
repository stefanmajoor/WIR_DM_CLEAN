import BeautifulSoup
import Mapper
import re

class UrlExtractor():
    def __init__(self):
        self.mapper = Mapper.Mapper()


    def extract(self, article):
        html  = article.getHtml()
        htmlObject = BeautifulSoup.BeautifulSoup(html)

        for link in htmlObject.findAll('a'):
            self.handleLink(link.get('href'))

    def extractHtml(self, htmlObject):
        for link in htmlObject.findAll('a'):
            self.handleLink(link.get('href'))

    def handleLink(self, link):
        try:
            if re.match('^http[s]*:\/\/', link) != None:
                self.mapper.addLink(link)
        except:
            pass