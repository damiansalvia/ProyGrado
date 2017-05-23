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
log = Log(logdir)

MIN_MATCHES = 5

class IndependentLexiconIntersector:
   

    def __init__(self, input_dir = inputdir):
        self.files = glob.glob(input_dir + 'polarities*.json')
        self.polarities = defaultdict(list)

    def intersect_corpus(self):
        
        def all_equal(list):
            return all(map(lambda x: x == list[0], list))

        for file in self.files:
            try:
                file_name = file.split('/')[-1]
                with codecs.open(file, "r", "utf-8") as f:
                    corpus_polarities = json.load(f)
                words_count = len(corpus_polarities)
                for idx, (word,polarity) in enumerate(corpus_polarities.iteritems()):
                    progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx)
                    self.polarities[word].append(polarity)
            except Exception as e:
                log(str(e))
                raise e
            progressive_bar( 'Processing ' + file_name.replace('.json', '').replace('_', ' ') + " : ", words_count, idx+1)
            print 
        self.lexicon = {word:self.polarities[word][0] 
            for word in self.polarities if  len(self.polarities[word]) >= MIN_MATCHES and all_equal(self.polarities[word])} 


    def save(self, output_dir):
        with codecs.open(output_dir + 'static_polarities.json' , "w", "utf-8") as f:
            json.dump(self.lexicon, f, indent=4, ensure_ascii=False)



#=====================================================================================================
if __name__ == "__main__":

    start_time = time.time()

    intersector = IndependentLexiconIntersector()
    intersector.intersect_corpus()
    intersector.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)

