__author__ = 'Roy van den Hurk'

from random import *

'''
Class that breeds two individuals to produce a new individual.
'''
class Mutator:
    '''
    Breed the male and the female.
    
    Args:
        male (individual) : The male
        female (individual) : The female
    Returns:
        The child of male and female
    '''
    def mutate(self, male, female):
        raise NotImplementedError('"mutate()" should be implemented.')

'''
Mutator that breeds by combining the first half the male with
    the second half of the female.
'''
class HalfMutator(Mutator):
    def mutate(self, male, female):
        half = len(male)/ 2
        return male[:half] + female[half:]

'''
Mutator that breeds by combining the first (randomly choosen) part of the male with
    the second part of the female.
'''
class SinglePointMutator(Mutator):
    def mutate(self, male, female):
        point = randint(0, len(male) - 1)
        return male[:point] + female[point:]

class WeightedAverageMutator(Mutator):
    def __init__(self, weight):
        self.weight = weight
        
    def mutate(self, male, female):
        child = []
        for i in range(0, len(male)):
            child.append(self.weight * male[i] + (1 - self.weight) * female[i])
        return child

class RandomMutator(Mutator):
    def mutate(self, male, female):
        child = []
        for i in range(0, len(male)):
            child.append(male[i] if random() > 0.5 else female[i])
        return child
'''
TODO:
    Two Points -> Take random section from male, take rest from female
    Random -> Pick random elements
    Arithmetic -> Do some calculation (E.G. average)
'''
