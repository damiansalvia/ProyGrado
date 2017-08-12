# -*- coding: utf-8 -*-

# Corpus sources paths
parameters = [
    ("../../corpus/corpus_apps_android","*/*.json","\"(.*?)\"[,(?:\\r\\n)]","(.*?)/","PATH",
        None,0,0,'unicode-escape',{'neg': 0,'pos': 100}),
    ("../../corpus/corpus_cine","*.xml","<body>(.*?)</body>","rank=\"(.*?)\"","FILE",
        "BEFORE",None,0,'utf8',{u'1': 0, u'2': 25, u'3': 50, u'4': 75, u'5': 100}),
    ("../../corpus/corpus_hoteles","*.xml","<coah:review>(.*?)</coah:review>","<coah:rank>(.*?)</coah:rank>","FILE",
        "BEFORE",None,0,'utf8',{u'1': 0, u'2': 25, u'3': 50, u'4': 75, u'5': 100}),
    ("../../corpus/corpus_prensa_uy","*.csv","\"(.*?)\",(?:TRUE|FALSE)",",(.*?)\\n","FILE",
        "AFTER",None,0,'utf8',{u'Neg': 0, u'Neu': 50, u'Pos': 100}),
    ("../../corpus/corpus_tweets","*.tsv","(.*?)\\t.*?\\n","(.*?\\t.*?)\\t","FILE",
        "BEFORE",None,1,'utf8',{u'3\t1': 10, u'3\t2': 20, u'2\t4': 90, u'2\t2': 70, u'2\t3': 60, u'4\t2': 30, u'2\t1': 80, 
                                u'5\t1': 40, u'1\t5': 50, u'1\t4': 30, u'4\t1': 50, u'1\t1': 40, u'1\t3': 60, u'1\t2': 70}),
    ("../../corpus/corpus_variado_sfu","*/*.txt","(.*)\s","(.*?)_","PATH",
        None,1,0,'utf8',{'no': 0, 'yes': 100})
]

# Read each corpus
from corpus_reader import CorpusReader
for parameter in parameters:
    reader = CorpusReader(
                    parameter[0],
                    parameter[1],
                    parameter[2],
                    parameter[3],
                    parameter[4],
                    category_position=parameter[5],
                    category_level=parameter[6],
                    start=parameter[7],
                    decoding=parameter[8],
                )
    fun = parameter[9]
    data = reader.get_data(lambda x:fun[x])
    
