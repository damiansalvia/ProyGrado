# -*- encoding: utf-8 -*-
'''
Module with negation utilities
@author: Nicolás Mechulam, Damián Salvia
'''

import os
clean = 'cls' if os.name == 'nt' else 'clear'

from colorama import init, Fore, Style, Back
init(autoreset=True) 

from cldas.utils import progress, save, title, Log, load
from cldas.morpho import Preprocess

log = Log("../log") 


def interactive_prediction(model,formatter, **kwrgs):
    '''
    Makes predictions interactively from console input.
    @param model      : Keras model of a Neural Networ (FFN or LSTM).
    @param formmatter : Function to format X and Y dataset from input.  
    ''' 
    while True:   
        os.system(clean)
        print Fore.YELLOW + Style.BRIGHT + 'New text'
        print '>', ; text = raw_input()
        
        preproc = Preprocess( 'Test', [{'text':text,'category':None}], verbose=False )
        data = preproc.data()
        
        X,_ = formatter( data, **kwrgs )
        Y = model.predict( X )
        
        os.system(clean)
        print Fore.YELLOW + Style.BRIGHT +'Result'
        print ' '.join(["%s" % (
                    Fore.MAGENTA+Style.BRIGHT+word if neg 
                    else Fore.RESET+Style.RESET_ALL+word 
                ) for word,neg in zip( [token['word'] for token in data[0]['text']], Y ) ])  
        
        if not raw_input("\nContinue..."):
            os.system(clean)
            break


def manual_tagging(dp,tofile='./neg/manual'):
    '''
    Displays command-line interface for start manual tagging
    @param dp    : Data provider as cldas.db.crud operations.
    @param tofle : Directory path where negation tags will be stored.  
    '''
    
    sources = dp.get_sources()
    sources_size = len( sources )
    
    def DisplayMenu():
        os.system(clean)
        title("MENU")
        print "0 . exit"
        for i in range( len(sources) ): 
            qty = len( dp.get_tagged( dp.TaggedType.MANUAL , sources[i]) ) 
            print i+1,".","%-30s" % sources[i], "(%i)" % qty
        return 
     
    def DisplayReview(_id,current,total,words,tags):
        os.system(clean)
        print "Review [%s]" % _id
        print "<<",
        for i in range(total):
            if i < current and tags[i] == 'n':
                print words[i] + Fore.GREEN + Style.BRIGHT + "/"+tags[i] + Style.RESET_ALL,
            elif i < current:
                print words[i] + Fore.MAGENTA + Style.BRIGHT +"/"+tags[i] + Style.RESET_ALL,
            elif i > current:
                print words[i]+"  ",
            else:
                print Back.BLUE + Fore.WHITE +words[i]+Style.RESET_ALL,
        print ">>"
        
    def chunkstring(string, length):
        return ( string[0+i:length+i] for i in range(0, len(string), length) )
    
    def ViewSave(result,source):
        os.system(clean)
        if not result:
            return

        op = raw_input("Done! Save result for %s? [y/n] > " % source)
        if op.lower() == 'n':
            op = raw_input("Are you sure? [y/n] > ")
            if op.lower() == 'y':
                return
        
        save( result,"negtag_%s" % source, tofile, overwrite=False )
        
    # #------- Execute Function -------#
    
    while True:
        DisplayMenu()
        
        op = raw_input("\nOption > ")
        if not op.isdigit():
            raw_input("Opcion invalida")
            continue
        
        op = int(op)
        if op == 0:
            break 
        
        if op > sources_size:
            raw_input("Opcion invalida")
            continue
        
        else:    
            result = {}        
            source = sources[op-1]
            try:     
                
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
                
                samples = dp.get_sample(quantity,source,indexes)
                
                left = quantity
                while left != 0:   
                                     
                    # Retrieve relevant data from the sample
                    sample  = samples[left-1]
                    _id     = sample['_id']
                    review  = sample['text']
                    
                    # Initialization (keep current words and empty categories)
                    words = [item['word'].encode('ascii','ignore') for item in review]
                    total = len(words)
                    tags  = ['  ' for _ in range(total)]
                    
                    # For each word, annotate with (N) or (I) and give the possibility of back by pressing (B)
                    cat = "" ; idx = 0
                    
                    while True:
                        
                        DisplayReview( sample['_id'], idx, total, words, tags )
                        
                        # Check end condition
                        if idx == total:
                            op = raw_input("\nDone. Proceed with the next review (left %i)? [y/n] > " % (left-1)) if left-1 != 0 else 'y'
                            if op == 'y':
                                break
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = '  '
                            continue
                        
                        # Ask for input
                        tooltip  = "\nTag with N(ormal) or I(nverted). "
                        tooltip += "Enter A(bort), B(ack) S(kip), Q(uit) or <intro> for "
                        tooltip += "repeating last action (%s) > " % (cat.upper() if cat else "None")
                        tag = raw_input(tooltip)
                        
                        if not tag and not cat: # Prevents parse empty cat
                            raw_input("Input a category first")
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in 'nibasq':
                            raw_input("Option '%s' is not correct." % cat)
                            continue
                        if cat == 'q'or cat == 's':
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
                    
                    if cat == 'q':
                        break
                    if cat == 's':
                        left -= 1
                        continue
                            
                    # Once the text is tagged, add it to the result
                    tags = map( lambda cat : cat =='i', tags )
                    result.update({ _id:tags })
                    
                    # Update
                    left -= 1
                       
                # View and save results
                if op == 0: continue
                ViewSave(result,source)
                
            except Exception as e:
                content = '\n'.join([ _id+">>"+str(tags) for _id,tags in result.items() ])
                log("Reason : %s (at %s) [%i] '%s'" % ( str(e) , source , sample['_id'] , content ))
                raw_input("Reason: %s\nEnter to continue..." % str(e))


