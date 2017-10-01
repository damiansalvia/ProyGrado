# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
sys.path.append('../independent_system')
from utilities import *

import math
import json
from _collections import defaultdict

from DataProvider import db
import DataProvider as dp

FLATTNER = 5000

PREFIX_TAGS = [
    'AQ', # Adjetivo calificativos     - EJ: alegre   -
    # 'AO', # Adjetivo ordinales         - EJ: primer   -
    'RG', # Adverbio General           - EJ: despacio -
    # 'RN', # Adverbio Negativo          - EJ: no       -
    'DD', # Determinante Demostrativo  - EJ: este     -
    'NC', # Nombre Comun               - EJ: gato     -
    # 'NP', # Nombre Propio              - EJ: Pedro    -
    'VM', # Verbo Principal            - EJ: Pedro    -
    # 'VA', # Verbo Auxiliar             - EJ: habia    -
    # 'VS', # Verbo Semiauxiliar         - EJ: es       -
    'PD', # Pronombre Demostrativo     - EJ: aquel    -
    'PI'  # Pronombre Indefinido       - EJ: bastante -
]


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
                inv = text[i-1]['negated']
                if not (nb,inv) in graph[ lem ]['ady']: 
                    graph[ lem ]['ady'].append( (nb,inv) ) # (node,relation)
            if i != size-1:
                nb  = text[i+1]['lemma'] # right word
                inv = text[i+1]['negated']
                if not (nb,inv) in graph[ lem ]['ady']: 
                    graph[ lem ]['ady'].append( (nb,inv) ) # (node,relation)
                    
    count = { lemma['_id']:1 for lemma in dp.get_soruce_vocabulary(source) }
    
    seeds = json.load( open(seeds_path) ).items()
    queue = [ (lemma,pol[val_key],1) for lemma,pol in seeds ]
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
        
        for idx,(ady,inv) in enumerate( graph[lem]['ady'] ):
            pol = -pol if inv else pol
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
        result = dict( filter( lambda x: x[1]!=0 , result.items() ))
    
    if limit:
        result = dict( sorted( result.items() , key=lambda x: abs(x[1]) , reverse=True )[:limit] )
        
    suffix = "_top%i" % limit if limit else ""
    save(result,"dependent_lexicon_by_graph_%s_li%i" % (source,len(seeds)) + suffix,"../lexicon/dependent")


# Sigmoideal function to calculate weight based on edge ocurrence (CURRENTLY DEPRECATED)
def sigmoid(x):
    x = x + 0
    return x / math.sqrt( FLATTNER + x**2)


def valid_tag(tag, list):
    for prefix in list:
        if tag.startswith(prefix):
            return True
    return False


def generate_graph(reviews, source, prefix_tag_list, max_weight, win = 1):
    ''' Generates the weighted bidirectional multigraph corresponding to reviews
    '''
    graph = defaultdict(lambda:{ 'ady':defaultdict(lambda:{ 'p_dir':0 , 'p_inv':0 }) })
    total = reviews.count()  
    for idx,review in enumerate( reviews ):
        progress("Building graph for %s" % source,total,idx)
        text = review['text']   

        # Remove tokens having unrelevant information
        if prefix_tag_list:
            text =  [token for token in text if valid_tag( token['tag'], prefix_tag_list)]

        size = len(text)
        for i,item in enumerate(text):
            lem = item['lemma'] 
            is_negated_item = item.get('negated', False) 
            for j in range(max(i-win,0),i) + range(i+1, min(i+1+win, size)):
                nb  = text[j]['lemma'] 
                inv = text[j].get('negated', False) != is_negated_item
                graph[ lem ]['ady'][nb]['p_inv' if inv else 'p_dir'] += win + 1 - abs(i-j)

    for lemma in graph:
        # The weights are generated as a markovian model
        total_dir = sum([ x[1]['p_dir'] for x in graph[lemma]['ady'].items() ]) * 1.0 + 1e-7
        total_inv = sum([ x[1]['p_inv'] for x in graph[lemma]['ady'].items() ]) * 1.0 + 1e-7
        for edge in graph[lemma]['ady']:
            graph[lemma]['ady'][edge]['p_dir'] = (graph[lemma]['ady'][edge]['p_dir'] / total_dir) * max_weight 
            graph[lemma]['ady'][edge]['p_inv'] = (graph[lemma]['ady'][edge]['p_inv'] / total_inv) * max_weight 
    return dict(graph)

def dijkstra(graph, initial):
    influence = {initial: (1, 0)}
    nodes = set(graph.keys())

    while nodes: 
        next_node = None
        for node in nodes:
            if node in influence:
                if next_node is None:
                    next_node = node
                elif influence[node] > influence[next_node]:
                    next_node = node

        if next_node is None:
            break

        nodes.remove(next_node)
        current_weight = influence[next_node]

        for edge in graph[next_node]['ady']:
            weight = current_weight * graph[next_node]['ady'][edge]['p_dir']
            if edge not in influence or weight > influence[edge]:
                influence[edge] = weight
    return influence

def get_dependent_lexicon_by_dijkstra(source, reviews, seeds, 
    prefix_tag_list  = None, 
    filter_neutral = True, 
    limit = None, 
    neutral_resistance = 1,
    max_weight = 1
    ):

    # Create Graph
    graph = generate_graph(reviews, source, prefix_tag_list, max_weight)
    influences = defaultdict(list)
    for seed in seeds:
        nodes_weights = dijkstra(graph, seed)
        for w in nodes_weights:
            influences[w].append((seeds[seed], nodes_weights[w]))

    result = {}
    for lemma in influences:
        total_influence = sum([ inf[1] for inf in influences[lemma] ]) 
        if lemma not in seeds.keys():
            total_influence += neutral_resistance * 1.0
        result[lemma] = sum([ inf[0] * inf[1] for inf in influences[lemma] ]) / total_influence

    if filter_neutral:
        result = dict( filter( lambda x: x[1]!=0 , result.items() ) )
    
    if limit:
        result = dict( sorted( result.items() , key=lambda x: abs(x[1]) , reverse=True )[:limit] )
        
    suffix = "_top%i" % limit if limit else ""
    save(result,"dependent_lexicon_by_dijkstra_%s_li%i" % (source,len(seeds)) + suffix,"../lexicon/dependent")

if __name__=='__main__':

    # for source in dp.get_sources():    
    #     get_dependent_lexicon_by_graph(
    #         source=source,
    #         seeds_path='indepentent_lexicon.json',
    #         val_key='rank',
    #         limit = 300
    #     )
    
    # source = 'test'
    # # seeds = { lem:pol[val_key] for lem,pol in json.load( open(seeds_path) ).items() }
    # seeds = { "genial": 4.8748148332370644 }
    # reviews = db.reviews.find({"source":source})

    # get_dependent_lexicon_by_dijkstra(source, reviews, seeds, prefix_tag_list = PREFIX_TAGS )

    graph = {
        'A': { 'val':[], 'ady':{
            'B':{'p_dir': 0.8 },
            'C':{'p_dir': 0.1 }
        }},
        'B': { 'val':[], 'ady':{
            'A':{'p_dir': 0.8 },
            'D':{'p_dir': 0.5 }
        }},
        'C': { 'val':[], 'ady':{
            'A':{'p_dir': 0.1 },
            'D':{'p_dir': 0.5 },
        }},
        'D': { 'val':[], 'ady':{
            'B':{'p_dir': 0.5 },
            'C':{'p_dir': 0.5 },
        }}
    }

    print dijkstra(graph, 'A')
