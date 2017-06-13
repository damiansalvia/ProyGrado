# -*- coding: utf-8 -*-
from corpus_reader import CorpusReader
import os, random, json, io

tmp = os.popen('stty size', 'r').read().split()
width = int(tmp[1])-15 if tmp else 100

# source extension review_pattern category_pattern category_location category_position category_level start decoding
parameters = [
    ("../../corpus/corpus_apps_android","*/*.json","\"(.*?)\"[,(?:\\r\\n)]","(.*?)/","PATH",None,0,0,'unicode-escape'),
    ("../../corpus/corpus_cine","*.xml","<body>(.*?)</body>","rank=\"(.*?)\"","FILE","BEFORE",None,0,'utf8'),
    ("../../corpus/corpus_hoteles","*.xml","<coah:review>(.*?)</coah:review>","<coah:rank>(.*?)</coah:rank>","FILE","BEFORE",None,0,'utf8'),
    ("../../corpus/corpus_prensa_uy","*.csv","\"(.*?)\",(?:TRUE|FALSE)",",(.*?)\\n","FILE","AFTER",None,0,'utf8'),
    ("../../corpus/corpus_tweets","*.tsv","(.*?)\\t.*?\\n","(.*?\\t.*?)\\t","FILE","BEFORE",None,1,'utf8'),
    ("../../corpus/corpus_variado_sfu","*/*.txt","(.*)\s","(.*?)_","PATH",None,1,0,'utf8')
]
 
def DisplayMenu():
    print "************************ MENU ************************"
    print "0. SALIR"
    print "1. APPS" 
    print "2. CINE"
    print "3. HOTELES"
    print "4. PRENSA"
    print "5. TWEETS"
    print "6. SFU"
    return 
 
def DisplayStatus(idx,total,words,cats):
    for i in range(total):
        if i < idx:
            print words[i]+"\033[93m/"+cats[i]+"\033[0m",
        elif i > idx:
            print words[i],
        else:
            print '\033[92m'+words[i]+"\033[0m",
    print
 
while True:
    DisplayMenu()
    op = raw_input("> ")
    os.system('clear')
    if len(op)>1 or op not in "0123456":
        print "Opcion invalida"
        continue
    op = int(op)
    if op == 0:
        # Salir
        break
    else:
        # Read the parameters
        parameter = parameters[op-1]
        name = parameters[op-1][0].split("/")[-1]
        corpus = CorpusReader(
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
        # Ask how manu review for annotating
        op = ""
        while not op.isdigit():
            op = raw_input("How many? > ")
        left = int(op)
        # Get the reviews an shuffle them for pick random reviews
        reviews = corpus.get_opinions()
        random.shuffle(reviews)
        result = []
        for review in reviews:
            words = review.split(' ')
            total = len(words)
            cats = ['' for _ in range(total)]
            idx = 0
            # For each word annotate with N or I and give the positibility of back by pressing B
            while idx != total:
                os.system('clear') 
                DisplayStatus(idx,total,words,cats)
                cat = raw_input("N(ormal), I(nverted) or B(ack)? > ")
                cat = cat.upper()
                if cat not in 'NIBnib':
                    print "Option",cat,"is not correct." ;raw_input()
                    continue
                if cat == 'B':
                    # BACK
                    idx = idx - 1 if idx != 0 else 0
                    cats[idx] = ''
                else:
                    # Associate the category
                    cats[idx] = cat
                    idx = idx + 1
            # Save the result as two list: words and its respective category for each one 
            result.append({
                "id" : left,
                "annotation" : ' '.join(word+"/"+cat for word,cat in zip(words,cats))
#                 'id'         : left,
#                 'words'      : words,
#                 'categories' : cats  
            })
            # Check finish
            left -= 1
            if left == 0:
                print "DONE";raw_input()
                break
            print "Result added. Are you ready for the next? (left %i)" % left
        # Save the result
        odir = "./outputs/negation"
        if not os.path.isdir(odir): 
            os.makedirs(odir)
        odir = odir+"/negated_%s.json" % name
        with io.open(odir,"w",encoding='utf8') as f:
            content = json.dumps(result,indent=4,ensure_ascii=False)
            f.write(content)    
                    
            