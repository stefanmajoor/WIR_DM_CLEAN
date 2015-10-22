import re
from Source import NYTSource;
import Mapper
from Source import CnnSource

mapper = Mapper.Mapper();

nyt = CnnSource.CnnSource('cnn')

allUrls = []
with file('../cnn.txt', 'r') as f:
    for line in f:
        allUrls += re.findall('(http:\/\/on.cnn.com\/[A-Za-z0-9]*)', line)

print allUrls


for url in allUrls:
    print url, "\n"
    try:
        article = nyt.makeArticle(url)
        mapper.saveArticle(article, article.isEconomical)
    except Exception as e:
       print "An error has occured: " + str(e.message)