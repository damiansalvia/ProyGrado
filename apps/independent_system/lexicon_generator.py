# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities') # To import 'utilities' modules

import time
import os
import nltk
import codecs
import json
import glob
from collections import defaultdict
from printHelper import *

inputdir    = 'outputs/corpus/'
outputdir   = 'outputs/lexicons/single_corpus_lexicon/'

MAX_RANK = 100

WINDOW_LEFT  = 2
WINDOW_RIGHT = 1

negators_list = [
    u"aunque", u"denegar", u"jamás", u"nada", u"nadie", u"negar", 
    u"negativa", u"ni", u"ninguna", u"ninguno", u"ningún", 
    u"no", u"nunca", u"pero", u"rehúso", u"tampoco"
]

class IndependentLexiconGenerator:

    def __init__(self, from_reviews=None, input_dir=inputdir, negators_list=negators_list, 
                 window_left=WINDOW_LEFT, window_right=WINDOW_RIGHT, max_rank=MAX_RANK,
                 ldir='./'): 
        # reviews[from][text|rank]
        if not os.path.isdir(ldir): os.makedirs(ldir)
        self.log = Log(ldir)
        if from_reviews:
            self.reviews = from_reviews
        elif input_dir:
            self.reviews = defaultdict(list)
            input_dir = input_dir.replace("\\","/")
            input_dir = input_dir if input_dir[-1] != "/" else input_dir[:-1]
            for file in glob.glob(input_dir + '/corpus*.json'):
                file_name = file.replace("\\","/").split('/')[-1]
                with codecs.open(file, "r", "utf-8") as f:
                    self.reviews[file_name] = json.load(f)
        else:
            raise "No review source found"
        self.polarities   = {}
        self.window_right = window_right
        self.window_size  = window_left + window_right
        self.max_rank     = max_rank
        self.negators     = [negator.encode('utf8') for negator in negators_list]   
    
    def generate(self):

        def get_tokens(review):
            # obtain a list of words from a text
            return nltk.word_tokenize(review)

        def get_polarity(val):
            if val < 40:
                return '-'
            elif val > 60:
                return '+'
            else:
                return '0'

        def get_list_polarity(list):
            val = sum(list)/len(list)
            return get_polarity(val)

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
        for _from,content in self.reviews.iteritems():
            file_statistics = defaultdict(int)
            occurrences = defaultdict(list)
            negated_count = defaultdict(int)
            corpus_length = len(content)
            for idx, rev in enumerate(content):
                progressive_bar( "Generating from %s: " % _from, corpus_length, idx)
                try:
                    review  = rev['review']
                    rank    = rev['rank']
                    tokens  = get_tokens(review)
                    file_statistics['rev_' + get_polarity(rank)] += 1
                    negations_indexes = get_negation_indexes(tokens)
                    file_statistics['negators'] += len(negations_indexes)
                    for tx_idx,token in enumerate(tokens):
                        if not tx_idx in negations_indexes:
                            token = token.lower()
                            # The negators shouldn't have polarities by themselves (this should be discussed)
                            if is_negated(tx_idx,negations_indexes):
                                occurrences[token].append(inverse(rank)) 
                                file_statistics['neg_word'] += 1
                                negated_count[token] += 1
                            else: 
                                occurrences[token].append(rank) 
                except Exception as e:
                    self.log(str(e))
                    raise e
            progressive_bar( "Generating from %s: " % _from, corpus_length, idx + 1)
            print
                
            file_name = _from
            self.polarities[file_name] = {}         
            file_polarities = { 
                word: {
                    'polarity'             : get_list_polarity(rank),
                    'positives_ocurrences' : len(filter(lambda val: get_polarity(val) == "+", rank)),
                    'negatives_ocurrences' : len(filter(lambda val: get_polarity(val) == "-", rank)),
                    'neutral_ocurrences'   : len(filter(lambda val: get_polarity(val) == "0", rank)),
                    'total_ocurrences'     : len(rank),
                    'negated_ocurrences'   : negated_count[word]
                } for word, rank in occurrences.iteritems() 
            }
            self.polarities[file_name]['words'] = file_polarities
            self.polarities[file_name]['analytics'] = {
                "positive_reviews"     : file_statistics['rev_+'],
                "negative_reviews"     : file_statistics['rev_-'],
                "neutral_reviews"      : file_statistics['rev_0'],
                "total_reviews"        : file_statistics['rev_+'] + file_statistics['rev_-'] + file_statistics['rev_0'],
                "positive_words"       : len(filter(lambda word: file_polarities[word]['polarity'] == "+", file_polarities.keys())),
                "negative_words"       : len(filter(lambda word: file_polarities[word]['polarity'] == "-", file_polarities.keys())),
                "neutral_words"        : len(filter(lambda word: file_polarities[word]['polarity'] == "0", file_polarities.keys())),
                "vocabulaty_size"      : len(file_polarities),
                "negators"             : file_statistics['negators'],
                "negated_words"        : file_statistics['neg_word']
            }

    def get_polarities(self):
        return self.polarities

    def save(self, output_dir = outputdir):
        if not os.path.isdir(output_dir): os.makedirs(output_dir)
        for (file_name, pol) in self.polarities.iteritems():
            cdir = "%s/%s" % (output_dir,file_name.replace('corpus', 'polarities'))
            with codecs.open(cdir, "w", "utf-8") as f:
                json.dump(pol, f,indent=4,sort_keys=True,ensure_ascii=False)
            print "Result was saved in %s\n" % cdir


if __name__ == "__main__":

    start_time = time.time()

    generator = IndependentLexiconGenerator()
    generator.generate()
    generator.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
