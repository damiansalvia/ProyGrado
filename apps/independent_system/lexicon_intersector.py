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
        self.min_matches = int(round(len(self.files)*tolerance,0))

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
            
        self.lexicon = {
            word:{
                "rank":self.polarities[word][0],
                "matches":len(self.polarities[word])
            } 
            for word in self.polarities 
            if  len(self.polarities[word]) >= self.min_matches 
                and all_equal(self.polarities[word])
        } 


    def save(self, output_dir=outputdir):
        cdir = "%s/static_polarities_(match_%s).json" % (output_dir,self.min_matches)
        with codecs.open(cdir, "w", "utf-8") as f:
            json.dump(self.lexicon, f, indent=4, ensure_ascii=False)
        print "Result was saved in %s\n" % cdir



#=====================================================================================================
if __name__ == "__main__":

    start_time = time.time()

    intersector = IndependentLexiconIntersector(tolerance=0.33)
    intersector.intersect_corpus()
    intersector.save()

    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)

