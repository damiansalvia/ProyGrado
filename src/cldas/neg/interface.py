# -*- encoding: utf-8 -*-
'''
Module with negation utilities
@author: Nicolás Mechulam, Damián Salvia
'''

import os
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
clean = 'cls' if os.name == 'nt' else 'clear'

from colorama import init, Fore, Style, Back
init(autoreset=True) 

from cldas.utils import progress, save, title, Log, load
from cldas import Preprocess

log = Log("../log") 


def interactive_prediction(model,formatter, **kwrgs):
    '''
    Makes predictions interactively from console input.
    @param model      : Keras model of a Neural Network (FFN or LSTM).
    @param formmatter : Function to format X and Y dataset from input.  
    ''' 
    while True:   
        os.system(clean)
        print Fore.YELLOW + Style.BRIGHT + 'NEW TEXT'
        print '>', ; text = raw_input()
        
        preproc = Preprocess( 'Test', [{'text':text,'category':None}], verbose=False )
        data = preproc.data()
        
        X,_ = formatter( data, **kwrgs )
        Y = model.predict( X )
        
        os.system(clean)
        print Fore.YELLOW + Style.BRIGHT +'PREDICTION RESULT'
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
    
    blank = ' '*5
    
    def DisplayMenu():
        os.system(clean)
        title("MENU")
        print "0 . exit"
        for i in range( len(sources) ): 
            qty = len( dp.get_tagged( dp.TaggedType.MANUAL , sources[i]) ) 
            print i+1,".","%-30s" % sources[i], "(%i)" % qty
        return 
    
    def DisplayHelp():
        print Fore.CYAN   + Style.BRIGHT + '<intro>', ':', 'Repeat last action.'
        print Fore.CYAN   + Style.BRIGHT + 'n      ', ':', '(N)ormal or (N)ot-inverted word. Tag \'O\'.'
        print Fore.CYAN   + Style.BRIGHT + 'e      ', ':', '(E)expresion of negation word.   Tag \'B-NEG\' (atomically).'
        print Fore.CYAN   + Style.BRIGHT + 'i      ', ':', '(I)nverted word.                 Tag \'B-INV\' or \'I-INV\'.'
        print Fore.CYAN   + Style.BRIGHT + 'b      ', ':', '(B)ack tagging previous.'
        print Fore.CYAN   + Style.BRIGHT + 's      ', ':', '(S)skip current tagging.'
        print Fore.CYAN   + Style.BRIGHT + 'q      ', ':', '(Q)uit tagging and return.'
        print Fore.CYAN   + Style.BRIGHT + 'a      ', ':', '(A)bort tagging and close.'
        print Fore.CYAN   + Style.BRIGHT + 'h      ', ':', '(H)elp.'
        raw_input('Enter to continue...')
        return
     
    def DisplayReview(_id,current,total,words,tags):
        os.system(clean)
        print "Review [%s]" % _id
        print "<<",
        for i in range(total):
            if i < current and tags[i].strip() == 'O': # not-inverted
                print words[i] + Fore.GREEN + Style.BRIGHT + "/"+tags[i] + Style.RESET_ALL,
            elif i < current and tags[i] == 'B-NEG': # neg-token
                print words[i] + Fore.MAGENTA + Style.BRIGHT + "/"+tags[i] + Style.RESET_ALL,
            elif i < current: # inverted
                print words[i] + Fore.RED + Style.BRIGHT +"/"+tags[i] + Style.RESET_ALL,
            elif i > current: # to be completed
                print words[i]+' '+tags[i],
            else: # current
                print Back.BLUE + Fore.WHITE + words[i] + Style.RESET_ALL +' '+tags[i],
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
                
                print '\nIdentifiers separated by \',\' or <intro> for pick up randomly'
                op = raw_input("> ")
                
                if op: # From indexes
                    indexes = list(set(int(i) for i in op.split(',')))
                    quantity = len(indexes)
                    indexes = indexes[:quantity]
                    
                else: # Randomly
                    while not op.isdigit():
                        print 'How many opinions?'
                        op = raw_input("> ")
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
                    words = [ item['word'].encode('ascii','ignore') for item in review ]
                    total = len( words )
                    tags  = [ blank for _ in range(total) ]
                    
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
                            tags[idx] = blank
                            continue
                        
                        # Ask for input
                        print "\n(H)elp. Last action (%s)" % (cat.upper() if cat else "-")
                        tag = raw_input("> ")
                        
                        if not tag and not cat: # Prevents parse empty cat
                            raw_input("Input a category first")
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in ['n','i','b','e','h','a','s','q']:
                            raw_input("Option '%s' is not correct." % cat)
                            continue
                        if cat == 'h':
                            DisplayHelp()
                            continue
                        elif cat == 'q'or cat == 's':
                            break
                        elif cat == 'b': # Back
                            idx = idx - 1 if idx != 0 else 0
                            tags[idx] = blank
                        elif cat == 'a':
                            op = raw_input("Are you sure you want to abort (left %i)? [y/n] > " % left)
                            if op.lower() == 'y': raise Exception("Abort")
                        else:
                            # Associate the category
                            if cat == 'i' and ( idx == 0 or not tags[idx-1].endswith('INV') ): bio = 'B-INV'
                            elif cat == 'i': bio = 'I-INV'
                            elif cat == 'e': bio = 'B-NEG'
                            else: bio = 'O    '
                            tags[idx] = bio
                            idx = idx + 1
                    
                    if cat == 'q':
                        break
                    if cat == 's':
                        left -= 1
                        continue
                            
                    # Once the text is tagged, add it to the result
                    tags = [ None if tag == 'B-NEG' else False if tag =='O' else True for tag in tags ]
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


