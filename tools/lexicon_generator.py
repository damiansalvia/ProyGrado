# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json

from printHelper import *
from utils import *

inputdir  = 'apps/dictionaries/'
outputdir = 'apps/outputs/'
logdir    = 'apps/log/'

max_acceptable_length  = 300000

def is_length_acceptable(text):
    try:
        if len(nltk.word_tokenize(text)) < max_acceptable_length:
            return True
        return False
    except Exception as e:
        log(str(e))
        return False


def get_tokens(review):
    return nltk.word_tokenize(review)

# Main

log = Log(logdir)
start_time = time.time()

occurrences = []

with codecs.open(inputdir + "reviews.json", "r", "utf-8") as f:
    reviews = json.load(f)

corpus_length = len(reviews)

for idx, rev in enumerate(reviews):
    subject  = rev['subject']
    review  = rev['review']
    rank  = rev['rank']

    if is_length_acceptable(review):
        [occurrences.append((x.lower(), rank)) for x in get_tokens(review) if is_valid_word(x)]

    progressive_bar("Reading reviews:    ", corpus_length, idx)

sys.stdout.write('\n')
sys.stdout.flush()


print occurrences
# with codecs.open(outputdir + "absolute_polarities.json", "w", "utf-8") as f:
#     json.dump(polarities, f, ensure_ascii=False)

sys.stdout.write('Elapsed time: %.2f Sec' % (time.time() - start_time))
sys.stdout.write('\n')
sys.stdout.flush()
