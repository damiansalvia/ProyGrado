# -*- encoding: utf-8 -*-
'''
Module with miscellaneous methods

@author: Nicolás Mechulam, Damán Salvia
'''

from collections import defaultdict
from itertools import tee, chain
from collections import Counter
from enchant.utils import levenshtein
import re, random, types


def OpinionType(opinion):
    if not opinion.has_key('category'):
        return 1 # unpreprocessed opinion
    if opinion.has_key('text') and type(opinion['text']) == list and opinion['text'][0].has_key('lemma') and opinion['text'][0].has_key('tag'):
        return 2 # preprocessed opinion
    return 0


class Iterable(object):
    
    def __init__(self,iterable,count=None):
        for_real , for_sum = tee(iterable) 
        self.__count    = count if count is not None else sum( 1 for _ in for_sum ) 
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

    def get_iterator(self):
        for_real , for_iter = tee(self.__iterable)
        self.__iterable = for_real
        return for_iter

    def split_sample(self,frac,seed=1):
        for_iter1 , for_iter2 = tee(self.__iterable)
        for_real  , for_iter2 = tee(for_iter2)
        self.__iterable = for_real
        random.seed(seed)
        idxs = [ idx for idx in range(self.__count) ] ; random.shuffle(idxs)
        top = int( round( self.__count * frac ) )
        idxs1, idxs2 = idxs[:top], idxs[top:]
        iter1 = Iterable( val for pos,val in enumerate(for_iter1) if pos in idxs1 )
        iter2 = Iterable( val for pos,val in enumerate(for_iter2) if pos in idxs2 )
        return iter1, iter2

    
    
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
    return s.replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'"u',u'u')

 
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


def get_levinstein_pattern(word):
    pattern = u'|'.join([
                    '|'.join([ # Make Levistein regex from word
                        ''.join([ "^", word[:i]  , '.',                      word[i:]   , "$" ]),  # INS
                        ''.join([ "^", word[:i]  ,                           word[i:]   , "$" ]),  # DEL
                        ''.join([ "^", word[:i-1], '.',                      word[i:]   , "$" ]),  # MOD
                        ''.join([ "^", word[:i-1], word[i:i+1], word[i-1:i], word[i+1:] , "$" ]),  # TRN
                     ]) for i in range(1,len(word)+1)
                ])
    return pattern


def _search_influences(graph, initial, threshold):

    influence = defaultdict(lambda:[0,0]) ; influence[initial] = [1, 0]    
    visited_dir = [] ; visited_inv = []
    nodes = graph.nodes()    
    while nodes: 

        next_dir = None ; next_inv = None
        
        for node in nodes: # Select best direct node and best inverse node (It can be the dame node)
            
            if influence[node][0] > threshold and not node in visited_dir:
                if next_dir is None:
                    next_dir = node
                elif influence[node][0] > influence[next_dir][0]:
                    next_dir = node
            
            if influence[node][1] > threshold and not node in visited_inv:
                if next_inv is None:
                    next_inv = node
                elif influence[node][1] > influence[next_inv][1]:
                    next_inv = node

        if next_dir is None and next_inv is None:
            break

        if next_dir:
            
            visited_dir.append(next_dir)
            current_dir_w = influence[next_dir][0]
            
            for edge in graph[next_dir]:
                
                if edge not in visited_dir:
                    
                    dir_weight = current_dir_w * graph[next_dir][edge]['dir']
                    inv_weight = current_dir_w * graph[next_dir][edge]['inv']
                    
                    if dir_weight > influence[edge][0]:
                        influence[edge][0] = dir_weight
                        
                    if inv_weight > influence[edge][1]:
                        influence[edge][1] = inv_weight

        if next_inv:
            visited_inv.append(next_inv)
            current_inv_w = influence[next_inv][1]
            
            for edge in graph[next_inv]:
                
                if edge not in visited_inv:
                    
                    dir_weight = current_inv_w * graph[next_inv][edge]['inv']
                    inv_weight = current_inv_w * graph[next_inv][edge]['dir']
                    
                    if dir_weight > influence[edge][0]:
                        influence[edge][0] = dir_weight
                        
                    if inv_weight > influence[edge][1]:
                        influence[edge][1] = inv_weight

    return dict(influence)