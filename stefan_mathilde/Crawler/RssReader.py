import feedparser # https://wiki.python.org/moin/RssLibraries
import RssItem
import Mapper
import re

'''
Reads all items from an rss feed
'''
class RssReader:
    def __init__(self, url):
        self.url = url
        self.articles = []
        self.mapper = Mapper.Mapper()

    '''Run the rss reader, and get the rss Items'''
    def run(self):

        feed = feedparser.parse(self.url)
        for article in feed['items']:
            article['link'] = re.search(r'(^[^#]+)', article['link']).group(0)

            if not self.mapper.hasUrl(article['link']):
                if 'author' in article:
                    author = article['author']
                else:
                    author = None

                if 'published_parsed' in article:
                    published = article['published']
                else:
                    published = None
                rssItem = RssItem.RssItem(self.url, article['link'], article['title'], published, author)
                self.articles.append(rssItem)

    ''' Return the set of articles retrieved'''
    def getRssItems(self):
        return self.articles

