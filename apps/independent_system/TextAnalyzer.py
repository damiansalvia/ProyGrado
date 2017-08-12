 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities') # To import 'utilities' modules

import time
import freeling_analyzer
from printHelper import *
import OpinionsDatabase as db
import md5

analyzer = freeling_analyzer.Analyzer()
log = Log("./")

def analyze(reviews):

    def get_tokens(review):
        # obtain a list of words from a text
        return analyzer.analyze(review)

    # #------- Execute Function -------#
    opinions = []
    corpus_length = len(reviews)
    for idx, op in enumerate(reviews):
        progressive_bar( "analyzing", corpus_length, idx)
        try:
            op_id = md5.new(str(op['category']) + op['review']).hexdigest()
            if not db.get_opinion(op_id):
                opinion = {}         
                opinion['id_']      = op_id
                opinion['category'] = op['category']
                opinion['idx']      = op['idx']
                opinion['text']     = [{
                    'word'  : token['form'],
                    'lemma' : token['lemma'],
                    'tag'   : token['tag']
                } for token in get_tokens(op['review']) ]
                opinions.append(opinion)
        except Exception as e:
            log(str(e))
            raise e
    print '\n'
    return opinions


if __name__ == "__main__":

    start_time = time.time()

    reviews = [
        {
            'idx'     : 1,
            'category': 100 , 
            'review'  : 'Excelente .'
        },
        {
            'idx'     : 2,
            'category': 50, 
            'review'  : 'No esta mala .'
        },
        {
            'idx'     : 3,
            'category': 0, 
            'review'  : 'No me gustó .'
        }
    ]
    corpus  = "corpus_test"

    db.save_opinions(analyze(reviews),corpus )

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
