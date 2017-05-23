# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json
import glob
from collections import defaultdict
from printHelper import *

inputdir  = 'outputs/corpus/'
outputdir = 'outputs/lexicons/single_corpus_lexicon/'
logdir    = '../log/'
log = Log(logdir)


class IndependentLexiconGenerator:
    

    def __init__(self, input_dir = inputdir):
        self.files = glob.glob(input_dir + 'corpus*.json')
        self.polarities = {}
    

    def generate(self):

        def get_tokens(review):
            return nltk.word_tokenize(review)

        def get_polarity(list):
            val = sum(list)/len(list)
            if val < 40:
                return '-'
            elif val > 60:
                return '+'
            else:
                return '0'

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
                    for token in tokens:
                        occurrences[token.lower()].append(rank) 
                except Exception as e:
                    log(str(e))
                    raise e
            progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", corpus_length, idx+1)
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
    generator.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
