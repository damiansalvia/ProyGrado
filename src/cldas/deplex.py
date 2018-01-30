# -*- encoding: utf-8 -*-
'''
Module for generating a context dependent lexicon corpus from a set of seeds

@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save, save_word_cloud
from cldas.utils.graph import ContextGraph, _search_influences
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
    lexicon = dict( sorted( lexicon.items(), key=lambda x:x[0] ) )
    
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
    @param graph                : A non-empty ContextGraph instance.
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
    
    if not isinstance(graph, ContextGraph):
        raise ValueError('Expected argument \'graph\' to be a ContextGraph instance.')
    
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



def by_distance(graph, seeds,
        threshold       = 0.001,
        penalty         = 0.8,
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
    @param graph                : A non-empty ContextGraph instance.
    @param seeds                : A set of words seeds with its polarity.
    @param threshold            : When stop sparsing valencies.
    @param penalty              : Penalty applied in case of cycle detection on edge.
    @param neu_treshold         : Treshold where valency is considered neutral.
    @param filter_seeds         : Output without seeds. 
    @param confidence:          : Minimum frequency nodes admitted in output.
    @param limit                : Limit output.
    @param seed_name            : Mechanism of how seeds are been made.
    @param verbose              : Verbose output.
    @param tofile               : Directory where lexicon and wordcloud will be saved.
    @param wc_neu               : Threshold consider for wordcloud when neu_treshold is None.
    '''
    
    lexicon = { 
        lem:{
            'val': seeds.get(lem,0),
            'inf': 1 if lem in seeds else 0
        } for lem in graph.nodes() }
    
    visited = { sem:[(sem,sem)] for sem in seeds.keys() } ; top = 0
    
    queue = sorted( seeds.items(), key=lambda x:x[1], reverse=True ) # max val first
    queue = [ (seed,seed,val) for seed,val in queue ]
    
    while queue:
        
        size = len(queue)
        top  = max(size,top)
        
        if verbose : progress("Building lexicon by bfs for %s" % graph.source,top,top-size)
        
        (seed,lem,val) = queue.pop(0)
        
        if lem not in graph or abs(val) < threshold:
            continue

        for ady,w in graph[lem].items():

            if (lem,ady) not in visited[seed]:
                visited[seed].append( (lem,ady) )

                _val = val * ( w['dir'] - w['inv'] )

                if abs(_val) > threshold: 
                    lexicon[ady]['val'] += val
                    lexicon[ady]['inf'] += 1
                    queue.append( (seed,ady,_val) )
    
    lexicon = _postprocess(lexicon, graph, "deplex_by_bfs", neu_treshold, filter_seeds, seeds, seed_name, limit, confidence, tofile, wc_neu)
        
    return lexicon



