import time
class Article():

    def __init__(self, sourceId, url, title, date, author, html, companies):
        self.url = url
        self.sourceId = sourceId
        self.date = date
        self.title = title
        self.author = author
        self.html = html
        self.companies = companies

    def setConfidence(self, confidence):
        self.confidence = confidence

    def getConfidence(self):
        return self.confidence

    def getUrl(self):
        return self.url

    def getHtml(self):
        return self.html

    def getCompanies(self):
        return self.companies

    def __str__(self):
        out = "Source: " + self.sourceId + "\n"
        out += "Url: " + self.url + "\n"
        out += "Title: " + self.title + "\n"
        out += "Date:" + time.strftime("%Y-%m-%d %H:%I:%S", self.date) + "\n"
        out += "Author: " + self.author + "\n"
        out += "HTML: \n" + self.html
        return out
