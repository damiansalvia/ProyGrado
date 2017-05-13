# -*- coding: utf-8 -*-

import time
import codecs
import json
import glob

from printHelper import *
from utils import *

inputdir  = 'apps/outputs/static_lexicons/single_corpus_lexicon/'
outputdir = 'apps/outputs/static_lexicons/'
logdir    = 'apps/log/'

MIN_MATCHES = 1

def add_word_to_dic(dic, word, pol):
    if not dic.get(word):
        dic[word] = []
    dic[word].append(pol)

def all_equal(list):
    return all(map(lambda x: x == list[0], list))

# Main
files = glob.glob(inputdir + 'polarities*.json')
log = Log(logdir)
start_time = time.time()
polarities = {}

for file in files:
    file_name = file.split('/')[-1]
    with codecs.open(file, "r", "utf-8") as f:
        words = json.load(f)
    words_count = len(words)
    for idx, word in enumerate(words):
        add_word_to_dic(polarities, word , words[word])
        progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx)
    sys.stdout.write('\n')
    sys.stdout.flush()

polarities = {x:polarities[x][0] for x in polarities if  len(polarities[x]) > MIN_MATCHES and all_equal(polarities[x])} 

with codecs.open(outputdir + 'static_polarities.json' , "w", "utf-8") as f:
    json.dump(polarities, f, ensure_ascii=False)

sys.stdout.write('Elapsed time: %.2f Sec' % (time.time() - start_time))
sys.stdout.write('\n')
sys.stdout.flush()
