__author__ = 'Roy van den Hurk'

from random import *

'''
Class to learn a set of weight for features in such a way that the result is as high as possible.

Args:
    mutator (Mutator) : The mutator to use
    fitnessFunction (function(individual)) : Function to evaluate a individual, higher score is better.
'''
class Genetic:

    def __init__(self, mutator, fitnessFunction):
       self.mutator = mutator
       self.fitnessFunction  = fitnessFunction;
        
    '''
    Create a individual.
    
    Args:
        length (int) : The length of the individual
        min (int) : The minimum value that a weight in the individual can take
        max (int) : The maximum value that a weight in the individual can take 
        
    Return:
        A list of random weights
    '''
    def individual(self, length, min, max):
        return [uniform(min, max) for x in xrange(length)]
    
    '''
    Create a new population.
    
    Args:
        count (int) : The number of individuals in the population
        length (int) : The length of an individual
        min (int) : The minimum value that a weight in an individual can take
        max (int) : The maximum value that a weight in an individual can take
        
    Returns:
        A list of individuals
    '''
    def population(self, count, length, min, max):
        return [self.individual(length, min, max) for x in xrange(count)]
    
    
    '''
    Breed the male and the female.
    
    Args:
        male (individual) : The male
        female (individual) : The female
    Returns:
        The child of male and female
    '''
    def mutate(self, male, female):
        return self.mutator.mutate(male, female)
        
    '''
    Calculate the fitness of an individual, higher is better.
    
    Args:
        individual (list of doubles) : The individual
        
    Returns:
        The fitness of an individual
    '''
    def fitness(self, individual):
        return self.fitnessFunction(individual)
        
    '''
    Evolve the population once.
    
    Args:
        population (list of individuals) : The population
        retain (double) : Percentage of the best parents to keep (default=0.2)
        random_select (double) : Chance to randomly add an not retained parent (default=0.5)
        mutate (double) : Chance to mutate a single weight of an individual (default=0.01)
        
    Returns:
        The new population
    '''
    def evolveOnce(self, population, retain=0.2, random_select=0.5, mutate=0.01):
        #sort population, highest fitness first
        ranked = [(self.fitness(x), x) for x in population]
        ranked = [x[1] for x in sorted(ranked, reverse=True)]
        
        #only keep the best parents
        retain_length = int(len(ranked)*retain)
        parents = ranked[:retain_length]
        
        # randomly add other individuals to promote genetic diversity
        for individual in ranked[retain_length:]:
            if random_select > random():
                parents.append(individual)
                
        #mutate some random individuals
        for individual in parents:
            if mutate > random():
                posToMutate = randint(0, len(individual) - 1)
                individual[posToMutate] = uniform(min(individual), max(individual))
        #breed parents
        numParents = len(parents)
        numDesiredChildren = len(population) - numParents
        children = []
        while len(children) < numDesiredChildren:
            malePos = randint(0, numParents - 1)
            femalePos = randint(0, numParents - 1)
            if malePos != femalePos:
                child = self.mutator.mutate(parents[malePos], parents[femalePos])
                children.append(child)
        parents.extend(children)
        return parents
        
    '''
    Evolve the population "iterations" times.
    
    Args:
        iterations (int) : The number of evolutions
        population (list of individuals) : The population
        retain (double) : Percentage of the best parents to keep (default=0.2)
        random_select (double) : Chance to randomly add an not retained parent (default=0.5)
        mutate (double) : Chance to mutate a single weight of an individual (default=0.01)
        
    Returns: 
        The new population
    '''
    def evolve(self, iterations, population, retain=0.2, random_select=0.5, mutate_prob=0.01):
        if int(len(population) * retain) <= 1:
           raise Exception('Need at least 2 top parents, try a bigger population size or retain percentage!')
        print 'evolving ', iterations, ' iterations'
        done = 0 
        mod = iterations/ 10
        if mod == 0:
            mod = 1
        for x in xrange(iterations):
            population = self.evolveOnce(population, retain, random_select ,mutate_prob)
            done += 1
            #print progress 100 times
            if (done % mod == 0):
                print 'Progress: ', done, '/', iterations
        return population
    
    '''
    Calculate the average fitness of the population.
    
    Args: 
        population (list of individuals) : The population
        
    Returns:
        The average fitness of population
    '''
    def grade(self, population):
        summed = sum(self.fitness(x) for x in population)
        return summed / float(len(population))

    def evaluateArticle(self, article):
        return 3.1415