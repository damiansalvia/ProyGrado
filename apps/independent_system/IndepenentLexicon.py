# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
from utilities import *

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

import CorpusReader as cr 
import DataProvider as dp
import NegationTagger as nt
import TextAnalyzer as ta
import LexiconGenerator as lg        
from Settings import *

#################################################################

config_set = config_set_parsing()

op = raw_input("Parse a(ll) or enter for none > ")
op = len(config_set) if op.lower() == 'a' else 0

count = 0
for config in config_set[:op]:
        
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

###################################################################

op = raw_input("Update negation for train? [y/n] > ")
op = op.lower()
if op == 'y': count += nt.load_corpus_negation()
           
###################################################################

if count: raw_input("Total %i. Continue..." % count)

###################################################################

op = raw_input("Update embeddings? [y/n] > ")
op = op.lower()
if op == 'y': dp.update_embeddings(verbose=True)

###################################################################

op = raw_input("Start manual tagging? [y/n] > ")
op = op.lower() 
if op == 'y': nt.start_tagging(tofile="./outputs/negation") 

###################################################################
  
config_set = config_set_neural_negation_tagger()

op = raw_input("Training-predict a(ll) > ")
op = len(config_set) if op.lower() == 'a' else 0

stats = []
for config in config_set[:op]:
    ann = nt.NeuralNegationTagger( config['wleft'], config['wright'] )    
    ann.set_model(
        out_dims      = config['out_dims'],
        activation    = config['activation'], 
        loss          = config['loss'],
        optimizer     = config['optimizer'],  
        drop_rate     = config['drop_rate'] 
    ) 
#     ann.load_model( './outputs/models/algo.h5' ) # A modo de ejemplo
    # TO-DO Decidir que hacer con los negadores (null, true o false)
    stat = ann.fit_tagged( neg_as=False , testing_fraction=0.20 , verbose=1, early_monitor = config['early_monitor'] )
    ann.save_model( "predict_l%i_r%i_%s_%s_o%s_e%s_d%s" % (
            config['wleft'],
            config['wright'],
            ''.join('d'+str(dim) for dim in config['out_dims']),
            ''.join(act[0].upper() for act in config['activation']),
            config['optimizer'][0].upper(),
            "Y" if config['early_monitor'] else "N",
            "Y" if config['drop_rate'] else "N"
        ) 
    )
#     ann.input_guess() # Interactive
    stats.append(stat)
    ann.predict_untagged( limit = 10, tofile="./outputs/tmp" )
 
print "Summary"
for nth,stat in enumerate(stats): print "Option",nth,stat

###################################################################

tolerance = 0.8
limit = 150

title('SENTI-TFIDF')
result = lg.get_indepentent_lexicon_by_senti_tfidf(limit=limit)
save(result,"LI_BySentiTFIDF","./outputs/lexicon")
 
title('AVERAGE')
result = lg.get_indepentent_lexicon_by_average(limit=limit, tolerance=tolerance)
save(result,"LI_ByAverage_at_%i" % (tolerance*100),"./outputs/lexicon")
 
title('WEIGHT FUNCTION')
result = lg.get_indepentent_lexicon_by_weight_function(limit=limit, tolerance=tolerance)
save(result,"LI_ByWeightedFunction_at_%i" % (tolerance*100),"./outputs/lexicon")
 
title('MATRICES')
result = lg.get_indepentent_lexicon_by_polarity_matrices(limit=limit, tolerance=tolerance)
save(result,"LI_ByMatrix_at_%i" % (tolerance*100),"./outputs/lexicon")
 



 


    