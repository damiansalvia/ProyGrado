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
import ANN_LSTM as nt
import TextAnalyzer as ta
from TextAnalyzer import an
import LexiconGenerator as lg        
from Settings import *

from InteractiveNegator import get_params, start_evaluator, new_model, get_window

from GraphModel import get_dependent_lexicon_by_dijkstra

log = Log("./log")

#################################################################

config_set = config_set_parsing()

batch =  raw_input("Batch mode? [ Y / N ] > ") in ['Y','y']

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

ann = nt.ANN(10)
ann.set_model()
stat = ann.fit_tagged( testing_fraction=0.20 , verbose=1 )
stats.append(stat)
ann.save_model("LSTM_w10_default")
ann.predict_untagged(tofile="./outputs/tmp")

elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
log( "LSTM train/test/predict - Elapsed: %s" % elapsed , level="INFO")
print "LSTM train/test/predict - Elapsed time: %s" % elapsed
    
# for config in config_set[:op]:        
#     ann = nt.NeuralNegationTagger( config['wleft'], config['wright'] )    
#     ann.set_model(
#         out_dims      = config['out_dims'],
#         activation    = config['activation'], 
#         loss          = config['loss'],
#         optimizer     = config['optimizer'],  
#         drop_rate     = config['drop_rate'] 
#     ) 
# #     ann.load_model( './outputs/models/algo.h5' ) # A modo de ejemplo
#     # TO-DO Decidir que hacer con los negadores (null, true o false)
#     stat = ann.fit_tagged( neg_as=False , testing_fraction=0.20 , verbose=1, early_monitor = config['early_monitor'] )
#     ann.save_model( "predict_l%i_r%i_%s_%s_o%s_e%s_d%s" % (
#             config['wleft'],
#             config['wright'],
#             ''.join('d'+str(dim) for dim in config['out_dims']),
#             ''.join(act[0].upper() for act in config['activation']),
#             config['optimizer'][0].upper(),
#             "Y" if config['early_monitor'] else "N",
#             "Y" if config['drop_rate'] else "N"
#         ) 
#     )
# #     ann.input_guess() # Interactive
#     stats.append(stat)
#     ann.predict_untagged( limit = 10, tofile="./outputs/tmp" )
 
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

# tolerance = 0.8
# limit = 300
# filter_neutral = True
#  
# suffix  = "_top%i" % limit if limit else "_all"
# suffix += "_%ip" % (tolerance*100)
# suffix += "_neu" if not filter_neutral else ""
#
# title('SENTI-TFIDF')
# start_time = time.time()
# result = lg.get_indepentent_lexicon_by_senti_tfidf(limit=limit,tolerance=tolerance,filter_neutral=filter_neutral)
# save(result,"indepentent_lexicon_by_senti_tfidf"+suffix,"../lexicon/independent")
# print "Elapsed time:",time.time()-start_time,'s'
#  
# title('AVERAGE')
# start_time = time.time()
# result = lg.get_indepentent_lexicon_by_average(limit=limit, tolerance=tolerance)
# save(result,"indepentent_lexicon_by_average"+suffix,"../lexicon/independent")
# print "Elapsed time:",time.time()-start_time,'s'
#  
# title('WEIGHT FUNCTION')
# start = gmtime()
# result = lg.get_indepentent_lexicon_by_weight_function(limit=limit, tolerance=tolerance)
# save(result,"indepentent_lexicon_by_weight_function"+suffix,"../lexicon/independent")
# print "Elapsed time:",time.time()-start_time,'s'
#
# title('MATRICES')
# start_time = time.time()
# result = lg.get_indepentent_lexicon_by_polarity_matrices(limit=limit, tolerance=tolerance)
# save(result,"lexicon_by_polarity_matrices"+suffix,"../lexicon/independent")
# print "Elapsed time:",time.time()-start_time,'s'

title('DEPENDENT LEXICON by DIJKSTRAGRAPH')
for source in dp.get_sources(): 
    start_time = time.time()

    get_dependent_lexicon_by_dijkstra(
        source=source,
        seeds_path='../lexicon/independent/indepentent_lexicon_by_senti_tfidf_seed.json',
        val_key='rank',
        limit = 400
    )

    elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
    log( "DIJKSTRA for %s - Elapsed: %s" % (source,elapsed) , level="INFO")
    print "DIJKSTRA for %s - Elapsed time: %s" % (source, elapsed)

 


    