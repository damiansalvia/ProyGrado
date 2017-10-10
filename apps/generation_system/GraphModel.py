# -*- coding: utf-8 -*-
import time
import sys
sys.path.append('../utilities')
sys.path.append('../independent_system')
from utilities import *

import json
from _collections import defaultdict

from DataProvider import db
import DataProvider as dp


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


TEST_GRAPHS = [
        ({
            'A': {
                'B':{'p_dir': 0.5, 'p_inv': 0.0}
            },
            'B': {
                'C':{'p_dir': 0.0, 'p_inv': 0.5}
            },
            'C': {
            }
        },{'A':[1,0], 'B': [0.5, 0], 'C': [0, 0.25] }),
        ({
            'A': {
                'B':{'p_dir': 0.8, 'p_inv': 0.0},
                'C':{'p_dir': 0.0, 'p_inv': 0.8}
            },
            'B': {
                'D':{'p_dir': 0.8, 'p_inv': 0.5}
            },
            'C': {
                'D':{'p_dir': 0.8, 'p_inv': 0.5}
            },
            'D': {
                'E':{'p_dir': 0.8, 'p_inv': 0.8}
            },
            'E': {
            }
        },{'A':[1,0], 'B': [0.8, 0], 'C': [0, 0.8], 'D': [0.64,0.64] , 'E': [0.512,0.512] }),
    ]


# def get_dependent_lexicon_by_graph(source,seeds_path,val_key,filter_neutral=True,limit=None):    
#     graph  = defaultdict(lambda:{'val':0,'ady':[]})
#     
#     reviews = db.reviews.find({"source":source})
#     
#     total = reviews.count()    
#     for idx,review in enumerate( reviews ):
#         progress("Building graph for %s" % source,total,idx)
#         text = review['text']        
#         size = len(text)
#         for i,item in enumerate(text):
#             lem = item['lemma']           
#             if i != 0: 
#                 nb  = text[i-1]['lemma'] # left word
#                 neg = text[i-1]['negated']
#                 if not (nb,neg) in graph[ lem ]['ady']: 
#                     graph[ lem ]['ady'].append( (nb,neg) ) # (node,relation)
#             if i != size-1:
#                 nb  = text[i+1]['lemma'] # right word
#                 neg = text[i+1]['negated']
#                 if not (nb,neg) in graph[ lem ]['ady']: 
#                     graph[ lem ]['ady'].append( (nb,neg) ) # (node,relation)
#                     
#     count = { lemma['_id']:1 for lemma in dp.get_soruce_vocabulary(source) }
#     
#     seeds = json.load( open(seeds_path) ).items()
#     queue = [ (lem,pol[val_key],1) for lem,pol in seeds ]
#     top = 0
#     
#     while queue:
#         size = len(queue)
#         top  = max(size,top)         
#         progress("Calculating valence",top,top-size)
#         
#         (lem,pol,vis) = queue.pop(0)
#         
#         if not graph.has_key(lem): # prune word not in vocabulary
#             continue
#         
#         count[lem] += 1
#         val = pol/vis 
#         if abs(val) < 0.7: # prune neutral
#             continue
#         
#         graph[lem]['val'] += val
#         
#         val = pol/(vis+1)
#         if abs(val) < 0.7: # prune if next polarity doesn't contribute
#             continue
#         
#         for idx,(ady,neg) in enumerate( graph[lem]['ady'] ):
#             pol = -pol if neg else pol
#             queue.append( (ady,val,vis+1) )
#             
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
                if not (nb,inv) in graph[ lem ]: 
                    graph[ lem ].append( (nb,inv) ) # (node,relation)
            if i != size-1:
                nb  = text[i+1]['lemma'] # right word
                inv = text[i+1]['negated']
                if not (nb,inv) in graph[ lem ]: 
                    graph[ lem ].append( (nb,inv) ) # (node,relation)
                    
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
        
        for idx,(ady,inv) in enumerate( graph[lem] ):
            pol = -pol if inv else pol
            queue.append( (ady,val,vis+1) )
    
    result = { 
        lem:{
            "val" :round( info['val'] * int(count[lem]/len(info)) , 3 ),
            "freq":count[lem],
            "adys":len(info),
            "weight": 1.0 * count[lem]/len(info)
        } for lem,info in graph.items() 
    }
    
    if filter_neutral:
        result = dict( filter( lambda x: x[1]!=0 , result.items() ))
    
    if limit:
        result = dict( sorted( result.items() , key=lambda x: abs(x[1]) , reverse=True )[:limit] )
        
    suffix = "_top%i" % limit if limit else ""
    save(result,"dependent_lexicon_by_graph_%s_li%i" % (source,len(seeds)) + suffix,"../lexicon/dependent")

def valid_tag(tag, list):
    for prefix in list:
        if tag.startswith(prefix):
            return True
    return False


def generate_graph(reviews, source, prefix_tag_list  = None, max_weight = 1, graph_context_window = 1):
    ''' Generates the weighted bidirectional multigraph corresponding to reviews
    '''
    graph = defaultdict(lambda : defaultdict(lambda: {'p_dir': 0, 'p_inv':0}))
    # graph = defaultdict(lambda:{ 'p_dir':0 , 'p_inv':0 })
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
                graph[ lem ][nb]['p_inv' if inv else 'p_dir'] += win + 1 - abs(i-j)

    for lemma in graph:
        # The weights are generated as a markovian model
        total_dir = sum([ x[1]['p_dir'] for x in graph[lemma].items() ]) * 1.0 + 1e-7
        total_inv = sum([ x[1]['p_inv'] for x in graph[lemma].items() ]) * 1.0 + 1e-7
        for edge in graph[lemma]:
            graph[lemma][edge]['p_dir'] = (graph[lemma][edge]['p_dir'] / total_dir) * max_weight 
            graph[lemma][edge]['p_inv'] = (graph[lemma][edge]['p_inv'] / total_inv) * max_weight 
    return dict(graph)

def dijkstra(graph, initial, threshold):

    influence = defaultdict(lambda:[0,0])
    influence[initial] = [1, 0]
    
    visited_dir = []
    visited_inv = []

    nodes = set(graph.keys())
    while nodes: 

        next_dir = None
        next_inv = None
        for node in nodes:
            # Select best direct node and best inverse node
            # (It can be the dame node) 
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

def get_dependent_lexicon_by_dijkstra(source, graph , seeds, 
    filter_neutral = True, 
    limit = None, 
    neutral_resistance = 1,
    filter_seeds = True, 
    dijkstra_threshold = 0.005,
    ):

   
    influences = defaultdict(list)
    total_seeds = len(seeds)
    print '\nPROCESS SEEDS'
    start = time.time()
    for idx, seed in enumerate(seeds):
        nodes_influences = dijkstra(graph, seed, dijkstra_threshold)
        for w in nodes_influences:
            # Direct influnece
            influences[w].append((seeds[seed], nodes_influences[w][0]))
            # Inverse influence
            influences[w].append((seeds[seed] * -1, nodes_influences[w][1]))
        
        progress("Processing seed: ", total_seeds,idx)
    elapsed = start - time.time()
    print 'Elapsed tiem: %d:%d ' % (elapsed / 60, elapsed % 60 )
    result = {}
    print '\nCREATE DEPENDENT LEXICON'
    total_influences = len(influences)
    progress("Creating dependent_lexicon", total_influences, -1)
    for idx, lemma in enumerate(influences):
        influnece = sum([ inf[1] for inf in influences[lemma] ]) 
        if lemma not in seeds.keys():
            total_influence = influnece + neutral_resistance * 1.0
        result[lemma] = {
            'valence': sum([ inf[0] * inf[1] for inf in influences[lemma] ]) / total_influence,
            'influence': influnece
        }
        progress("Creating dependent_lexicon", total_influences, idx)


    if filter_neutral:
        result = dict( filter( lambda x: abs(x[1]['valence']) > 0.3 , result.items() ) )
    
    if filter_seeds:
        result = dict( filter( lambda x: x[0] not in seeds , result.items() ) )
        
    if limit:
        result = dict( sorted( result.items() , key=lambda x: x[1]['influence'] , reverse=True )[:limit] )
        
    suffix = "_top%i" % limit if limit else ""
    save(result,"dependent_lexicon_by_dijkstra_%s_li%i" % (source,len(seeds)) + suffix,"../lexicon/dependent")
    return result


def dijkstra_evaluation(tests, seed):
    error = False
    for idx,test in enumerate(tests):
        graph  = test[0]
        expected = test[1]
        evaluation = dijkstra(graph, seed)
        if not evaluation == expected:
            error = True
            print 'Error in test %d :' % (idx + 1)
            print '    EVALUATED: ',  evaluation
            print '    EXPECTED : ',  expected

    if not error:
        print 'Every test was succesfull' 


def get_connected_component(graph, nodes = None):
    connected_components = []
    if nodes:
        seeds = set(nodes.keys)
    else:
        seeds = set(graph.keys)
    while seeds:
        component = set()
        queue = set([seeds.pop()])
        visited = set()
        while queue:
            root = queue.pop()
            for edge in graph[root]:
                if not edge in visited:
                    queue.add(edge)
                    if edge in seeds:
                        seeds.remove(edge)
                        component.add(edge)
        connected_components.append(component)
    return connected_components


def get_GML(graph, lexicon):
    tab = ' '*4
    gml_nodes = ''
    gml_edges = ''
    for node, edges in graph.items():
        gml_nodes += '{br}node [{br}{t}id {node}{br}{t}value {val}{br}]'.format(
            t = tab,
            br = '\n' + tab,
            node = node, 
            val = lexicon[node] * 1.0
        )
        for edge, weights in edges.items():

            gml_edges += '{br}edge [{br}{t}source {node}{br}{t}target {edge}{br}{t}label direct{br}{t}weight {val} {br}]'.format(
                t = tab,
                br = '\n' + tab,
                node = node, 
                edge = edge, 
                val = weights['p_dir'] * 1.0
            )

            gml_edges += '{br}edge [{br}{t}source {node}{br}{t}target {edge}{br}{t}label inverse{br}{t}weight {val} {br}]'.format(
                t = tab,
                br = '\n' + tab,
                node = node, 
                edge = edge, 
                val = weights['p_inv'] * 1.0
            )
    gml = 'graph [' + gml_nodes + gml_edges + '\n]'
    return gml

if __name__=='__main__':

    # # for source in dp.get_sources():    
    # #     get_dependent_lexicon_by_graph(
    # #         source=source,
    # #         seeds_path='indepentent_lexicon.json',
    # #         val_key='rank',
    # #         limit = 300
    # #     )
    # seeds_path = '../lexicon/independent/independent_lexicon.json'
    # source = 'corpus_apps_android'
    # val_key = 'rank'
    # seeds = { lem:pol[val_key] for lem,pol in json.load( open(seeds_path) ).items() }
    # # seeds = { "genial": 4.8748148332370644 }
    # reviews = db.reviews.find({"source":source})

    # graph = generate_graph(reviews, source, 
    #     prefix_tag_list = PREFIX_TAGS, 
    #     max_weight = 1, 
    #     graph_context_window = 1
    # )

    # lexicon = get_dependent_lexicon_by_dijkstra(source, reviews, seeds,
    #     prefix_tag_list  = PREFIX_TAGS, 
    #     filter_neutral = True, 
    #     limit = None, 
    #     neutral_resistance = 1,
    #     max_weight = 1,
    #     filter_seeds = True,
    #     dijkstra_threshold = 0.005,
    #     graph_context_window = 2
    #     )

    # print lexicon

    # print '\n\n\n--- END OF SCRIPT ---'

    graph ={
        'A': {
           'B':{'p_dir': 0.5, 'p_inv': 0.1}
        },
        'B': {
           'C':{'p_dir': 0.1, 'p_inv': 0.5}
        },
        'C': {
        }
    }

    lexicon = {'A':5, 'B': -2, 'C': 0.1 }
    gml = get_GML(graph, lexicon)
    print gml
    with io.open('graphs/test.gml',"w",encoding='utf8') as f:
        if not isinstance(gml, unicode):
            gml = unicode(gml,'utf8')
        f.write(gml)