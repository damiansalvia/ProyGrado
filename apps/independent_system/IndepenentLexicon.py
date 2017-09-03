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
           
if op: raw_input("Total %i. Continue..." % count)

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

op = raw_input("Traing-predict a(ll) or enter for none > ")
op = len(config_set) if op.lower() == 'a' else 0

stats = []
for config in config_set[:op]:
    ann = nt.NeuralNegationTagger( 
        config['wleft'], 
        config['wright'],
        out_dims      = config['out_dims'],
        activation    = config['activation'], 
        loss          = config['loss'],
        optimizer     = config['optimizer'], 
        early_monitor = config['early_monitor'], 
        drop_rate     = config['drop_rate'] 
    )     
    stat = ann.fit_tagged( testing_fraction=0.20 , verbose=1 )
    stats.append(stat)
    ann.predict_untagged( limit = 10, tofile="./outputs/tmp" )

print "Summary"
for nth,stat in enumerate(stats): print "Option",nt,stat

###################################################################

# tolerance = 1.0
# li = dp.get_indepentent_lex(tolerance=tolerance)
# save(li,"independent_lexcon_-_tolerance_%i_percent" % (tolerance*100),"./outputs/lexicon")
# li = dp.get_indepentent_lex2(tolerance=tolerance)
# save(li,"independent_lexcon_2_-_tolerance_%i_percent" % (tolerance*100),"./outputs/lexicon")
 



 


    