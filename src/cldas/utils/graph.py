# -*- encoding: utf-8 -*-
'''
Module for for generating a context dependent lexicon corpus and seeds

@author: Nicolás Mechulam, Damián Salvia
'''

import os, re

from collections import defaultdict
from cldas.utils import progress, save
from cldas.utils.misc import Iterable, _search_influences


def _valid_tag(tag, tagset):
    for prefix in tagset:
        if tag.startswith(prefix): return True
    return False



class ContextGraph(object):
    '''
    Multigraph of words abstract data type 
    '''
    
    def __init__(self, opinions, source, filter_tags=None, max_weight=1, context_win=1, verbose=True):
            
        self.source = source
        self._graph = self._create_graph(opinions,filter_tags,max_weight,context_win,verbose)
    
    
    def _create_graph(self,opinions,filter_tags,max_weight,context_win,verbose):
        
        graph = defaultdict( lambda : defaultdict( lambda: defaultdict(int) ) )
        
        total = len( opinions )
             
        for idx,opinion in enumerate( opinions ):
            
            if verbose : progress("Building graph for %s" % self.source,total,idx)
    
            text = opinion['text']   
    
            if filter_tags: # Remove tokens having irrelevant information
                text =  [token for token in text if _valid_tag( token['tag'] , filter_tags ) ]
    
            size = len(text)
            for i,item in enumerate(text):
                
                lem = item['lemma']
                 
                neg = item.get('negated', False)
                 
                for j in range(max(i-context_win,0),i) + range(i+1, min(i+1+context_win, size)):
                    
                    nb  = text[j]['lemma'] 
                    inv = text[j].get('negated', False) != neg
                    
                    graph[lem][nb]['inv' if inv else 'dir'] += context_win + 1 - abs(i-j)
    
        for lemma in graph: # The weights are generated as a markovian model
            
            total_dir = sum([ ady['dir'] for ady in graph[lemma].values() ]) * 1.0 + 1e-7
            
            total_inv = sum([ ady['inv'] for ady in graph[lemma].values() ]) * 1.0 + 1e-7
            
            for edge in graph[lemma]:
                
                graph[lemma][edge]['dir'] = (graph[lemma][edge]['dir'] / total_dir) * max_weight
                 
                graph[lemma][edge]['inv'] = (graph[lemma][edge]['inv'] / total_inv) * max_weight
                
        return graph
    
    
    def __repr__(self):
        return "< %s.%s - %s >" % (self.__class__.__module__, self.__class__.__name__,self.source)
    
    
    def __str__(self):
        return "%s(%s)" % ( self.__class__.__name__ , self.source )
    
    
    def __getitem__(self, word):
        return self._graph[word]
    
    
    def __contains__(self, word):
        return word in self._graph.keys()
    
    
    def has(self, word):
        return word in self._graph.keys()
    
    
    def edges(self, word, direction=None):
        if not self.has(word):
            raise []
        if not direction:
            return self._graph[word].items()
        if direction not in ['dir','inv']:
            raise ValueError('Expected keyword argument \'direction\' to be dir(ected) or inv(erted).')
        return [ (wd,pt[direction]) for wd,pt in self._graph[word].items() if pt[direction] != 0 ]
    
    
    def nodes(self):
        return self._graph.keys()
    
    
    def adjacents(self, word, direction=None):
        if not self.has(word):
            return []
        if not direction:
            return Iterable( self._graph[word].keys() )
        if direction not in ['dir','inv']:
            raise ValueError('Expected keyword argument \'direction\' to be dir(ected) or inv(erted).')
        return Iterable( wd for wd,pt in self._graph[word].items() if pt[direction] != 0 ) 
    
    
    def incidents(self, word, direction=None):
        if not self.has(word):
            return []
        if not direction:
            return Iterable( wd for wd,adys in self._graph.items() if word in adys )
        if direction not in ['dir','inv']:
            raise ValueError('Expected keyword argument \'direction\' to be dir(ected) or inv(erted).')
        return Iterable( wd for wd,adys in self._graph.items() if word in adys and adys['word'].has_key(direction) )
    
    
    def remove(self, word):
        for ady in self._graph.values():
            try: del ady[word] 
            except KeyError: pass
        try: del self._graph[word]
        except: pass
        
        
    def components(self,nodes=None):
        connected_components = []
        seeds = set(nodes.keys) if nodes else set(self._graph.keys) 
        while seeds:
            component = set()
            queue = set([seeds.pop()])
            visited = set()
            while queue:
                root = queue.pop()
                for edge in self._graph[root]:
                    if not edge in visited:
                        queue.add(edge)
                        if edge in seeds:
                            seeds.remove(edge)
            connected_components.append(component)
        return connected_components