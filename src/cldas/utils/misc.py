# -*- encoding: utf-8 -*-
'''
Module with miscellaneous methods

@author: Nicolás Mechulam, Damán Salvia
'''

def _type(opinion):
    if not opinion.has_key('category'):
        return 1 # unpreprocessed opinion
    if opinion.has_key('text') and type(opinion['text']) == list and opinion['text'][0].has_key('lemma') and opinion['text'][0].has_key('tag'):
        return 2 # preprocessed opinion
    return 0
