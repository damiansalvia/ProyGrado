# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from printHelper import Log

import OpinionsDatabase as db 
import os, random, json, io



tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")


sources = [
    "corpus_apps_android",
    "corpus_cine",
    "corpus_hoteles",
    "corpus_prensa_uy"
    "corpus_tweets",
    "corpus_tweets_2",
    "corpus_variado_sfu"
]



def start(sample):
    
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
            if i < current and cats[i] == 'n':
                print words[i]+"\033[93m/"+cats[i]+"\033[0m",
            elif i < current:
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
        db.save_negations(result)
        
    
    while True:
        # Display menu options
        DisplayMenu()
        op = raw_input("\nOption > ")
        if not op.isdigit() or op > len(sources):
            print "Opcion invalida"
            continue
        op = int(op)
        if op == 0:
            # Exit
            break
        else:            
            try:     
                # Ask for retrieving options 
                op = raw_input("\nInsert IDs separated by ',' or <intro> for pick up randomly > ")
                if op: # From indexes
                    indexes = [int(i) for i in op.split(',')]
                    indexes = set(indexes)  # Ensure no duplicated
                    indexes = list(indexes) # Transform
                    left = len(indexes)
                else: # Randomly
                    while not op.isdigit():
                        op = raw_input("How many? > ")
                    left = int(op)
                    indexes = range(len(reviews))
                    random.shuffle(indexes)
                indexes = indexes[:left]
                
                # Get a sample of reviews from options
                source = sources[op-1]
                reviews = db.get_sample(quantity, source,indexes)
                
                # Tag every review
                result = []
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
                raw_input("Reason: %s\nEnter to continue..." % str(e))
    