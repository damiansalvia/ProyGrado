# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
sys.path.append('../generation_system')
from utilities import *

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
import time

import CorpusReader as cr 
import DataProvider as dp
import NegationTagger as nt
import ANN_LSTM as lstm
import TextAnalyzer as ta
from TextAnalyzer import an
import LexiconGenerator as lg        
from Settings import *
from DataProvider import db

from InteractiveNegator import get_params, start_evaluator, new_model, get_window

from GraphModel import get_dependent_lexicon_by_dijkstra

log = Log("./log")

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

#################################################################

batch =  raw_input("Batch mode? [ Y / N ] > ") in ['Y','y']

config_set = config_set_parsing()
 
if not batch:
    op = raw_input("Parse a(ll) or enter for none > ")
    op = len(config_set) if op.lower() == 'a' else 0
else: 
    op = len(config_set)
 
count = 0
for config in config_set[:op]:
         
    start_time = time.time()
         
    opinions = cr.from_corpus(
            config['source'],            
            config['path_pattern'],      
            config['review_pattern'],    
            config['category_pattern'],  
            config['category_mapping'],  
            config['category_location'], 
            category_position = config['category_position'],
            category_level    = config['category_level'],
            start             = config['start'],
            decoding          = config['decoding'],
            tofile = "./outputs/tmp"
        )
       
    analyzed = ta.analyze(
            opinions,
            tofile="./outputs/tmp"
        )
            
    count += len(analyzed)
 
    elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
    log( "READING & PREPROCESSING for %s - Elapsed: %s" % (config['source'],elapsed) , level="INFO")
    print "READING & PREPROCESSING for %s - Elapsed: %s" % (config['source'],elapsed)
 
del an
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
log( "READING & PREPROCESSING  - Elapsed: %s" % elapsed , level="INFO")
print "READING & PREPROCESSING - Elapsed time: %s" % elapsed
###################################################################
 
 
if not batch:
    op = raw_input("Update negation for train? [y/n] > ")
    op = op.lower()
    if op == 'y': count += nt.load_corpus_negation()
else:
    count += nt.load_corpus_negation()
 
            
###################################################################
 
if not batch:
    if count: raw_input("Total %i. Continue..." % count)
 
###################################################################
 
start_time = time.time()
 
if not batch:
    op = raw_input("Update embeddings? [y/n] > ")
    op = op.lower()
    if op == 'y': dp.update_embeddings(verbose=True)
else:
    dp.update_embeddings(verbose=True)
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
log( "EMBEDDINGS  - Elapsed: %s" % elapsed , level="INFO")
print "EMBEDDINGS - Elapsed time: %s" % elapsed
 
###################################################################
 
if not batch:
    op = raw_input("Start manual tagging? [y/n] > ")
    op = op.lower() 
    if op == 'y': nt.start_tagging(tofile="./outputs/negation") 
 
 
###################################################################
   
config_set = config_set_neural_negation_tagger()
 
 
if not batch:
    op = raw_input("Training-predict a(ll) > ")
    op = len(config_set) if op.lower() == 'a' else 0
else: 
    op = len(config_set)
     
stats = []
 
start_time = time.time()
 
# ann = lstm.ANN(10)
# ann.set_model()
# stat = ann.fit_tagged( testing_fraction=0.20 , verbose=1 )
# stats.append(stat)
# ann.save_model("LSTM_w10_default")
# ann.predict_untagged(tofile="./outputs/tmp")
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
log( "LSTM train/test/predict - Elapsed: %s" % elapsed , level="INFO")
print "LSTM train/test/predict - Elapsed time: %s" % elapsed
  
print "Summary"
for nth,stat in enumerate(stats): print "Option",nth,stat
 
###################################################################
 
start_time = time.time()
 
title('INDEPENDENT LEXICON by SENTI-TFIDF')
result = lg.get_indepentent_lexicon_by_senti_tfidf(limit=150,tolerance=0.8,filter_neutral=True)
save(result,"indepentent_lexicon_by_senti_tfidf_seed","../lexicon/independent")
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
log( "SENTI TFIDF - Elapsed: %s" % elapsed , level="INFO")
print "SENTI TFIDF - Elapsed time: %s" % elapsed

###################################################################

title('DEPENDENT LEXICON by DIJKSTRAGRAPH')
seeds_path = '../lexicon/independent/indepentent_lexicon_by_senti_tfidf_seed.json'
val_key = 'rank'

for source in dp.get_sources(): 
    start_time = time.time()
    
    reviews = db.reviews.find({"source":source})
    
    seeds = { lem:pol[val_key] for lem,pol in json.load( open(seeds_path) ).items() }

    lexicon = get_dependent_lexicon_by_dijkstra(source, reviews, seeds,
        prefix_tag_list  = PREFIX_TAGS, 
        filter_neutral = True, 
        limit = 300, 
        neutral_resistance = 0.3,
        max_weight = 1,
        filter_seeds = True,
        dijkstra_threshold = 0.005,
        graph_context_window = 2
    )
    save(lexicon,"dependent_lexicon_by_dijkstra_%s" % source,"../lexicon/dependent")

    elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
    log( "DIJKSTRA for %s - Elapsed: %s" % (source,elapsed) , level="INFO")
    print "DIJKSTRA for %s - Elapsed time: %s" % (source, elapsed)

 


    