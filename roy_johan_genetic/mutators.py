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
        point = randint(len(male) - 1)
        return male[:point] + female[point:]


'''
TODO:
    Two Points -> Take random section from male, take rest from female
    Random -> Pick random elements
    Arithmetic -> Do some calculation (E.G. average)
'''
