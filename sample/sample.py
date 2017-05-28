# -*- coding: utf-8 -*-

import sys
sys.path.append('../apps/independent_system')
sys.path.append('../apps/utilities')

from corpus_parser import CorpusParser
from lexicon_generator import IndependentLexiconGenerator
from lexicon_intersector import IndependentLexiconIntersector
import glob

negators_list = [
    u"aunque", u"denegar", u"jamás", u"nada", u"nadie", u"negar", 
    u"negativa", u"ni", u"ninguna", u"ninguno", u"ningún", 
    u"no", u"nunca", u"pero", u"rehúso", u"tampoco"
]

corpus_sources = [
    "../corpus/corpus_cine",
    "../corpus/corpus_tweets",
    "../corpus/corpus_hoteles",
    "../corpus/corpus_prensa_uy",
    "../corpus/corpus_apps_android",
    "../corpus/corpus_variado_sfu"
]

for source_file in corpus_sources:
    parser = CorpusParser(cdir=source_file,ldir="./log/")
    parser.parse()
    parser.save("./tmp/corpus")

win_sizes = zip(range(4),range(2))

for source_file in glob.glob("./tmp/corpus/*.json"):
    for (win_left,win_right) in win_sizes:
        generator = IndependentLexiconGenerator(
                        input_dir=source_file, 
                        negators_list=negators_list,
                        window_left=win_left, 
                        window_right=win_right,
                        ldir='./log/'
                    )
        generator.generate()
        generator.save("./tmp/polarities_win_%i_%i" % (win_left,win_right))
 
for (win_left,win_right) in win_sizes:
    polarity_sources = glob.glob("./tmp/polarities_win_%i_%i" % (win_left,win_right))
    total = len(polarity_sources)
    for source_file in polarity_sources:
        for cantidad in range(total):
            intersector =   IndependentLexiconIntersector(
                                input_dir = source_file,
                                tolerance = cantidad/total
                            )
            intersector.intersect_corpus()
            intersector.save("./tmp/lexicon")