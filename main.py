from stefan_mathilde.Crawler import Crawl

class Crawler(Crawl.Crawl):
    def handleArticle(self, article):
        print "Found an article: "  + article.title



print "Starting crawler. It may take some time before articles are found"
crawler = Crawler()
crawler.crawl()
