# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *
from metrics import precision, recall, fmeasure, cosine, mse, bce, binacc

from keras.models import Sequential
from keras.layers import Dense
from keras.layers.core import Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import Bidirectional
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
# from keras.utils import plot_model

import DataProvider as dp 

import os, json, io, glob, re, md5
import numpy as np



np.random.seed(666)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")



sources = dp.get_sources()
sources_size = len(sources)



class NeuralNegationTagger:
     
    def __init__(self,
            wleft,
            wright,
            out_dims        = [750,500],
            activation      = ['relu','relu','sigmoid'],
            loss            = 'binary_crossentropy', 
            optimizer       = 'adam', 
            metrics         = [binacc, precision, recall, fmeasure, mse, bce],
            early_monitor   ='val_binary_accuracy',
            early_min_delta = 0,
            early_patience  = 2,
            early_mode      = 'auto',
            drop_rate       = [0.2,0.2],
        ):
        
        assert len(out_dims) == len(drop_rate)
        assert len(out_dims)+1 == len(activation)
                    
        # Parameters calculation
        vec_size  = dp.get_size_embedding()        
        input_dim = vec_size * (wright + wleft + 1)
        
        # Attributes settings
        self.wright = wright
        self.wleft  = wleft
        self.dim    = input_dim
        self.name   = "predict_l%i_r%i_%s_%s_o%s_e%s_d%s" % (
            wleft,
            wright,
            ''.join('d'+str(dim) for dim in out_dims),
            ''.join(act[0].upper() for act in activation),
            optimizer[0].upper(),
            "Y" if early_monitor else "N",
            "Y" if drop_rate else "N"
        )
        
        # Callbacks settings
        self.callbacks = []
        if early_monitor:
            self.callbacks.append(
                EarlyStopping(
                    monitor   = early_monitor,
                    min_delta = early_min_delta,
                    patience  = early_patience, 
                    mode      = early_mode,
                    verbose   = 0
                )
            )
        
        # Model definition     
        self.model = Sequential()
        
        # Input layer
        self.model.add( Dense( out_dims[0], input_dim=input_dim, activation=activation[0] ) )
        self.model.add( Dropout( drop_rate[0] , seed=666 ) )
         
        # Intermediate layers
        for i in range( 1 , len(out_dims) ):
            self.model.add( Dense( out_dims[i], activation=activation[i] ) )
            self.model.add( Dropout( drop_rate[i] , seed=666 ) ) 
         
        # Output layer
        self.model.add( Dense( 1, activation=activation[-1] ) )
        
        # Compile model from parameters
        self.model.compile( loss=loss, optimizer=optimizer , metrics=metrics )
        
        # Result
        log('MODEL ARQUITECTURE\n'+self.model.to_json(indent=4),level='info')
        print self.model.summary()
     
     
    def fit_tagged(self,testing_fraction=0.2,verbose=0):    
        opinions = dp.get_tagged('manually') 
        
        if not opinions: raise Exception('Nothing to train')
        
        X , Y = [] , []
        total = opinions.count()
        for idx,opinion in enumerate(opinions):
            progress("Getting embeddings",total,idx)
            x_curr,y_curr = dp.get_text_embeddings( opinion['text'], self.wleft, self.wright )
            X += x_curr
            Y += y_curr
        
        X = np.array(X)
        Y = np.array(Y)
        
        self.model.fit( X, Y, 
            callbacks=self.callbacks , 
            batch_size=32 , epochs=100 , 
            validation_split=testing_fraction , 
            verbose=verbose 
        )
        
        scores = self.model.evaluate(X,Y,batch_size=32,verbose=verbose)
        scores = [ round(score*100,1) for score in scores ]
        scores = zip( self.model.metrics_names , scores )
        log('MODEL EVALUATION\n'+str(scores),level='info')
        print        
        for metric,score in scores: print "%-20s: %.1f%%" % ( metric, score )
        print "_________________________________________________________________"
        return scores
            
    
    def predict_untagged(self,limit=None,tofile=None):
        opinions = dp.get_untagged(limit,666)
        results = {}
        total = opinions.count(with_limit_and_skip=True)
        print 'limit =',limit,", total =",total;raw_input()
        for idx,opinion in enumerate(opinions): 
            progress("Predicting on new data",total,idx)
            results[ opinion['_id'] ] = []
            for X in dp.get_text_embeddings( opinion['text'], self.wleft, self.wright )[0]:
                X = X.reshape((1, -1))
                Y = self.model.predict( X )
                Y = ( round(Y) == 1 ) # 0 <= Y <= 1 -- Round is ok?
                results[ opinion['_id'] ].append( Y ) 
        if tofile: save(results,"%s" % self.name,tofile)
        #dp.save_negation(result,tagged_as='automatically')
        return results
    
     
    def save(self,odir = './outputs/models'):
        odir = odir if odir[-1] != "/" else odir[:-1]
        if not os.path.isdir(odir): os.makedirs(odir)
        self.model.save( odir+"/model_%s.h5" % self.name )
#         plot_model( self.model, to_file=odir+'/model_neg_l%i_r%i_d%i.png' % (self.left,self.right,self.dim) , show_shapes=True )    



def load_corpus_negation(sources='../../corpus/corpus_variado_sfu_neg/*/*.xml'):
    sources = glob.glob(sources)
    total = len(sources)
    isneg, tmpisneg = False, None
    opinions = []
    
    for idx,source in enumerate(sources):
        
        progress("Reading negation corpus_variado_sfu (%s)" % source.split('/')[-2],total,idx) 
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
                else: # mathsign, solo tiene POS
                    continue                       
                
                if not tag:
                    tag   = "cs"
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
                'word'   : token['form'],
                'lemma'  : token['lemma'],
                'tag'    : token['tag'],
                'negated': token['negated']
            } for token in tokens ]
            opinions.append(opinion)
    
    dp.save_opinions(opinions) 
    return len(opinions)
    
    

def start_tagging(tofile=None):
    
    def DisplayMenu():
        os.system('clear')
        title("MENU")
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
                quit = False
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
                content = json.dumps(result,indent=4,ensure_ascii=False)
                log("Reason : %s (at %s) [%i] '%s'" % ( str(e) , source , sample['idx'] , content ))
                raw_input("Reason: %s\nEnter to continue..." % str(e))
    
  
    
def load_neg_from_files(source_dir):
    sources = glob.glob(source_dir)
    total = len(sources)
    for idx,source in enumerate(sources):
        progress("Load negation tags from %s" % source,total,idx)
        content = json.load( open(source) )    
        dp.save_negations(content,tagged_as='manually')        
        

def nprint(file):
    tags = json.load(open(file))
    for _id in tags:
        opinion = dp.get_opinion(_id)
        print ' '.join(["%s" % ("\033[91m"+wd+"\033[0m" if tg else wd) for wd,tg in zip([text['word'] for text in opinion['text']],tags[_id]) ])
        raw_input("Next...")
        
        
        
if __name__ == '__main__':
#     load_neg_from_files('./outputs/negation/negtag_*.json')
    load_corpus_negation()
    