__author__ = 'Roy van den Hurk'

from nltk.tokenize import * 
from nltk.corpus import stopwords
from nltk.stem import *

class NullTokenizer():
    def tokenize(self, text):
        return text.split();

class NullStemmer():
    def stem(self, tokens):
        return tokens
        
class NullLemmatizer():
    def lemmatize(self, tokens):
        return tokens
        
def tokenize(text, tokenizer=NullTokenizer(), stemmer=NullStemmer(), lemmatizer=NullLemmatizer(), removeStopWords=True):
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    #TODO: check unicode warning
    tokens = [i.decode('unicode-escape') for i in tokens if i not in stopwords.words('english')] if removeStopWords else tokens
    tokens = [stemmer.stem(i) for i in tokens]
    tokens = [lemmatizer.lemmatize(i) for i in tokens]
    return tokens