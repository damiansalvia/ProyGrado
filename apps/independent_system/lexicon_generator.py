# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json
import glob
from collections import defaultdict
from printHelper import *
from utils import *


inputdir  = 'outputs/corpus/'
outputdir = 'outputs/lexicons/single_corpus_lexicon/'
logdir    = '../log/'

def get_tokens(review):
    return nltk.word_tokenize(review)

def add_word_to_dic(occurrences, word, rank):
    if not occurrences.get(word):
        occurrences[word] = []
    occurrences[word].append(rank)

def get_polarity(list):
    val = sum(list)/len(list)
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
    occurrences = defaultdict(list)
    with codecs.open(file, "r", "utf-8") as f:
        reviews = json.load(f)
    corpus_length = len(reviews)
    for idx, rev in enumerate(reviews):
        progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", corpus_length, idx)
        try:
            review  = rev['review']
            rank  = rev['rank']
            for token in get_tokens(review):
                occurrences[token.lower()].append(rank) 
        except Exception as e:
            log(str(e))
            raise e
    progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", corpus_length, idx+1)
    print
    polarities = {key:get_polarity(value) for key, value in occurrences.iteritems()}
    with codecs.open(outputdir +    file_name.replace('corpus', 'polarities'), "w", "utf-8") as f:
        json.dump(polarities, f,indent=4,sort_keys=True,ensure_ascii=False)

print '\nElapsed time: %.2f Sec' % (time.time() - start_time)

