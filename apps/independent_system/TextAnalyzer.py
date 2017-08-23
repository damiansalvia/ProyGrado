 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

import time
from analyzer import Analyzer
from utilities import *
import OpinionsDatabase as db
import md5, re

print "Initializing FreeLing analyzer"
an = Analyzer()
log = Log("./log")

def analyze(opinions):

    # #------- Execute Function -------#
    analyzed = []
    _ids = []
    total = len(opinions)
    fails = 0
    for idx, opinion in enumerate(opinions):
        progress("Analyzing %s (%05.2f%%)" %  ( opinion['source'], 100.0*fails/total ), total, idx )
        try:
            
            _id = md5.new(str(opinion['category']) + opinion['text'].encode('ascii', 'ignore')).hexdigest()
            
            if not db.get_opinion(_id) and _id not in _ids:
                
                _ids.append(_id)
                tokens = an.analyze(opinion['text'])
                
                if not tokens:
                    raise Exception("Empty analysis")
                
                analysis = {}         
                analysis['_id']      = _id
                analysis['category'] = opinion['category']
                analysis['idx']      = opinion['idx']
                analysis['source']   = opinion['source']
                analysis['text']     = [{
                    'word'  : token['form'],
                    'lemma' : token['lemma'],
                    'tag'   : token['tag']
                } for token in tokens ]
                    
                analyzed.append(analysis)
                
        except Exception as e:
            fails += 1
            log("Reason : %s for '%s' (at %s)" % (str(e),opinion['text'].encode('ascii','ignore'),opinion['source']) )
        
    db.save_opinions(analyzed)


if __name__ == '__main__':
    opinions = [
        {
            'source' : 'corpus_test',
            'text' : u'Mola mundo .',
            'category': 100,
            'idx' : 1
        },
        {
            'source' : 'corpus_test',
            'text' : u'. Hola mundo .',
            'category': 50,
            'idx' : 2
        },
        {
            'category': 1000, 
            'source': 'corpus_test', 
            'idx': 76, 
            'text': u'Hola mundo ! .'
        },
        {
            'category': 1000, 
            'source': 'corpus_test', 
            'idx': 76, 
            'text': u'Hola ( mundo !' # Este caso da error para FreeLing
        }
    ]

    analyze(opinions) 