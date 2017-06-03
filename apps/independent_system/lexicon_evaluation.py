# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities') # To import 'utilities' modules

from _collections import defaultdict

import pandas as pd
import numpy as np

from printHelper import *

from corpus_parser import CorpusParser
from lexicon_generator import IndependentLexiconGenerator
from lexicon_intersector import IndependentLexiconIntersector

corpus_sources = [
    #"../../corpus/corpus_cine",
    #"../../corpus/corpus_tweets",
    #"../../corpus/corpus_hoteles",
    #"../../corpus/corpus_prensa_uy",
    "../../corpus/corpus_apps_android",
    #"../../corpus/corpus_variado_sfu"
]

negators_list = [
    u"aunque", u"denegar", u"jamás", u"nada", u"nadie", u"negar", 
    u"negativa", u"ni", u"ninguna", u"ninguno", u"ningún", 
    u"no", u"nunca", u"pero", u"rehúso", u"tampoco"
]

def splitter(sources):
    res_train, res_test = defaultdict(dict), defaultdict(dict)
    for source in sources:
        # Parse corpus
        parser = CorpusParser(input_dir=source,ldir="./log/")
        parser.parse()
        # Get and transform to DataFrame
        reviews = parser.get_parsed()
        reviews = pd.DataFrame(reviews)
        # Split train/test
        np.random.seed(42)
        msk = np.random.rand(len(reviews)) < 0.8
        train, test = reviews[msk], reviews[~msk]
        # Retransform to dict
        train, test = train.T.to_dict().values(), test.T.to_dict().values() 
        # Add to result
        res_train[source] = train
        res_test[source]  = test
    return res_train, res_test

def lexicon(corpus,wleft=3,wright=1,negators=[],output_dir=None):
    generator = IndependentLexiconGenerator(
                    from_reviews  = corpus, 
                    negators_list = negators,
                    window_left   = wleft, 
                    window_right  = wright,
                    ldir='./log/'
                )
    generator.generate()
    polarities  = generator.get_polarities()
    intersector = IndependentLexiconIntersector(
                        from_reviews = polarities,
                        tolerance = .80
                    )
    intersector.intersect_corpus()
    lexicon = intersector.get_lexicon()
    if output_dir:
        intersector.save(output_dir=output_dir)
    return lexicon

def clean(corpus):
    ret = defaultdict(list)
    for source,content in corpus.iteritems():
        for item in content:
            ret[source].append(item['review'])
    return ret

def get_indexes(tokens,lex):
    # returns the indexes of the negators words in a secuence
    return [ idx for idx, word in enumerate(tokens) if word in lex.keys() ]
     
def classify(corpus,li,threshold=10):
    for source,content in corpus.iteritems():
        total = len(content)
        ok = 0
        for idx,item in enumerate(content):
            progressive_bar("Classifying", total, idx+1)
            review = item['review']
            # Tokenize and normalize
            tokens = review.split(' ') # TODO - Usar freeling
            # Get negated idexes
            polarities = [] # list of -1,0,1
            for i in get_indexes(tokens, li):
                token   = tokens[i] 
                category = li[token] 
                if category == '-':
                    polarities.append(0)
                elif category == '0':
                    polarities.append(50)
                elif category == '+':
                    polarities.append(100)
            ctr = sum(polarities)
            qty = len(polarities)
            pred_rank = 0 if qty==0 else ctr/qty# TODO - Extraño
            real_rank = item['rank']
#             if real_rank != 0:
#                 print "Pred:",pred_rank,",","Real:",real_rank; raw_input()
            ok += pred_rank <= real_rank + threshold and pred_rank >= real_rank - threshold
        print "%i/%i predicted OK for %s" % (ok,total,source)
            
if __name__ == '__main__':
    test,train = splitter(corpus_sources)
    li = lexicon(train,negators=negators_list)
#     test = clean(test)
#     print test['../../corpus/corpus_apps_android'][0]
    classify(test,li['words'],threshold=10)
    