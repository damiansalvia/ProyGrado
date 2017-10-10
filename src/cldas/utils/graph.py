# -*- encoding: utf-8 -*-
'''
Module for for generating a context dependent lexicon corpus and seeds

@author: Nicolás Mechulam, Damián Salvia
'''

from _collections import defaultdict
from cldas.utils import progress


def _valid_tag(tag, tagset):
    for prefix in tagset:
        if tag.startswith(prefix): return True
    return False


def _generate_graph(opinions, source, filter_tags, max_weight, win, verbose=True):
    
    graph = defaultdict(lambda : defaultdict(lambda: {'p_dir': 0, 'p_inv':0}))
     
    total = len( list( opinions ) ) 
    for idx,opinion in enumerate( opinions ):
        
        if verbose : progress("Building graph for %s" % source,total,idx)

        text = opinion['text']   

        if filter_tags: # Remove tokens having irrelevant information
            text =  [token for token in text if _valid_tag( token['tag'] , filter_tags ) ]

        size = len(text)
        for i,item in enumerate(text):
            
            lem = item['lemma']
             
            neg = item.get('negated', False)
             
            for j in range(max(i-win,0),i) + range(i+1, min(i+1+win, size)):
                
                nb  = text[j]['lemma'] 
                inv = text[j].get('negated', False) != neg
                
                graph[lem][nb]['p_inv' if inv else 'p_dir'] += win + 1 - abs(i-j)

    for lemma in graph: # The weights are generated as a markovian model
        
        total_dir = sum([ ady['p_dir'] for ady in graph[lemma].values() ]) * 1.0 + 1e-7
        
        total_inv = sum([ ady['p_inv'] for ady in graph[lemma].values() ]) * 1.0 + 1e-7
        
        for edge in graph[lemma]:
            
            graph[lemma][edge]['p_dir'] = (graph[lemma][edge]['p_dir'] / total_dir) * max_weight
             
            graph[lemma][edge]['p_inv'] = (graph[lemma][edge]['p_inv'] / total_inv) * max_weight
             
    return dict(graph)


def _search_influences(graph, initial, threshold):

    influence = defaultdict(lambda:[0,0])
    influence[initial] = [1, 0]
    
    visited_dir = []
    visited_inv = []

    nodes = set(graph.keys())
    
    while nodes: 

        next_dir = None
        next_inv = None
        
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
                    
                    dir_weight = current_dir_w * graph[next_dir][edge]['p_dir']
                    inv_weight = current_dir_w * graph[next_dir][edge]['p_inv']
                    
                    if dir_weight > influence[edge][0]:
                        influence[edge][0] = dir_weight
                        
                    if inv_weight > influence[edge][1]:
                        influence[edge][1] = inv_weight

        if next_inv:
            visited_inv.append(next_inv)
            current_inv_w = influence[next_inv][1]
            
            for edge in graph[next_inv]:
                
                if edge not in visited_inv:
                    
                    dir_weight = current_inv_w * graph[next_inv][edge]['p_inv']
                    inv_weight = current_inv_w * graph[next_inv][edge]['p_dir']
                    
                    if dir_weight > influence[edge][0]:
                        influence[edge][0] = dir_weight
                        
                    if inv_weight > influence[edge][1]:
                        influence[edge][1] = inv_weight

    return dict(influence)