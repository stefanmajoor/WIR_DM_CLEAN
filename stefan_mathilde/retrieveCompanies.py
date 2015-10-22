    import BeautifulSoup
    import urllib2
    import re

    global stopList

    stopList = [
        'systems',  'corp', 'group', 'inc', 'Co', 'pharmaceuticals', 'technology', 'ltd', 'pharmaceut', 'pharmac', 'pharmaceu', 'com',
        'technologie'
    ]


    class NasdaqArticle(object):
        def NasdaqFind(self, url):
            request = urllib2.urlopen(url)
            read = request.read()
            BeatiUrl = BeautifulSoup.BeautifulSoup(read)
            NasdaqName = BeatiUrl.findAll("tr", {"class":"normal-row"}) + BeatiUrl.findAll("tr", {"class":"silver"})
            ListItem = []
            for item in NasdaqName:
                newItem = item.findAll("a")
                name = newItem[0].text
                name = ' '.join(i if i.strip() not in stopList else '' for i in re.findall(r"\w+", name.lower()))
                ListItem.append(name);
            return ListItem

    nasqad = NasdaqArticle()
    names =  nasqad.NasdaqFind('http://www.beurs.nl/koersen/nasdaq/p1?rc=100#start')

    for i in names:
        print i, "\n";