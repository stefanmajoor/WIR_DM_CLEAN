'''
Add companies for all the articles that do not have a company yet
'''

import sqlite3
import Mapper
import CompanyFinder
import BeautifulSoup

articleConnection = sqlite3.connect('articles.db')
c = articleConnection.cursor()
c.execute('SELECT * FROM article')


while True:
    articles = c.fetchall()
    print(len(articles))
    for article in articles:
        id = article[0]
        html = article[6]
        htmlObject = BeautifulSoup.BeautifulSoup(html)
        text = htmlObject.getText()

        companies = CompanyFinder.findCompanies(text)
        c.execute('UPDATE article SET companies = ? WHERE id = ' + str(id), [str(companies)])
        articleConnection.commit()