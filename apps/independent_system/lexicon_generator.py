# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json
import glob
from collections import defaultdict
from printHelper import *

inputdir    = 'outputs/corpus/'
outputdir   = 'outputs/lexicons/single_corpus_lexicon/'
negatorsdir = 'negators_list.txt'
logdir      = '../log/'

log = Log(logdir)

MAX_RANK = 100

WINDOW_LEFT   = 0
WINDOW_RIGHT = 0

class IndependentLexiconGenerator:
    

    def __init__(self, input_dir = inputdir, negators_dir = negatorsdir, window_left = WINDOW_LEFT, window_right = WINDOW_RIGHT, max_rank = MAX_RANK):
        self.files        = glob.glob(input_dir + 'corpus*.json')
        self.polarities   = {}
        self.window_right  = window_right
        self.window_size  = window_left + window_right
        self.max_rank     = max_rank
        with codecs.open(negators_dir, "r", "utf-8") as f:
            self.negators =  [x.strip() for x in f.readlines()]  
    
    def generate(self):

        def get_tokens(review):
            # obtain a list of words from a text
            return nltk.word_tokenize(review)

        def get_polarity(list):
            val = sum(list)/len(list)
            if val < 40:
                return '-'
            elif val > 60:
                return '+'
            else:
                return '0'

        def get_negation_indexes(word_list):
            # returns the indexes of the negators words in a secuence
            return [ idx for idx, word in enumerate(word_list) if word in self.negators ]
            
        def is_negated(idx, negations_indexes):
            # chek if a word is affected by any existent negators
            return any( i >= 0 and i <= self.window_size for i in [ idx - neg + self.window_right for neg in negations_indexes])

        def inverse(rank):
            # invert the rank
            return self.max_rank - rank

        # #------- Execute Function -------#
        for file in self.files:
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
                    tokens = get_tokens(review)
                    negations_indexes = get_negation_indexes(tokens)
                    for tx_idx,token in enumerate(tokens):
                        if not tx_idx in negations_indexes:
                            # The negators shouldn't have polarities by themselves (this should be discussed)
                            if is_negated(tx_idx,negations_indexes):
                                occurrences[token.lower()].append(inverse(rank)) 
                            else: 
                                occurrences[token.lower()].append(rank) 
                except Exception as e:
                    log(str(e))
                    raise e
            progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", corpus_length, idx + 1)
            print
        self.polarities[file_name] = {key:get_polarity(value) for key, value in occurrences.iteritems()}

    def get_polarities(self):
        return self.polarities

    def save(self, output_dir = outputdir):
        for (file_name, pol) in self.polarities.iteritems():
            with codecs.open(output_dir + file_name.replace('corpus', 'polarities'), "w", "utf-8") as f:
                json.dump(pol, f,indent=4,sort_keys=True,ensure_ascii=False)


if __name__ == "__main__":

    start_time = time.time()

    generator = IndependentLexiconGenerator()
    generator.generate()
    # generator.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
