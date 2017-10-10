# -*- encoding: utf-8 -*-
'''
Module for generating a context dependent lexicon corpus and seeds

@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save
from cldas.utils.graph import _generate_graph, _search_influences
from _collections import defaultdict


def by_influence(source, opinions, seeds, 
        filter_tags        = None,
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
    Generates a lexicon from an opinion set and seeds words by Influence Search like model
    '''
    
    graph = _generate_graph(opinions, source, filter_tags, max_weight, context_window, verbose=verbose)
    
    influences = defaultdict(list) ; total = len(seeds)
    
    for idx, seed in enumerate(seeds):
        
        if verbose : progress("Processing seeds for %s" % source, total,idx)
        
        nodes_influences = _search_influences(graph, seed, threshold)
        
        for w in nodes_influences:
            influences[w].append( (seeds[seed] *  1, nodes_influences[w][0]) )
            influences[w].append( (seeds[seed] * -1, nodes_influences[w][1]) )
        
    
    lexicon = {} ; total = len(influences)
    
    for idx, lemma in enumerate(influences):
        
        if verbose : progress("Building lexicon by influence for %s" % source,total,idx)
        
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
        save( lexicon , "deplex_by_influence" + suffix , tofile )
        
    return lexicon



def by_bfs(source, opinions, seeds, 
        filter_tags     = None,
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
    
    graph = _generate_graph(opinions, source, filter_tags, max_weight, context_window, verbose=verbose)
    
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



