# -*- encoding: utf-8 -*-
'''
Module for generating a context dependent lexicon corpus from a set of seeds

@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save, save_word_cloud
from cldas.utils.graph import MultiGraph, _search_influences
from collections import defaultdict


def _postprocess(lexicon, graph, method, neu_treshold, filter_seeds, seeds, seed_name, limit, confidence, tofile, wc_neu):
    
    lexicon = dict( filter( lambda item: item[0] in graph.nodes() , lexicon.items() ) ) 
    
    if neu_treshold is not None:
        wc_neu = neu_treshold
        lexicon = dict( filter( lambda item: abs( item[1]['val'] ) > neu_treshold , lexicon.items() ) )
         
    if filter_seeds is True:
        lexicon = dict( filter( lambda item: item[0] not in seeds , lexicon.items() ) ) 
     
    if limit is not None:
        lexicon = dict( filter( lambda item: item[1]['inf'] >= confidence , lexicon.items() ) )
        lexicon = dict( sorted( lexicon.items() , key=lambda item: abs( item[1]['val'] ) , reverse=True )[:limit] )
        
    lexicon = { lem:{'val':round(item['val'],5),'inf':item['inf']} for lem,item in lexicon.items() }
    
    if tofile:
        name  = "_%s" % graph.source
        name += "_top%03i" % limit if limit else ""
        name += "_%s%03i" % (seed_name,len(seeds))
        name = method + name
        save( lexicon , name , tofile )
        save_word_cloud( lexicon, name, tofile, neu_treshold=wc_neu )
    
    return lexicon



def by_influence(graph, seeds, 
        threshold          = 0.005,  
        neutral_resistance = 1,
        neu_treshold       = None,
        filter_seeds       = False, 
        confidence         = 0,
        limit              = None, 
        seed_name          = "",
        verbose            = True,
        tofile             = None,
        wc_neu             = 0.0
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Influence Search like model.
    @param graph                : A non-empty MultiGraph instance.
    @param seeds                : A set of words seeds with its valencies.
    @param threshold            : Minimum admitted influence for sparcing between nodes.
    @param neutral_resistance   : Adds neutral adyacency nodes. 
    @param neu_treshold         : Treshold where valency is considered neutral.
    @param filter_seeds         : Output without seeds.
    @param confidence:          : Minimum influence admitted in output. 
    @param limit                : Limit output.
    @param seed_name            : Mechanism of how seeds are been made.
    @param verbose              : Verbose output.
    @param tofile               : Directory where lexicon and wordcloud will be saved. 
    @param wc_neu               : Threshold consider for wordcloud when neu_treshold is None. 
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
            "inf": round(influence,2)              
        }
        
    lexicon = _postprocess(lexicon, graph, "deplex_by_influence", neu_treshold, filter_seeds, seeds, seed_name, limit, confidence, tofile, wc_neu)
        
    return lexicon



def by_bfs(graph, seeds,
        threshold       = 0.005,
        neu_treshold    = None,
        filter_seeds    = False,
        confidence      = 1, 
        limit           = None, 
        seed_name       = "",
        verbose         = True,
        tofile          = None,
        wc_neu          = 0.0
    ):
    '''
    Generates a lexicon from an opinion set and seeds words by Breath First Search model
    @param graph                : A non-empty MultiGraph instance.
    @param seeds                : A set of words seeds with its polarity.
    @param threshold            : When stop sparsing valencies.
    @param neu_treshold         : Treshold where valency is considered neutral.
    @param filter_seeds         : Output without seeds. 
    @param confidence:          : Minimum frequency nodes admitted in output.
    @param limit                : Limit output.
    @param seed_name            : Mechanism of how seeds are been made.
    @param verbose              : Verbose output.
    @param tofile               : Directory where lexicon and wordcloud will be saved.
    @param wc_neu               : Threshold consider for wordcloud when neu_treshold is None.
    '''
    
    lexicon = { lem:{'val':0,'inf':0} for lem in graph.nodes() }
    
    visited_dir = [] ; visited_inv = []
    
    queue = seeds.items() ; top = 0
    
    while queue:
        
        size = len(queue)
        top  = max(size,top)
        
        if verbose : progress("Building lexicon by bfs for %s" % graph.source,top,top-size)
        
        (lem,val) = queue.pop(0)
        
        if lem not in graph or abs(val) < threshold:
            continue
        
        lexicon[lem]['val'] += val
        lexicon[lem]['inf'] += 1
        
        for ady,edge in graph[lem].items():
            
            _val = val * edge['dir'] 
            if (lem,ady) not in visited_dir and abs(_val) > threshold: 
                visited_dir.append( (lem,ady) )
                queue.append( (ady,_val) )
                
            _val = -val * edge['inv'] 
            if (lem,ady) in visited_inv and abs(_val) > threshold: 
                visited_inv.append( (lem,ady) )
                queue.append( (ady,_val) )
    
    lexicon = _postprocess(lexicon, graph, "deplex_by_bfs", neu_treshold, filter_seeds, seeds, seed_name, limit, confidence, tofile, wc_neu)
        
    return lexicon



