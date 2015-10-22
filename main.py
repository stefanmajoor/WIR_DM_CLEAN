from stefan_mathilde.Crawler import Crawl
from tom_kaitao import

class Crawler(Crawl.Crawl):
    def handleArticle(self, article):
        print "Found an article: "  + article.title




crawler = Crawler()
crawler.crawl()