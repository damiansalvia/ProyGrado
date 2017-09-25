# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
sys.path.append('../independent_system')
from utilities import *

import json
from _collections import defaultdict

from DataProvider import db
import DataProvider as dp

import numpy as np



def get_dependent_lexicon_by_graph(source,seeds_path,val_key,filter_neutral=True,limit=None):    
    graph  = defaultdict(lambda:{'val':0,'ady':[]})
    
    reviews = db.reviews.find({"source":source})
    
    total = reviews.count()    
    for idx,review in enumerate( reviews ):
        progress("Building graph for %s" % source,total,idx)
        text = review['text']        
        size = len(text)
        for i,item in enumerate(text):
            lem = item['lemma']           
            if i != 0: 
                nb  = text[i-1]['lemma'] # left word
                neg = text[i-1]['negated']
                if not (nb,neg) in graph[ lem ]['ady']: 
                    graph[ lem ]['ady'].append( (nb,neg) ) # (node,relation)
            if i != size-1:
                nb  = text[i+1]['lemma'] # right word
                neg = text[i+1]['negated']
                if not (nb,neg) in graph[ lem ]['ady']: 
                    graph[ lem ]['ady'].append( (nb,neg) ) # (node,relation)
                    
    count = { lemma['_id']:1 for lemma in dp.get_soruce_vocabulary(source) }
    
    seeds = json.load( open(seeds_path) ).items()
    queue = [ (lem,pol[val_key],1) for lem,pol in seeds ]
    top = 0
    
    while queue:
        size = len(queue)
        top  = max(size,top)         
        progress("Calculating valence",top,top-size)
        
        (lem,pol,vis) = queue.pop(0)
        
        if not graph.has_key(lem): # prune word not in vocabulary
            continue
        
        count[lem] += 1
        val = pol/vis 
        if abs(val) < 0.7: # prune neutral
            continue
        
        graph[lem]['val'] += val
        
        val = pol/(vis+1)
        if abs(val) < 0.7: # prune if next polarity doesn't contribute
            continue
        
        for idx,(ady,neg) in enumerate( graph[lem]['ady'] ):
            pol = -pol if neg else pol
            queue.append( (ady,val,vis+1) )
            
    result = { 
        lem:round( info['val'] * int(count[lem]/len(info['ady'])) , 3 ) # OBS: Trucating weight  
        for lem,info in graph.items()
    }
#     result = { 
#         lem:{
#             "val" :round( info['val'] * int(count[lem]/len(info['ady'])) , 3 ),
#             "freq":count[lem],
#             "adys":len(info['ady']),
#             "weight": 1.0 * count[lem]/len(info['ady'])
#         } for lem,info in graph.items() 
#     }
    
    if filter_neutral:
        result = dict( filter( lambda x: x[1]!=0 , result.items() ) )
    
    if limit:
        result = dict( sorted( result.items() , key=lambda x: abs(x[1]) , reverse=True )[:limit] )
        
    suffix = "_top%i" % limit if limit else ""
    save(result,"dependent_lexicon_by_graph_%s_li%i" % (source,len(seeds)) + suffix,"../lexicon/dependent")


for source in dp.get_sources():    
    get_dependent_lexicon_by_graph(
        source=source,
        seeds_path='../lexicon/independent/indepentent_lexicon_by_senti_tfidf_150_80p.json',
        val_key='rank',
        limit = 300
    )

