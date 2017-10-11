# -*- encoding: utf-8 -*-
'''
Module with miscellaneous methods

@author: Nicolás Mechulam, Damán Salvia
'''

from itertools import tee, chain


def _type(opinion):
    if not opinion.has_key('category'):
        return 1 # unpreprocessed opinion
    if opinion.has_key('text') and type(opinion['text']) == list and opinion['text'][0].has_key('lemma') and opinion['text'][0].has_key('tag'):
        return 2 # preprocessed opinion
    return 0


class Iterable(object):
    
    def __init__(self,iterable):
        for_real , for_sum = tee(iterable) 
        self.__count    = sum( 1 for _ in for_sum ) 
        self.__iterable = for_real
        
    def __iter__(self):
        for_real , for_iter = tee(self.__iterable)
        self.__iterable = for_real
        for it in for_iter:
            yield it
            
    def __len__(self):
        return self.__count
    
    def __add__(self,other):
        if not isinstance(other, self.__class__): #or type(other) != list:
            raise TypeError('unsupported operand type(s) for +: \'%s\' and \'%s\'' % (self.__class__.__name__, other.__class__.__name__))
        return Iterable( chain(self.__iterable,other) )
    
class _Enum:
    class __metaclass__(type):
        def __contains__(self,item):
            return item in self.__dict__.values()
        