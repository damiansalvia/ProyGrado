# -*- encoding: utf-8 -*-
'''
Example for generating independent and dependent lexicon from a given corpus by UI
@author: Nicolás Mechulam, Damián Salvia
'''
import sys
sys.path.append('../src')

import os
clean = 'cls' if os.name == 'nt' else 'clear'

import glob

import cldas.db.crud as dp

from cldas.indeplex import *
from cldas.deplex import *
from cldas.utils import load, title, USEFUL_TAGS, save_sub_graph


def display_options(name, options, files=[]):
    
    title(name,30)
    
    for i in range( len(options) ):
        print i,".",options[i] if not callable( options[i] ) else options[i].__name__.replace('_',' ')
        
    for j in range( len(files) ):
        print j+i+1,".",files[j]
        
    op = ''
    while not op.isdigit() or int(op) >= len(options) + len(files):
        op = raw_input('> ')
    op = int(op)
    
    return op


'''
---------------------------------------------
      Dataset retrieval (db or custom)
---------------------------------------------
'''
pos = dp.get_opinions( cat_cond={"$gt":50} )
neg = dp.get_opinions( cat_cond={"$lt":50} )
lemmas = dp.get_lemmas()



while True:
    '''
    ---------------------------------------------
          Independent Lexicon generation
    ---------------------------------------------
    '''
    os.system(clean)
    
    indeplex = [ by_senti_tfidf, by_senti_qtf, by_senti_avg, by_senti_pmi ]
    files = [ file for file in glob.glob("./indeplex/*") if file.endswith('json') ]
    i = display_options( "Independent Lexicon", indeplex, files)
    
    limit = len(indeplex)
    if i > limit-1:
        li = load( files[i-limit] )
        seed_name = files[i-limit].split('/')[-1].split('_')[3]
    else:
        li = indeplex[i]( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150, tofile='./indeplex' )
        seed_name = indeplex[i].__name__
    
    
    '''
    ---------------------------------------------
          Dependent Lexicon generation
    ---------------------------------------------
    '''
    os.system(clean)
    
    corporea = dp.get_sources()
    j = display_options("Sources",corporea)
    corpus   = corporea[j]
    opinions = dp.get_opinions( source=corpus )
    graph = ContextGraph( opinions, corpus, filter_tags=USEFUL_TAGS )
    
    
    os.system(clean)
    
    deplex = [ by_distance, by_influence ]
    k = display_options("Dependent Lexicon",deplex)
    ld = deplex[k]( graph, li, seed_name=seed_name, limit=300, tofile='./deplex', wc_neu=0.2)
    
    
    save_sub_graph(graph, ld, name=deplex[k].__name__,path='./graphs')
    

    if raw_input("Exit? [y/n] > ") == 'y': break
    