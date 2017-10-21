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
from cldas.utils import load, title, USEFUL_TAGS


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

wdcloud = raw_input("Generate word cloud? [y/n] > ") == 'y'

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
    
    options = [ by_senti_tfidf, by_senti_qtf, by_senti_avg, by_senti_pmi ]
    files = [ file for file in glob.glob("./indeplex/*") if file.endswith('json')]
    i = display_options( "Independent Lexicon", options, files)
    
    limit = len(options)
    if i > limit:
        li = load( files[i-limit] )
    else:
        li = options[i]( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150, tofile='./indeplex', wdcloud=wdcloud )
    
    
    '''
    ---------------------------------------------
          Dependent Lexicon generation
    ---------------------------------------------
    '''
    os.system(clean)
    
    corporea = dp.get_sources()
    i = display_options("Sources",corporea)
    corpus   = corporea[i]
    opinions = dp.get_opinions( source=corpus )
    graph = MultiGraph( opinions, corpus, filter_tags=USEFUL_TAGS )
    
    
    os.system(clean)
    
    options = [ by_bfs, by_influence ]
    i = display_options("Dependent Lexicon",options)
    ld = options[i]( graph, li, neu_treshold=0.2, limit=300, tofile='./deplex', wdcloud=wdcloud )

    if raw_input("Exit? [y/n] > ") == 'y': break


