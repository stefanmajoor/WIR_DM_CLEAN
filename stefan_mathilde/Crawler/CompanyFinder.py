companies = {
    'CSCO': ['Cisco'],
    'AMZN': ['Amazon'],
    'TSLA': ['Tesla'],
    'COKE': ['Coca-Cola'],
    'VOD': ['Vodafone'],
    'MSFT': ['Microsoft', 'Windows'],
    'NFLX': ['Netflix'],
    'SBUX': ['Starbucks'],
    'CMCSK': ['Comcast'],
    'INTC': ['Intel']
}

'''
Extrac the company names from the html

returns array with all company tickers ids
'''
def findCompanies(text):
    global companies


    results = []

    for ticker in companies.iterkeys():
        for name in companies[ticker]:
            if name in text:
                results.append(ticker)
                break # We don't give the same company twice
    return results

