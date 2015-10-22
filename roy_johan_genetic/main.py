__author__ = 'Roy van den Hurk'

from mutators import *
from genetic import *
from tokenizers import *

def fitnessFunction(individual):
    #TODO: write this function
    return sum(individual)

        
def runTest(mutator, fitness, populationSize, length, min , max, retain, random_select, mutate):
    iterations = [100]
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
        results.append((genetic.grade(newPop), ranked[0]))
    return results
    
def test(a):
    a.append('test')

if __name__ == '__main__' :
    #TODO: make sure that a population has enough individuals so that the weights can gradually change, or use a different mutator
    seed(0)
    results = runTest(HalfMutator(), fitnessFunction, 10000, 5, -100, 100, 0.2, 0.2, 0.05)
    print results