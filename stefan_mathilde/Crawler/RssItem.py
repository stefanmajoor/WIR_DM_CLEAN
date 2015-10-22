'''
One RSS Item to be used
'''
class RssItem:
    def __init__(self, rssUrl, url, title, date, author):
        self.rssUrl = rssUrl
        self.url = url
        self.title = title
        self.date = date
        self.author = author

    def getRssUrl(self):
        return self.rssUrl

    def getAuthor(self):
        return self.author

    def getUrl(self):
        return self.url

    def getTitle(self):
        return self.title

    def getDate(self):
        return self.date