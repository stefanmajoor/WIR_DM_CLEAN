import time
class Article():

    def __init__(self, sourceId, url, title, date, author, html, isEconomical):
        self.url = url
        self.sourceId = sourceId
        self.date = date
        self.title = title
        self.author = author
        self.isEconomical = isEconomical
        self.html = html

    def getUrl(self):
        return self.url

    def __str__(self):
        out = "Source: " + self.sourceId + "\n"
        out += "Url: " + self.url + "\n"
        out += "Title: " + self.title + "\n"
        out += "Date:" + str(self.date) + "\n"
        out += "Author: " + str(self.author) + "\n"
        out += "Economical: " + str(self.isEconomical) + "\n"
        out += "HTML: \n" + self.html
        return out
