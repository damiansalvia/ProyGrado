# -*- encoding: utf-8 -*-
'''
Module for for generating a context dependent lexicon corpus and seeds
@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save
from _collections import defaultdict


def _valid_tag(tag, tagset):
    for prefix in tagset:
        if tag.startswith(prefix): return True
    return False


def _generate_graph(opinions, source, prefix_tag_list, max_weight, win, verbose=True):
    
    graph = defaultdict(lambda : defaultdict(lambda: {'p_dir': 0, 'p_inv':0}))
     
    total = len( list( opinions ) ) 
    for idx,opinion in enumerate( opinions ):
        
        if verbose : progress("Building graph for %s" % source,total,idx)

        text = opinion['text']   

        if prefix_tag_list: # Remove tokens having irrelevant information
            text =  [token for token in text if _valid_tag( token['tag'] , prefix_tag_list ) ]

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


def _dijkstra(graph, initial, threshold):

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



def by_dijkstra(source, opinions, seeds, 
        prefix_tag_list    = None,
        max_weight         = 1,
        threshold          = 0.005,
        context_window     = 1,  
        neutral_resistance = 1,
        filter_neutral     = True,
        filter_seeds       = True, 
        limit              = None, 
        verbose            = True,
        tofile             = None
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Dijkstra Search like model
    '''
    
    graph = _generate_graph(opinions, source, prefix_tag_list, max_weight, context_window, verbose=verbose)
    
    influences = defaultdict(list) ; total = len(seeds)
    
    for idx, seed in enumerate(seeds):
        
        if verbose : progress("Processing seeds for %s" % source, total,idx)
        
        nodes_influences = _dijkstra(graph, seed, threshold)
        
        for w in nodes_influences:
            influences[w].append( (seeds[seed] *  1, nodes_influences[w][0]) )
            influences[w].append( (seeds[seed] * -1, nodes_influences[w][1]) )
        
    
    lexicon = {} ; total = len(influences)
    
    for idx, lemma in enumerate(influences):
        
        if verbose : progress("Building lexicon by dijkstra for %s" % source,total,idx)
        
        total_influence = sum([ inf[1] for inf in influences[lemma] ]) 
        
        if lemma not in seeds.keys():
            total_influence += neutral_resistance * 1.0
            
        lexicon[lemma] = sum([ inf[0] * inf[1] for inf in influences[lemma] ]) / total_influence
        
    if filter_neutral:
        lexicon = dict( filter( lambda item: abs( item[1] ) > 0.3 , lexicon.items() ) )
    
    if limit:
        lexicon = dict( sorted( lexicon.items() , key=lambda item: abs( item[1] ) , reverse=True )[:limit] )
        
    if filter_seeds:
        lexicon = dict( filter( lambda item: item[0] not in seeds , lexicon.items ) ) 
    
    if tofile:
        suffix  = "_%s" % source
        suffix += "_top%03i" % limit if limit else ""
        suffix += "_seeds%03i" % len(seeds)
        save( lexicon , "deplex_by_dijkstra" + suffix , tofile )
        
    return lexicon



def by_bfs(source, opinions, seeds, 
        prefix_tag_list = None,
        max_weight      = 1, 
        threshold       = 0.005,
        context_window  = 1, 
        filter_neutral  = True,
        filter_seeds    = True, 
        limit           = None,
        verbose         = True,
        tofile          = None
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Breath First Search model
    '''
    
    graph = _generate_graph(opinions, source, prefix_tag_list, max_weight, context_window, verbose=verbose)
    
    lexicon = { lem:0 for lem in graph.keys() }
    
    visited_dir = [] ; visited_inv = []
    
    queue = seeds.items() ; top = 0
    
    while queue:
        
        size = len(queue)
        top  = max(size,top)
        
        if verbose : progress("Building lexicon by bfs for %s" % source,top,top-size)
        
        (lem,val) = queue.pop(0)
        
        if not graph.has_key(lem) or abs(val) < threshold:
            continue
        
        lexicon[lem] += val
        
        for ady,edge in graph[lem].items():
            
            _val = val * edge['p_dir'] 
            if (lem,ady) not in visited_dir and abs(_val) > threshold: 
                visited_dir.append( (lem,ady) )
                queue.append( (ady,_val) )
                
            _val = -val * edge['p_inv'] 
            if (lem,ady) in visited_inv and abs(_val) > threshold: 
                visited_inv.append( (lem,ady) )
                queue.append( (ady,_val) )
    
    if filter_neutral:
        lexicon = dict( filter( lambda item: abs( item[1] ) > 0.3 , lexicon.items() ) )
    
    if limit:
        lexicon = dict( sorted( lexicon.items() , key=lambda item: abs( item[1] ) , reverse=True )[:limit] )
        
    if filter_seeds:
        lexicon = dict( filter( lambda item: item[0] not in seeds , lexicon.items() ) ) 
    
    if tofile:
        suffix  = "_%s" % source
        suffix += "_top%03i" % limit if limit else ""
        suffix += "_seeds%03i" % len(seeds)
        save( lexicon , "deplex_by_bfs" + suffix , tofile )
        
    return lexicon



