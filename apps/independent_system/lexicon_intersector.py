# -*- coding: utf-8 -*-

import time
import codecs
import json
import glob
from collections import defaultdict
from printHelper import *
from utils import *

inputdir  = 'outputs/lexicons/single_corpus_lexicon/'
outputdir = 'outputs/lexicons/'
logdir    = '../log/'

MIN_MATCHES = 5

def all_equal(list):
    return all(map(lambda x: x == list[0], list))

# Main
files = glob.glob(inputdir + 'polarities*.json')
log = Log(logdir)
start_time = time.time()
polarities = defaultdict(list)
for file in files:
    try:
        file_name = file.split('/')[-1]
        with codecs.open(file, "r", "utf-8") as f:
            corpus_polarities = json.load(f)
        words_count = len(corpus_polarities)
        for idx, (word,polarity) in enumerate(corpus_polarities.iteritems()):
            progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx)
            polarities[word].append(polarity)
    except Exception as e:
        log(str(e))
        raise e
    progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx+1)
    print 
    
polarities = {word:polarities[word][0] for word in polarities if  len(polarities[word]) >= MIN_MATCHES and all_equal(polarities[word])} 

with codecs.open(outputdir + 'static_polarities.json' , "w", "utf-8") as f:
    json.dump(polarities, f, indent=4, ensure_ascii=False)

print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
