 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

import time
from analyzer import Analyzer
from utilities import *
import DataProvider as dp
import md5, re


print "Initializing FreeLing analyzer"
an = Analyzer()
log = Log("./log")


def analyze(opinions,tofile=None):

    # #------- Execute Function -------#
    analyzed = []
    _ids = []
    total = len(opinions)
    fails = 0 
    for idx, opinion in enumerate(opinions):
        progress("Analyzing %s (%05.2f%%)" %  ( opinion['source'], 100.0*fails/total ), total, idx )
        try:
                
            _id = md5.new(str(opinion['category']) + opinion['text'].encode('ascii', 'ignore')).hexdigest()
            
            if not dp.get_opinion(_id) and _id not in _ids:
                
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
                
                if idx % 500 == 0: # partial dump
                    dp.save_opinions(analyzed)
                    analyzed = []
                    
        except Exception as e:
            fails += 1
            log("Reason : %s for '%s' (at %s)" % (str(e),opinion['text'].encode('ascii','ignore'),opinion['source']) )
        except KeyboardInterrupt:
            fails += 1
            log("Reason : Interrupted on '%s' (at %s)" % (opinion['text'].encode('ascii','ignore'),opinion['source']) )
        
    dp.save_opinions(analyzed)
    if tofile: save(analyzed,"analyzed_%s" % opinions[0]['source'],tofile)
    
    return analyzed


if __name__ == '__main__':
    opinions = [
        {
            "category": 90, 
            "source": "test", 
            "idx": 1, 
            "text": "La pelicula es muy divertida , es genial ."
        }, 
        {
            "category": 80, 
            "source": "test", 
            "idx": 2, 
            "text": "Me parece encantadora la pelicula , la recomiendo , genial ."
        }
    ]

    print analyze(opinions) 