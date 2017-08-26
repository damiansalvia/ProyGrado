 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
from utilities import *

import CorpusReader as cr 
import DataProvider as dp
import NegationTagger as nt
import TextAnalyzer as ta        


parameters = [
    (
        "../../corpus/corpus_apps_android",
        "*/*.json",
        "\"(.*?)\"[,(?:\\r\\n)]",
        "(neg|pos)/",
        {
            'neg': 20,
            'pos': 80
        },
        "PATH",
        None,
        0,
        0,
        'unicode-escape'
    ),
    (
        "../../corpus/corpus_cine",
        "*.xml",
        "<body>(.*?)</body>",
        "rank=\"([1-5])\"",
        {
            '1': 0, 
            '2': 25, 
            '3': 50, 
            '4': 75, 
            '5': 100
        },
        "FILE",
        "BEFORE",
        None,
        0,
        'cp1252'
    ),
    (
        "../../corpus/corpus_hoteles",
        "*.xml",
        "<coah:review>(.*?)</coah:review>",
        "<coah:rank>([1-5])</coah:rank>",
        {
            '1': 0, 
            '2': 25, 
            '3': 50, 
            '4': 75, 
            '5': 100
        },
        "FILE",
        "BEFORE",
        None,
        0,
        'utf8'
    ),
    (
        "../../corpus/corpus_prensa_uy",
        "*.csv",
        "\#(.*(?!TRUE|FALSE)),[^ ]", # No considera el test.csv, el "\#" significa "no uses re.DOTALL" 
        ",(Neg|Neu|Pos)\\n",
        {
            'Neg': 0, 
            'Neu': 50, 
            'Pos': 100
        },
        "FILE",
        "AFTER",
        None,
        0,
        'utf8'
    ),
    (
        "../../corpus/corpus_tweets",
        "*.tsv",
        "(.*?)\\t.*?\\n",
        "(\d\\t\d)\\t",
        {
            '3\t1': 10, 
            '3\t2': 20, 
            '2\t4': 90, 
            '2\t2': 70, 
            '2\t3': 60, 
            '4\t2': 30,
            '2\t1': 80, 
            '5\t1': 40, 
            '1\t5': 50, 
            '1\t4': 30, 
            '4\t1': 50, 
            '1\t1': 40, 
            '1\t3': 60, 
            '1\t2': 70
        },
        "FILE",
        "BEFORE",
        None,
        1,
        'utf8'
    ),
    (
        "../../corpus/corpus_variado_sfu", 
        "*/*.txt", 
        "(.*)\s",
        "(yes|no)_",
        {
            'no' : 20, 
            'yes': 80
        },
        "PATH",
        None,
        1,
        0,
        'unicode-escape'
    ),
    (
        "../../corpus/corpus_tweets_2",
        "*.csv",
        "\"(.*?)\",",
        "(N|P|NEU|NONE)\\n",
        {
            'N'   :0,
            'NEU' :50,
            'NONE':50,
            'P'   :100
        },
        "FILE",
        "AFTER",
        None,
        1,
        'utf8'
    ),
    (
        "../../corpus/corpus_restaurantes",
        "*/*.json",
        "\"(.*?)\"[,(?:\\r\\n)]",
        "(neg|pos)/",
        {
            'neg': 20,
            'pos': 80
        }, 
        "PATH",
        None,
        0,
        0,
        'unicode-escape'
    )
] 

# count = 0
# for parameter in parameters: 
#               
#     opinions = cr.from_corpus(
#             parameter[0], # source
#             parameter[1], # path pattern to file
#             parameter[2], # review pattern
#             parameter[3], # category pattern
#             parameter[4], # category mapping
#             parameter[5], # category mapping
#             category_position=parameter[6],
#             category_level=parameter[7],
#             start=parameter[8],
#             decoding=parameter[9],
#             tofile=True
#         )
#            
#     analyzed = ta.analyze(
#             opinions,
#             tofile=True
#         )
#        
#     count += len(analyzed)
#        
# raw_input("Total %i .Continue..." % count)
#
# dp.update_embeddings(verbose=True)
#         
# nt.start_tagging(tofile=True) 
 
ann = nt.NeuralNegationTagger(2,2)     
ann.fit_tagged()
ann.predict_untagged()    
# dp.save_negation(Y,tagged_as='automatically')

# tolerance = 1.0
# li = dp.get_indepentent_lex(tolerance=tolerance)
# save(li,"independent_lexcon_-_tolerance_%i_percent" % (tolerance*100),"./outputs/lexicon")
# li = dp.get_indepentent_lex2(tolerance=tolerance)
# save(li,"independent_lexcon_2_-_tolerance_%i_percent" % (tolerance*100),"./outputs/lexicon")
 



 


    