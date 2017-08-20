# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *

from keras.models import Sequential
from keras.layers import Dense
import OpinionsDatabase as db 
import os, json, io, glob, re



tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")



sources = [
    "corpus_apps_android",
    "corpus_cine",
    "corpus_hoteles",
    "corpus_prensa_uy",
    "corpus_tweets",
    "corpus_tweets_2",
    "corpus_variado_sfu"
]
sources_size = len(sources)



class Network:
     
    def __init__(self,
            win_size,
            hidden_layers=2,
            activation=['relu'],
            loss='binary_crossentropy', 
            optimizer='adam', 
            metrics=['accuracy'],
            neurons=(12,8)
        ):
        left = hidden_layers - len(activation)
        
        for _ in range(left):
            activation.append(activation[0])
             
        self.model = Sequential()
        
        self.model.add( Dense( neurons[0] , input_dim=win_size , activation=activation[0] ) )
        for i in range(hidden_layers)[:-1]:
            self.model.add( Dense( neurons[0] , activation=activation[i+1] ) )
        self.model.add( Dense( 2 , activation=activation[i+1] ) )
        
        self.model.compile(loss=loss, optimizer=optimizer , metrics=metrics)
     
     
    def fit(self,opinions, window_left, window_right):
        X , Y = [] , []
        total = len(opinions)
        for idx,op in enumerate(opinions):
            progress("Fitting negations",total,idx)
            entry = get_vectors(op.text, window_left, window_right)
            X.append(entry[0])
            Y.append(entry[1])
            
        if not X:
            raise Exception("Nothing to fit")
        
        self.model.fit(X,Y)
        
        scores = model.evaluate(X, Y)        
        for i in range(len(scores)):
            print "\n%s: %.2f%%" % (model.metrics_names[i], scores[i]*100)
    
    def predict(self,opinions, window_left=2, window_right=2):
        results = {}
        total = len(opinions)
        for idx,op in enumerate(opinions):
            progress("Predicting negations",total,idx)
            results[op._id] = [ self.model.predict(X) for X in get_vectors(op.text, window_left, window_right)[0] ]
        return results
    
    def get_vectors(text, window_left=2, window_right=2):
        vectors = []
        tags = []
        for idx, word in enumerate(text):
            vec = []
            for i in range(window_left + window_right + 1):
                vec.append(get_entry(text, idx - window_left + i))
            tags.append(text[idx].get('negated'))
            vectors.append(vec)
        return vectors, tags    
    
    def get_entry(text, idx):
        if  0 <= idx < len(text) :
            return text[idx]['word']
        else :
            return ''
        


def start_tagging():
    
    def DisplayMenu():
        os.system('clear')
        print "*"*20," MENU ","*"*20
        print "0 . exit"
        i = 1
        while i <= sources_size:
            print i,".",sources[i-1] ; i+=1
        print i,". from files"
        return 
     
    def DisplayReview(_id,current,total,words,tags):
        os.system('clear')
        print "Review [%s]" % _id
        print "<<",
        for i in range(total):
            if i < current and tags[i] == 'n':
                print words[i]+"\033[93m/"+tags[i]+"\033[0m",
            elif i < current:
                print words[i]+"\033[91m/"+tags[i]+"\033[0m",
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
    
    def ViewSave(result):
        os.system('clear')
        op = raw_input("Done! View result? (y/n) > ")
        # Ask for display
        if op.lower() == 'y':
            DisplayAnnotated(result)
        # Ask for save in two steps
        op = raw_input("\nSave result? [y/n] > ")
        if op.lower() == 'n':
            op = raw_input("Are you sure? [y/n] > ")
            if op.lower() == 'y':
                return
        # Save the result
        db.save_negations(result)
        
    # #------- Execute Function -------#
    
    while True:
        # Display menu options
        DisplayMenu()
        op = raw_input("\nOption > ")
        if not op.isdigit() or int(op) > sources_size:
            raw_input("Opcion invalida")
            continue
        op = int(op)
        if op == 0:
            # Exit
            break
        else:    
            result,id = [],0        
            try:     
                # Ask for retrieving options 
                source = sources[op-1]
                op = raw_input("\nInsert indexes separated by ',' or <intro> for pick up randomly > ")
                if op: # From indexes
                    indexes = list(set(int(i) for i in op.split(',')))
                    quantity = len(indexes)
                    indexes = indexes[:quantity]
                else: # Randomly
                    while not op.isdigit():
                        op = raw_input("How many? > ")
                    quantity = int(op)
                    indexes = []
                
                # Get a sample of reviews from options
                samples = db.get_sample(quantity,source,indexes)
                
                # Tag every review
                left = quantity
                while left != 0:   
                                     
                    # Retrieve relevant data from the sample
                    sample  = samples[left-1]
                    _id     = sample['_id']
                    review  = sample['text']
                    
                    # Initialization (keep current words and empty categories)
                    words = [item['word'] for item in review]
                    total = len(words)
                    tags  = ['  ' for _ in range(total)]
                    
                    # For each word, annotate with (N) or (I) and give the possibility of back by pressing (B)
                    cat = ""
                    idx = 0
                    while True:
                        # Display review
                        DisplayReview(_id,idx,total,words,tags)
                        
                        # Check end condition
                        if idx == total:
                            op = raw_input("\nDone. Proceed with the next review (left %i)? [y/n] > " % (left-1))
                            if op == 'y':
                                break
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = '  '
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
                            tags[idx] = '  '
                        elif cat == 'a':
                            op = raw_input("Are you sure you want to abort (left %i)? [y/n] > " % left)
                            if op.lower() == 'y': raise Exception("Abort")
                        else:
                            # Associate the category
                            tags[idx] = cat
                            idx = idx + 1
                            
                    # Once the text is tagged, add it to the result
                    result.append({
                        _id : enumerate(tags)
                    })
                    
                    # Update
                    left -= 1
                       
                # View and save results
                if op == 0: continue
                ViewSave(result)
                
            except Exception as e:
                content = json.dumps(result,indent=4,ensure_ascii=False)
                error = "Corpus:%s, Review:%i, Description:%s Partial:%s" % (source,id,str(e),content)
                log(error)
                raw_input("Reason: %s\nEnter to continue..." % str(e))
    
    
import re
def manual_file_to_db(source_dir):
    for source in glob.glob(source_dir):
        with open(source) as fp:
            print source
            opinions = json.load(fp)
        negations = {}
        errors = []
        for idx, op in enumerate(opinions):
            target = db.get_by_idx(op['from'], op['id'])
            if 'negated' in target['text'][idx].keys(): # Skip if already re-tagged
                break
            tags  = [tag[-1] for tag in op['annotation'].split(' ')]
            words = [item['word'].lower() for item in target['text']]
            annot = [tag[:-2].lower() for tag in op['annotation'].split(' ')]
            if words != annot:
                size = len(words)
                retags = [None for _ in range(size)]
                idxW,idxA = 0,0
                try:
                    qW,qA = [],[]
                    while True:
                        os.system('clear')
                        print op['from'], op['id']
                        print "WORDS"
                        print ' '.join(words),"\n"
                        print "ANNOT"
                        print ' '.join(annot),"\n" 
                        if idxW >= len(words) or idxA >= len(annot):
                           break 
                        if words[idxW] == annot[idxA]:
                            if idxW < len(retags) and idxA < len(tags):
                                retags[idxW] = tags[idxA]
                                qW.append(idxW)
                                qA.append(idxA)
                                idxW += 1
                                idxA += 1
                        elif annot[idxA] == '.':
                            qA.append(idxA)
                            idxA += 1 
                        else:
                            print "%-10s vs %10s" % (words[idxW],annot[idxA])
                            opt = raw_input("(S)kip or (B)orrow ? Tap <enter> for previous > ")
                            if opt == 'b': 
                                retags[idxW] = tags[idxA]
                                qW.append(idxW)
                                idxW += 1
                            elif opt == 's':
                                qA.append(idxA)
                                idxA += 1
                            else:
                                idxW = qW.pop()
                                idxA = qA.pop()
                except Exception as e:
                    print str(e)
                    print "words",idxW,len(words)
                    print "annot",idxA,len(annot)
                    print "tags",idxA, len(tags)
                    raw_input()
                tags = retags 
            negations[target['_id']] = map(lambda x: x == 'i', tags)
        
        db.save_negations(negations)
    
                
if __name__=='__main__':
#     start()
    manual_file_to_db("outputs/negation/*")
    