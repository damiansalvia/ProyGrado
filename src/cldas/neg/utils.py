# -*- encoding: utf-8 -*-
'''
Module with negation utilities
@author: Nicolás Mechulam, Damián Salvia
'''

import glob, os, re
from cldas.utils import progress, save, title, Log, load


log = Log("../log")
  
      
def load_neg_from_files(source_dir,verbose=True):
    sources = glob.glob(source_dir)
    total = len(sources)
    for idx,source in enumerate(sources):
        if verbose: progress("Load negation tags from %s" % source,total,idx)
        content = load(source)   
        yield content 
#         dp.save_negations(content,tagged_as='manually') 


def load_corpus_negation(sources='../../corpus/corpus_variado_sfu_neg/*/*.xml',verbose=False,tofile=None):
    sources = glob.glob(sources)
    total = len(sources)
    isneg, tmpisneg = False, None
    opinions = []
    
    for idx,source in enumerate(sources):
        
        if verbose: progress("Reading negation (%s)" % source.split('/')[-2],total,idx) 
        lines = open(source).readlines()
        tokens = []
        text = ""
        for line in lines:
            content = line.strip()
            if not isinstance(content,unicode):
                content = unicode(content,'utf8')            
            
            if content.startswith("<?xml"):
                regex = re.compile("polarity=\"(.*?)\"",re.DOTALL)
                category = regex.findall(content)[0]
                category = 20 if category=='negative' else 80
                continue
            
            elif content.startswith("<scope"):
                isneg = True
                continue               
                
            elif content.startswith("</scope"):
                isneg = False
                continue
            
            elif content.startswith("<negexp"):
                tmpisneg = isneg
                isneg = None
                continue               
                
            elif content.startswith("</negexp"):
                isneg = tmpisneg
                tmpisneg = None
                continue
            
            elif content.startswith("<v ") or\
                content.startswith("<s ") or\
                content.startswith("<f ") or\
                content.startswith("<p ") or\
                content.startswith("<r ") or\
                content.startswith("<a ") or\
                content.startswith("<d ") or\
                content.startswith("<c ") or\
                content.startswith("<n ") or\
                content.startswith("<w ") or\
                content.startswith("<z ") or\
                content.startswith("<i "):
                   
                forms = re.compile("wd=\"(.*?)\"",re.DOTALL).findall(content)
                lemma = re.compile("lem=\"(.*?)\"",re.DOTALL).findall(content)
                tag   = re.compile("pos=\"(.*?)\"",re.DOTALL).findall(content)
                
                if forms and lemma:
                    forms = forms[0]
                    lemma = lemma[0]
                elif lemma: 
                    forms = lemma[0]
                    lemma = lemma[0]
                else: # is mathsign, only has POS-tag
                    continue                       
                
                if not tag:
                    tag   = "CS"
                else:
                    tag = tag[0]
                
                forms = forms.split('_') if not tag.startswith("NP") else forms
                
                for form in forms:  
                    tokens.append({
                        'form':form,
                        'lemma':lemma,
                        'tag':tag.upper(),
                        'negated': isneg,
                    })    
                    
                    text += " "+form
            else: # Casos raros como &gt;
                pass
                
        _id = md5.new(str(category) + text.encode('ascii', 'ignore')).hexdigest()
        
        if not dp.get_opinion(_id):
            opinion = {}         
            opinion['_id']      = _id
            opinion['category'] = category
            opinion['idx']      = idx+1
            opinion['source']   = 'corpus_variado_sfu'
            opinion['tagged']   = 'manually',
            opinion['text']     = [{
                'word'   : token['form'].lower(),
                'lemma'  : token['lemma'].lower(),
                'tag'    : token['tag'],
                'negated': token['negated']
            } for token in tokens ]
            opinions.append(opinion)
    
    dp.save_opinions(opinions) 
    
    if tofile: save(opinions,"from_corpus_sfu_negation",tofile)
    
    return len(opinions)


def manual_tagging(sources, tofile=None):
    
    sources_size = len( sources )
    
    def DisplayMenu():
        os.system('clear')
        title("MENU")
        print "0 . exit"
        for i in range(sources):
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
        if tofile:save(result,"negtag_%s" % source,tofile,overwrite=False)
        
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
        if op > sources_size:
            raw_input("Opcion invalida")
            continue
        else:    
            result = {}        
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
                        tooltip += "Enter A(bort), B(ack) S(kip), Q(uit) or <intro> for "
                        tooltip += "repeating last action (%s) > " % (cat.upper() if cat else "None")
                        tag = raw_input(tooltip)
                        
                        if not tag and not cat: # Prevents parse empty cat
                            print "Input a category first";raw_input()
                            continue
                        elif tag:
                            cat = tag
                        
                        # Action from decision
                        cat = cat.lower()
                        if not cat or cat not in 'nibasq':
                            print "Option",cat,"is not correct." ;raw_input()
                            continue
                        if cat == 'q':
                            break
                        if cat == 's':
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
                content = '\n'.join([ _id+">>"+str(tags) for _id,tags in result.items() ])
                log("Reason : %s (at %s) [%i] '%s'" % ( str(e) , source , sample['idx'] , content ))
                raw_input("Reason: %s\nEnter to continue..." % str(e))


