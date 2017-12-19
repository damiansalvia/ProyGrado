# -*- encoding: utf-8 -*-
'''
Module with miscellaneous methods

@author: Nicolás Mechulam, Damán Salvia
'''

from itertools import tee, chain
from collections import Counter
from enchant.utils import levenshtein
import re


def OpinionType(opinion):
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
        
    def __repr__(self):
        return "< %s.%s - size(%s) >" % ( self.__class__.__module__, self.__class__.__name__, self.__count )
    
    def __str__(self):
        return "<%s object with %i items of %s>" % (self.__class__.__name__,self.__count,self.__iterable.__repr__()) 
 
    def __getitem__(self, i):
        for_real , for_iter = tee(self.__iterable)
        self.__iterable = for_real
        for pos,val in enumerate(for_iter):
            if pos==i: return val
    
    
class EnumItems:
    class __metaclass__(type):
        def __contains__(self,item):
            return item in self.__dict__.values()
        
        
class Levinstein:
    
    def __init__(self,vocabulary):
        "Based on Norvig solution."
        self.WORDS = vocabulary
    
    def P(self, word, N=None): 
        "Probability of `word`."
        N = sum(self.WORDS.values()) if N is None else N
        return 1.0 * self.WORDS[word] / N
    
    def correction(self, word): 
        "Most probable spelling correction for word."
        return max(self.suggestions(word), key=self.P)
    
    def suggestions(self, word): 
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
    
    def known(self, words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)
    
    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters    = u'abcdefghijklmnopqrstuvwxyzáéóúñü'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
    
    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
 
 
def no_accent(s):
    return s.replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'"u',u'u').replace(u'ñ',u'n')

 
def levenshtein_no_accent(s1, s2):
    return levenshtein( no_accent(s1) , no_accent(s2) )


def get_score(s1,s2):
    res = 0
    res += levenshtein( s1 , s2 )
    res += levenshtein( no_accent(s1) , no_accent(s2) )
    res += 3 if re.search('[\s-]', s2) is not None else 0
    return res


def get_close_dist(word, wordlist, cutoff=0.7, n=None):
    if not wordlist:
        return []
    res = { wd:get_score(word,wd) for wd in wordlist }
    max_score  = max(res.values()) 
    mean_score = (max_score - min(res.values())) / 2
    res = [ wd for wd,score in sorted( res.items(), key=lambda item:item[1] ) if 1.0*(max_score-score) > cutoff * mean_score ]
    res = res[:n]
    return res

