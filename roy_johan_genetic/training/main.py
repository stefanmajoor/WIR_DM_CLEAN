__author__ = 'Roy van den Hurk, Johan Munneke'

import csv
import threading

from mutators import *
from genetic import *
from tokenizers import *

from nltk.stem.snowball import *

def loadDataSet(fileName, limit):
    with open(fileName) as file:
        csvReader = csv.reader(file)
        data = []
        counter = 0 
        for row in csvReader:
            counter += 1
            if counter > limit and limit != -1:
                break
            tokens = tokenize(row[3], tokenizer=RegexpTokenizer('[a-zA-Z]\w+'), stemmer=EnglishStemmer())
            data.append((tokens, 'neg' if row[1] == 0 else 'pos'))
        return data
    return []
    
def calculateSentiment(tokens, weights):
    sentiment = 0
    for word in tokens:
        try:
            index = words[word]
            sentiment += weights[index]
        except Exception as e:
            #Word has no sentiment value attached, so ignore
            pass
    return sentiment

def classify(tokens,weights):
   posCutoff = 0.01
   negCutoff = -0.01
   sentiment = calculateSentiment(tokens,weights)
   label = 'neu'
   if sentiment > posCutoff:
        label = 'pos'
   elif sentiment < negCutoff:
        label =  'neg'
   return (label, sentiment)    
    
def fitnessFunction(individual):
    correct = 0 
    for tokens, l in train:
        label, sentiment = classify(tokens, individual)
        if label == l:
            correct += 1
        else:
            pass
            #print 'Wrongly classified', tokens, ' as ', (label, sentiment)
    return correct / float(len(train))

#TODO: code dup
def evaluate(individual):
    correct = 0 
    for tokens, l in test:
        label, sentiment = classify(tokens, individual)
        if label == l:
            correct += 1
        else:
            pass
            #print 'Wrongly classified', tokens, ' as ', (label, sentiment)
    return correct / float(len(test))
        
def runTest(mutator, fitness, populationSize, length, min , max, retain, random_select, mutate):
    results = []
    genetic = Genetic(mutator, fitness)
    population = genetic.population(populationSize, length, min, max)
    run = 0 
    for iteration in iterations:
        run += 1
        print 'Starting run ', run
        population = genetic.population(populationSize, length, min, max)
        newPop = genetic.evolve(iteration, population)
        #Return (grade, best)
        ranked = [(genetic.fitness(x), x) for x in newPop]
        ranked = [x[1] for x in sorted(ranked, reverse=True)]
        results.append((genetic.grade(newPop), genetic.fitness(ranked[0]), ranked[0]))
    return results

train = []
test = []
words = {}
iterations = [1, 10, 50,100,250]

def doTest(name, mutator, fitness, populationSize, length, min , max, retain, random_select, mutate):
    results = runTest(mutator, fitness, populationSize, length, min , max, retain, random_select, mutate)
    output = '<<< Result of test ' ,  name ,  '>>>>>' , "\n"
    output = output, 'Average fitness',"\n"
    #for grade, fitness, weights in results:
    #    output= output, 'Fitness on training data' ,   fitness ,"\n"
    output = name
    for g, f, weights in results:
        output= output,  '(',  evaluate(weights) ,")"
    print output

if __name__ == '__main__' :
    train = loadDataSet('sentiment.csv', 100000)
    l = int(len(train) * 0.8)
    test = train[l:]
    train = train[:l]
    wordId = 0
    for tokens, l in train:
        for word in tokens:
            if not word in words:
                words[word] = wordId
                wordId += 1
    print '#train=', len(train) , '#test=' , len(test), '#words=', len(words)
    #TODO: make sure that a population has enough individuals so that the weights can gradually change, or use a different mutator
    seed(0)
    #results = runTest(WeightedAverageMutator(0.8), fitnessFunction, 100, len(words), -100, 100, 0.2, 0.5, 0.05)
    #print results
    #for grade, fitness, weights in results:
    #    print grade, ' ' , fitness
    #for g,f, weights in results:
    #    print evaluate(weights)
    TESTS = [
            ('bkvjasjhkd', RandomMutator(), fitnessFunction, 100, len(words), -100, 100, 0.2, 0.5, 0.05),
           ]
    for TEST in TESTS:
        t = threading.Thread(target=doTest, args = TEST)
        t.start()
    print 'done'
    #doTest('test 1', WeightedAverageMutator(0.8), fitnessFunction, 100, len(words), -100, 100, 0.2, 0.5, 0.05)


    
        
    