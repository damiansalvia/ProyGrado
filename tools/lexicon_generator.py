# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json
import glob

from printHelper import *
from utils import *

inputdir  = 'apps/dictionaries/'
outputdir = 'apps/outputs/static_lexicons/single_corpus_lexicon/'
logdir    = 'apps/log/'

def get_tokens(review):
    return nltk.word_tokenize(review)

def add_word_to_dic(occurrences, word, rank):
    if not occurrences.get(word):
        occurrences[word] = []
    occurrences[word].append(rank)

def get_polarity(list):
    val = reduce(lambda x,y:x+y,list)/len(list)
    if val < 40:
        return '-'
    elif val > 60:
        return '+'
    else:
        return '0'

# Main
log = Log(logdir)
start_time = time.time()

files = glob.glob(inputdir + 'corpus*.json')

for file in files:
    file_name = file.split('/')[-1]
    occurrences = {}
    with codecs.open(file, "r", "utf-8") as f:
        reviews = json.load(f)
    corpus_length = len(reviews)
    for idx, rev in enumerate(reviews):
        subject  = rev['subject']
        review  = rev['review']
        rank  = rev['rank']
        [add_word_to_dic(occurrences, x.lower(), rank) for x in get_tokens(review) if is_valid_word(x)]
        progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", corpus_length, idx)
    sys.stdout.write('\n')
    sys.stdout.flush()
    polarities = {key:get_polarity(value) for key, value in occurrences.iteritems()}
    with codecs.open(outputdir +    file_name.replace('corpus', 'polarities'), "w", "utf-8") as f:
        json.dump(polarities, f, ensure_ascii=False)

sys.stdout.write('Elapsed time: %.2f Sec' % (time.time() - start_time))
sys.stdout.write('\n')
sys.stdout.flush()

