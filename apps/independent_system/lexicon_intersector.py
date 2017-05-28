# -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities') # To import 'utilities' modules

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
log = Log(logdir)

class IndependentLexiconIntersector:
   

    def __init__(self,tolerance=0.0,input_dir=inputdir):
        input_dir = input_dir if input_dir[-1] != "/" else input_dir[:-1]
        self.files       = glob.glob(input_dir + '/polarities*.json')
        self.polarities  = defaultdict(list)
        self.min_matches = int(round(len(self.files)*(1-tolerance),0))
        self.lexicon = {}

    def intersect_corpus(self):
        
        def all_equal(list):
            return all(map(lambda x: x == list[0], list))

        polarities = defaultdict(list)
        word_statistics = defaultdict(lambda : defaultdict(int))

        for file in self.files:
            try:
                file_name = file.split('/')[-1]
                with codecs.open(file, "r", "utf-8") as f:
                    corpus_polarities = json.load(f)
                words_count = len(corpus_polarities['words'])
                for idx, word in enumerate(corpus_polarities['words']):
                    word_statistics[word]['pos'] += corpus_polarities['words'][word]['positives_ocurrences']
                    word_statistics[word]['neg'] += corpus_polarities['words'][word]['negatives_ocurrences']
                    word_statistics[word]['neu'] += corpus_polarities['words'][word]['neutral_ocurrences']
                    polarities[word].append(
                        corpus_polarities['words'][word]['polarity'])
                    progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx)
            except Exception as e:
                log(str(e))
                raise e
            progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx+1)
            print 
        
        words_polarities = {
            word: {
                'polarity'               : polarities[word][0],
                'matches'                : len(polarities[word]),
                'positives_ocurrences'   : word_statistics[word]['pos'],
                'negatives_ocurrences'   : word_statistics[word]['neg'],
                'neutral_ocurrences'     : word_statistics[word]['neu'],
                'total_ocurrences'       : word_statistics[word]['pos'] + word_statistics[word]['neg'] + word_statistics[word]['neu']
            } for word in polarities if  len(polarities[word]) >= self.min_matches  and all_equal(polarities[word])
        } 

        self.lexicon['analytics'] = {
            'parsed_corpus'        : len(self.files),
            'positive_words'       : len(filter(lambda word: words_polarities[word]['polarity'] == "+", words_polarities.keys())),
            'negative_words'       : len(filter(lambda word: words_polarities[word]['polarity'] == "-", words_polarities.keys())),
            'neutral_words'        : len(filter(lambda word: words_polarities[word]['polarity'] == "0", words_polarities.keys())),
            'total_words'          : len(words_polarities)
        }

        self.lexicon['words'] = words_polarities;

    def save(self, output_dir = outputdir):
        cdir = "%s/independen_lexicon_(MATCHES_%i_of_%i).json" % (outputdir, self.min_matches, len(self.files))
        with codecs.open(cdir , "w", "utf-8") as f:
            json.dump(self.lexicon, f, indent=4, ensure_ascii=False)
        print "Result was saved in %s\n" % cdir



#=====================================================================================================
if __name__ == "__main__":

    start_time = time.time()

    intersector = IndependentLexiconIntersector(tolerance=1)
    intersector.intersect_corpus()
    intersector.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)

