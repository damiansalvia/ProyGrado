# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from printHelper import Log

from corpus_reader import CorpusReader
import os, random, json, io

tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")

# source extension review_pattern category_pattern category_location category_position category_level start decoding
parameters = [
    ("../../corpus/corpus_apps_android","*/*.json","\"(.*?)\"[,(?:\\r\\n)]","(.*?)/","PATH",None,0,0,'unicode-escape'),
    ("../../corpus/corpus_cine","*.xml","<body>(.*?)</body>","rank=\"(.*?)\"","FILE","BEFORE",None,0,'cp1252'),
    ("../../corpus/corpus_hoteles","*.xml","<coah:review>(.*?)</coah:review>","<coah:rank>(.*?)</coah:rank>","FILE","BEFORE",None,0,'utf8'),
    ("../../corpus/corpus_prensa_uy","*.csv","\"(.*?)\",(?:TRUE|FALSE)",",(.*?)\\n","FILE","AFTER",None,0,'utf8'),
    ("../../corpus/corpus_tweets","*.tsv","(.*?)\\t.*?\\n","(.*?\\t.*?)\\t","FILE","BEFORE",None,1,'utf8'),
    ("../../corpus/corpus_variado_sfu","*/*.txt","(.*)\s","(.*?)_","PATH",None,1,0,'unicode-escape'),
    ("../../corpus/corpus_tweets_2","*.csv","\"(.*?)\",","(.*?)\\n","FILE","AFTER",None,1,'utf8')
]
 
def DisplayMenu():
    os.system('clear')
    print "*"*20," MENU ","*"*20
    print "0 . exit"
    for i,parm in enumerate(parameters):
        print i+1,".",parm[0].split('/')[-1]
    return 
 
def DisplayReview(id,current,total,words,cats):
    os.system('clear')
    print "Review [%i]" % id
    print "<<",
    for i in range(total):
        if i < current:
            if cats[i] == 'n':
                print words[i]+"\033[93m/"+cats[i]+"\033[0m",
            else:
                 print words[i]+"\033[91m/"+cats[i]+"\033[0m",
        elif i > current:
            print words[i]+"  ",
        else:
            print "\033[92m\033[4m"+words[i]+"\033[0m\033[0m  ",
    print ">>"
    
def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def DisplayAnnotated(result,width=WIDTH):
    width = width-10
    row   = "%-7s | %-"+str(width)+"s"
    line  = "%-7s-+-%-"+str(width)+"s"
    print row% ("ID","ANNOTATION")
    print line % ("-"*7,"-"*width)
    for item in result:
        chunks = chunkstring(item['annotation'], width)
        chunks = list(chunks)
        print row % (str(item['id']),chunks[0])
        for chunk in chunks[1:]:
            print row % ("",chunk)
        print line % ("-"*7,"-"*width)

def ViewSave(result,name,encoding='utf8'):
    os.system('clear')
    op = raw_input("Done! View result? (y/n) > ")
    # Ask for display
    if op.lower() == 'y':
        DisplayAnnotated(result)
    # Ask for save twice 
    op = raw_input("\nSave result? [y/n] > ")
    if op.lower() == 'n':
        op = raw_input("Are you sure? [y/n] > ")
        if op.lower() == 'y':
            return
    # Save the result
    odir = "./outputs/negation"
    if not os.path.isdir(odir): 
        os.makedirs(odir)
    odir = odir+"/negated_%s.json" % name
    with io.open(odir,"w",encoding=encoding) as f:
        content = json.dumps(result,indent=4,ensure_ascii=False)
        if not isinstance(content, unicode):
            content = unicode(content,'utf8')
        f.write(content) 

def Main():
    while True:
        # Display menu options
        DisplayMenu()
        op = raw_input("\nOption > ")
        if not op.isdigit() and int(op) in [0,1,2,3,4,5,6]:
            print "Opcion invalida"
            continue
        op = int(op)
        if op == 0:
            # Exit
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
            
            try:     
                # Get reviews and shuffle them 
                reviews = list(enumerate(corpus.get_opinions()))
                op = raw_input("\nInsert IDs separated by ',' or <intro> for randomly > ")
                if op: # From indexes
                    indexes = [int(i) for i in op.split(',')]
                    left = len(indexes)
                else: # Randomly
                    while not op.isdigit():
                        op = raw_input("How many? > ")
                    left = int(op)
                    indexes = range(len(reviews))
                    random.shuffle(indexes)
                indexes = indexes[:left]
                reviews = [(i,review) for (i,review) in reviews if i in indexes]
                result = []
                
                # Tag every review
                while left != 0:   
                                     
                    # Start
                    id,review = reviews[left-1]
                    words = review.split(' ')
                    total = len(words)
                    cats = ['  ' for _ in range(total)]
                    
                    # For each word annotate with (N) or (I) and give the possibility of back by pressing (B)
                    cat = ""
                    idx = 0
                    while True:
                        # Display review
                        DisplayReview(id,idx,total,words,cats)
                        
                        # Check end condition
                        if idx == total:
                            op = raw_input("\nDone. Proceed with the next review (left %i)? [y/n] > " % (left-1))
                            if op == 'y':
                                break
                            idx = idx - 1 if idx != 0 else 0
                            cats[idx] = '  '
                            continue
                        
                        # Ask for input
                        tooltip  = "\nTag with N(ormal) or I(nverted). "
                        tooltip += "Enter A(bort), B(ack) or <intro> for "
                        tooltip += "repeating last action (%s) > " % (cat.upper() if cat else "None")
                        tag = raw_input(tooltip)
                        
                        if not tag and not cat: # Prevents parse empty cat
                            print "Input a category first";raw_input()
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in 'niba':
                            print "Option",cat,"is not correct." ;raw_input()
                            continue
                        if cat == 'b': # Back
                            idx = idx - 1 if idx != 0 else 0
                            cats[idx] = '  '
                        elif cat == 'a':
                            op = raw_input("Are you sure you want to abort (left %i)? [y/n] > " % left)
                            if op.lower() == 'y': raise Exception("Abort")
                        else:
                            # Associate the category
                            cats[idx] = cat
                            idx = idx + 1
                            
                    # Save the result as two list: words and its respective category for each one 
                    result.append({
                        "id" : id+1,
                        "from" : name,
                        "annotation" : ' '.join(word.lower()+"/"+cat for word,cat in zip(words,cats))
                    })
                    
                    # Update
                    left -= 1
                       
                # View and save results
                if op == 0: continue
                ViewSave(result,name)
            
            except Exception as e:
                content = json.dumps(result,indent=4,ensure_ascii=False)
                error = "Corpus:%s, Review:%i, Description:%s Partial:%s" % (name,id,str(e),content)
                log(error)
                raw_input("Reason: %s\nEnter to cotinue..." % str(e))
            
# Call to main program
Main()                        
            