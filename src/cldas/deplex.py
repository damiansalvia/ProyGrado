# -*- encoding: utf-8 -*-
'''
Module for generating a context dependent lexicon corpus from a set of seeds

@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save, save_word_cloud
from cldas.utils.graph import MultiGraph, _search_influences
from collections import defaultdict


def by_influence(graph, seeds, 
        threshold          = 0.005,  
        neutral_resistance = 1,
        filter_neutral     = True,
        filter_seeds       = False, 
        confidence         = 0,
        limit              = None, 
        seed_name          = "",
        verbose            = True,
        tofile             = None,
        wdcloud            = False
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Influence Search like model.
    @param graph                : A non-empty MultiGraph instance.
    @param seeds                : A set of words seeds with its valencies.
    @param threshold            : 
    @param neutral_resistance   : Adds neutral adyacency nodes. 
    @param filter_neutrals      : Output without neutrals.
    @param filter_seeds         : Output without seeds.
    @param confidence:          : Minimum influence admitted in output 
    @param limit                : Limit output.
    @param seed_name            : Mechanism of how seeds are been made.
    @param verbose              : Verbose output.
    @param tofile               : Directory where lexicon and wordcloud will be saved. 
    @param wdcloud              : Generate a word cloud image. Argument tofile required.
    '''
    
    if not isinstance(graph, MultiGraph):
        raise ValueError('Expected argument \'graph\' to be a MultiGraph instance.')
    
    if not seeds:
        raise ValueError('Expected argiment \'seeds\' not null.')
    
    influences = defaultdict(list) ; total = len(seeds)
    
    for idx, seed in enumerate(seeds):
        
        if verbose : progress("Processing seeds for %s" % graph.source, total,idx)
        
        nodes_influences = _search_influences(graph, seed, threshold)
        
        for w in nodes_influences:
            influences[w].append( (seeds[seed] *  1, nodes_influences[w][0]) )
            influences[w].append( (seeds[seed] * -1, nodes_influences[w][1]) )
        
    
    lexicon = {} ; total = len(influences)
    
    total_influence = total    
    for idx, lemma in enumerate(influences):
        
        if verbose : progress("Building lexicon by influence for %s" % graph.source,total,idx)
        
        influence = sum([ inf[1] for inf in influences[lemma] ]) 
        
        if lemma not in seeds.keys():
            total_influence = influence + neutral_resistance * 1.0
            
        lexicon[lemma] = {
            "val": sum([ inf[0] * inf[1] for inf in influences[lemma] ]) / total_influence,
            "inf": influence              
        }
        
    if filter_neutral:
        lexicon = dict( filter( lambda item: abs( item[1]['val'] ) > 0.3 , lexicon.items() ) )
         
    if filter_seeds:
        lexicon = dict( filter( lambda item: item[0] not in seeds , lexicon.items() ) ) 
     
    if limit:
        lexicon = dict( filter( lambda item: item[1]['inf'] >= confidence , lexicon.items() ) )
        lexicon = dict( sorted( lexicon.items() , key=lambda item: abs( item[1]['val'] ) , reverse=True )[:limit] )
        
    lexicon = { lem:round(item['val'],3) for lem,item in lexicon.items() }
    
    if tofile:
        name  = "_%s" % graph.source
        name += "_top%03i" % limit if limit else ""
        name += "_%s%03i" % (seed_name,len(seeds))
        name = "deplex_by_influence" + name
        save( lexicon , name , tofile )
        if wdcloud: save_word_cloud( lexicon, name, tofile )
        
    return lexicon



def by_bfs(graph, seeds,
        threshold       = 0.005,
        filter_neutral  = True,
        filter_seeds    = False, 
        limit           = None, 
        seed_name       = "",
        verbose         = True,
        tofile          = None,
        wdcloud         = False,
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Breath First Search model
    @param graph                : A non-empty MultiGraph instance.
    @param seeds                : A set of words seeds with its polarity.
    @param threshold            : When stop sparsing valencies. 
    @param filter_neutrals      : Output without neutrals.
    @param filter_seeds         : Output without seeds. 
    @param limit                : Limit output.
    @param seed_name            : Mechanism of how seeds are been made.
    @param verbose              : Verbose output.
    @param tofile               : Directory where lexicon and wordcloud will be saved.
    @param wdcloud              : Generate a word cloud image. Argument tofile required.
    '''
    
    lexicon = { lem:0 for lem in graph.nodes() }
    
    visited_dir = [] ; visited_inv = []
    
    queue = seeds.items() ; top = 0
    
    while queue:
        
        size = len(queue)
        top  = max(size,top)
        
        if verbose : progress("Building lexicon by bfs for %s" % graph.source,top,top-size)
        
        (lem,val) = queue.pop(0)
        
        if lem not in graph or abs(val) < threshold:
            continue
        
        lexicon[lem] += val
        
        for ady,edge in graph[lem].items():
            
            _val = val * edge['dir'] 
            if (lem,ady) not in visited_dir and abs(_val) > threshold: 
                visited_dir.append( (lem,ady) )
                queue.append( (ady,_val) )
                
            _val = -val * edge['inv'] 
            if (lem,ady) in visited_inv and abs(_val) > threshold: 
                visited_inv.append( (lem,ady) )
                queue.append( (ady,_val) )
    
    if filter_neutral:
        lexicon = dict( filter( lambda item: abs( item[1] ) > 0.3 , lexicon.items() ) )
        
    if filter_seeds:
        lexicon = dict( filter( lambda item: item[0] not in seeds , lexicon.items() ) ) 
    
    if limit:
        lexicon = dict( sorted( lexicon.items() , key=lambda item: abs( item[1] ) , reverse=True )[:limit] )
    
    lexicon = { lem:round(val,3) for lem,val in lexicon.items() }
    
    if tofile:
        name  = "_%s" % graph.source
        name += "_top%03i" % limit if limit else ""
        name += "_%s%03i" % (seed_name,len(seeds))
        name = "deplex_by_bfs" + name
        save( lexicon , name , tofile )
        if wdcloud: save_word_cloud( lexicon, name, tofile )
        
    return lexicon



