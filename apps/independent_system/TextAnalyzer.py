 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

import time
import analyzer
from utilities import *
import OpinionsDatabase as db
import md5
import re

analyzer = analyzer.Analyzer()
log = Log("./log")

def analyze(reviews):

    def get_tokens(review):
        # obtain a list of words from a text
        return analyzer.analyze(review)

    # #------- Execute Function -------#
    opinions = []
    ids = []
    corpus_length = len(reviews)
    for idx, op in enumerate(reviews):
        progress("Analyzing %s " % op['source'], corpus_length, idx)
        try:
            op_id = md5.new(str(op['category']) + op['review'].encode('ascii', 'ignore')).hexdigest()
            if not db.get_opinion(op_id) and op_id not in ids:
                ids.append(op_id)
                opinion = {}         
                opinion['_id']      = op_id
                opinion['category'] = op['category']
                opinion['idx']      = op['idx']
                opinion['source']   = op['source']
                opinion['text']     = [{
                    'word'  : token['form'],
                    'lemma' : token['lemma'],
                    'tag'   : token['tag']
                } for token in get_tokens(op['review']) ]
                opinions.append(opinion)
        except Exception as e:
            log(str(e))
            raise e
    print 
    return opinions


if __name__ == '__main__':
    reviews = [
        {
            'source' : u'corpus_test',
            'review' : u'Excelente .',
            'category': 100,
            'idx' : 1
        },{
            'source' : u'corpus_test',
            'review' : u'No la volveria a ver, pero es buena .',
            'category': 50,
            'idx' : 2
        },{
            'source' : u'corpus_test',
            'review' : u'No me gustó .',
            'category': 0,
            'idx' : 3
        },

    ]

    db.save_opinions(analyze(reviews)) 


    