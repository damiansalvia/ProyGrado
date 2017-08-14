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
    ids = []
    corpus_length = len(reviews)
    for idx, op in enumerate(reviews):
        progressive_bar("Analyzing %s " % op['source'], corpus_length, idx)
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
    progressive_bar("Analyzing %s " % op['source'], corpus_length, idx+1)
    print '\n'
    return opinions


def addManualTagged(opinions):
    return 


if __name__ == "__main__":

    start_time = time.time()

    reviews = [
        {
            'idx'     : 1,
            'category': 100 , 
            'review'  : u'Excelente .'
        },
        {
            'idx'     : 2,
            'category': 50, 
            'review'  : u'No esta mala .'
        },
        {
            'idx'     : 3,
            'category': 0, 
            'review'  : u'No me gustó .'
        }
    ]
    corpus  = "corpus_test"

    db.save_opinions(analyze(reviews),corpus )


    # opinions [{
    #     "from": "corpus_apps_android", 
    #     "id": 687, 
    #     "annotation": "sin/i español/i español/n es/n uno/n de/n los/n idiomas/n más/n hablados/n en/n el/n mundo/n ,/i gogle/i ./n a/i ver/i si/i mejoramos/i un/i poco/i en/i ese/i aspecto/i ./n ./n ./n y/n el/n mundo/n no/i es/i solo/i usa/i ./n igual/i ,/i como/i si/i fueran/i a/i leer/i esto/i ./n ./n ./n ./n"
    # }, 
    # {
    #     "from": "corpus_apps_android", 
    #     "id": 7264, 
    #     "annotation": "me/n es/n de/n mucha/n utilidad/n buena/n ap/n en/n horabuena/n ./n"
    # }, 
    # {
    #     "from": "corpus_apps_android", 
    #     "id": 8160, 
    #     "annotation": "barato/n y/n fjncional/n no/n puedo/n opinar/n mucho/n del/n poco/n tiempo/n que/n lo/n tengo/n ,/i pero/i por/i 2/i 5/i cent/i que/i más/i se/i puede/i pedir/i ./n viva/n las/n promociones/n y/n el/n saldo/n de/n 2/n 0/n de/n gogle/n play/n ./n"
    # }]

    # print addManualTagged(opinions)


    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
