import re
from Source import NYTSource;
import Mapper

mapper = Mapper.Mapper()

nyt = NYTSource.NYTSource('nyt')
NasdaqArticle()

allUrls = []
with file('../nytimes.txt', 'r') as f:
    for line in f:
        allUrls += re.findall('(http:\/\/nyti.ms\/[A-Za-z0-9]*)', line)

for url in allUrls:
    print url, "\n"
    try:
        article = nyt.makeArticle(url)
        mapper.saveArticle(article, article.isEconomical)
    except Exception as e:
        print "An error has occured: " + str(e.message)