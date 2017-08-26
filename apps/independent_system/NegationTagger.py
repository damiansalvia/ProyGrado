# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *

from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping,CSVLogger
import DataProvider as dp 
import os, json, io, glob, re
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'



tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")



sources = dp.get_sources()
sources_size = len(sources)



class NeuralNegationTagger:
     
    def __init__(self,
            win_left,
            win_right,
            hidden_layers=2,
            activation=['relu','relu','relu','sigmoid'],
            loss='binary_crossentropy', 
            optimizer='adam', 
            metrics=['accuracy'],
            early_monitor='loss',
            early_min_delta=0,
            early_patience=2,
            early_mode='auto',
        ):
        
        # Check restrictions
        min_activation_len = 2+hidden_layers
        if len(activation) < min_activation_len:
            raise Exception("Activation array size must be %i\n -- 1 input, %2 hidden, 1 output" % (min_activation_len,hidden_layers))
        
        # Parameters calculation
        vec_size  = dp.get_size_embedding()        
        input_dim = vec_size * (win_right + win_left + 1)
        
        # Attributes settings
        self.right = win_right
        self.left  = win_left
        self.dim   = input_dim
        
        # Callbacks settings
        self.callbacks = []
        self.callbacks.append(
            EarlyStopping(
                monitor=early_monitor,
                min_delta=early_min_delta,
                patience=early_patience, 
                mode=early_mode,
                verbose=0
            )
        )
        self.callbacks.append(
            CSVLogger('./log/training.log')
        )
        
        # Model definition     
        self.model = Sequential()
        
        # Input layer
        out_dim = input_dim / 2
        self.model.add( Dense( out_dim, input_dim=input_dim, activation=activation[0] )) 
        
        # Hidden layers
        for i in range(hidden_layers): 
            out_dim = out_dim / 2
            self.model.add( Dense( out_dim, activation=activation[i+1] )) 
        
        # Output layer - Binary: Negated or Not-negated
        self.model.add( Dense( 1, activation=activation[min_activation_len-1] ))
        
        # Compile model from parameters
        self.model.compile(loss=loss, optimizer=optimizer , metrics=metrics)
     
     
    def fit_tagged(self):    
        opinions = dp.get_tagged('manually') 
        X , Y = [] , []
        total = len(opinions)
        for idx,opinion in enumerate(opinions):
            progress("Fitting negations",total,idx)
            x,y = dp.get_embeddings( opinion['text'], self.left, self.right )
            X += x
            Y += y
        X = np.array(X)
        Y = np.array(Y)
        
        self.model.fit(X,Y,callbacks=self.callbacks,verbose=1)
        
        scores = self.model.evaluate(X,Y)        
        for i in range(len(scores)):
            print "\n%s: %.2f%%" % ( self.model.metrics_names[i], scores[i]*100 )
            
    
    def predict_untagged(self):
        opinions = dp.get_untagged()
        results = {}
        total = len(opinions)
        for idx,opinion in enumerate(opinions):
            progress("Predicting negations",total,idx)
            for X in dp.get_embeddings( opinion['text'], self.left, self.right )[0]:
                import pdb;pdb.set_trace()
                raw_input()
#                 X = X.reshape((-1, 1))
                Y = self.model.predict(X)
                results[ op['_id'] ] = Y
        return results
        


def start_tagging(tofile=False):
    
    def DisplayMenu():
        os.system('clear')
        print "*"*10," MENU ","*"*10
        print "0 . exit"
        for i in range(sources_size):
            qty = len(dp.get_tagged('manually',sources[i])) 
            print i+1,".","%-20s" % sources[i], "(%i)" % qty
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
    
    def ViewSave(result,source):
        os.system('clear')
        if not result:
            return

        op = raw_input("Done! Save result for %s? [y/n] > " % source)
        if op.lower() == 'n':
            op = raw_input("Are you sure? [y/n] > ")
            if op.lower() == 'y':
                return
            
        dp.save_negations(result,tagged_as='manually')
        if tofile:save(result,"negtag_%s" % source,"./outputs/tmp",overwrite=False)
        
    # #------- Execute Function -------#
    
    while True:
        # Display menu options
        DisplayMenu()
        
        op = raw_input("\nOption > ")
        if not op.isdigit():
            raw_input("Opcion invalida")
            continue
        op = int(op)
        if op == 0:
            break # Exit
            raw_input("Opcion invalida")
        if op > sources_size:
            continue
        else:    
            result = {}
            id     = 0        
            source = sources[op-1]
            try:     
                # Ask for retrieving options 
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
                samples = dp.get_sample(quantity,source,indexes)
                
                # Tag every review
                left = quantity
                skipped = False
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
                        DisplayReview(sample['idx'],idx,total,words,tags)
                        
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
                        tooltip += "Enter A(bort), B(ack) S(kip) or <intro> for "
                        tooltip += "repeating last action (%s) > " % (cat.upper() if cat else "None")
                        tag = raw_input(tooltip)
                        
                        if not tag and not cat: # Prevents parse empty cat
                            print "Input a category first";raw_input()
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in 'nibas':
                            print "Option",cat,"is not correct." ;raw_input()
                            continue
                        if cat == 's':
                            skipped = True
                            break
                        elif cat == 'b': # Back
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = '  '
                        elif cat == 'a':
                            op = raw_input("Are you sure you want to abort (left %i)? [y/n] > " % left)
                            if op.lower() == 'y': raise Exception("Abort")
                        else:
                            # Associate the category
                            tags[idx] = cat
                            idx = idx + 1
                    
                    if skipped:
                        break
                            
                    # Once the text is tagged, add it to the result
                    tags = map(lambda cat : cat =='i', tags)
                    result.update({
                        _id : tags
                    })
                    
                    # Update
                    left -= 1
                       
                # View and save results
                if op == 0: continue
                ViewSave(result,source)
                
            except Exception as e:
                content = json.dumps(result,indent=4,ensure_ascii=False)
                log("Reason : %s (at %s) [%i] '%s'" % ( str(e) , source , sample['idx'] , content ))
                raw_input("Reason: %s\nEnter to continue..." % str(e))
    
    
import re
def manual_file_to_dp(source_dir):
    for source in glob.glob(source_dir):
        with open(source) as fp:
            print source
            opinions = json.load(fp)
        negations = {}
        errors = []
        for idx, op in enumerate(opinions):
            target = dp.get_by_idx(op['from'], op['id'])
            if idx > len(target['text']) or u'negated' in target['text'][idx].keys(): # Skip if already re-tagged
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
                            opt = raw_input("(S)kip or (B)orrow ? Tap <enter> for previous or (N)ext > ")
                            if opt == 'b': 
                                retags[idxW] = tags[idxA]
                                qW.append(idxW)
                                idxW += 1
                            elif opt == 's':
                                qA.append(idxA)
                                idxA += 1
                            elif opt == 'n':
                                break
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
        
        dp.save_negations(negations)
    
    