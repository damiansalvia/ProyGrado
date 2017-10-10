# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')

from utilities import *

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping,CSVLogger
from metrics import precision, recall, fmeasure, mse, bce, binacc

from InteractiveNegator import get_params, start_evaluator, new_model, get_window

import DataProvider as dp 

import os
import numpy as np


np.random.seed(005)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")

DEFAULT_LAYER_SIZE = 750
DEFAULT_DROPOUT    = 0.2
DEFAUTL_ACTIVATION = 'relu'

sources = dp.get_sources()
sources_size = len(sources)


class ANN:
     
    def __init__(self, window):

        # Parameters calculation
        self.vec_size  = dp.get_size_embedding()    
        self.window = window    
        self.end_vecotr = np.array(dp.get_word_embedding('.'))

        
    def save_model(self,oname,odir = './outputs/models'):
        odir = odir if odir[-1] != "/" else odir[:-1]
        if not os.path.isdir(odir): os.makedirs(odir)
        self.model.save( odir+"/model_%s.h5" % oname )
        
    
    def load_model(self,source):
        self.model = load_model(source , custom_objects={
            'binary_accuracy':binacc,
            'precision': precision,
            'recall':recall,
            'fmeasure':fmeasure,
            'mean_squared_error':mse,
            'binary_crossentropy':bce,
        })
    
    # LEYER DEFINITION:
    # {
    #     'units'            : <Int>, 
    #     'activation'       : <String>,
    #     'dropout'          : <Double>,
    #     'bias'             : <Boolean>,
    #     'recurrent_dropout': <Double>
    # }
    def set_model( self,
            hidden_leyers   = [{'units':750, 'activation': 'relu', 'dropout': 0.2 }],
            metrics         = [binacc, precision, recall, fmeasure, mse, bce],
            loss            = 'binary_crossentropy', 
            optimizer       = 'adam', 
            early_monitor   = 'val_binary_accuracy',
            early_min_delta =  0,
            early_patience  =  2,
            early_mode      = 'auto',
            verbose         = 2,
        ):
        
        # Callbacks settings
        self.callbacks = []
        self.callbacks.append(
            EarlyStopping(
                monitor   = early_monitor,
                min_delta = early_min_delta,
                patience  = early_patience, 
                mode      = early_mode,
                verbose   = 0,
            )
        )
        self.callbacks.append(
            CSVLogger('./log/training.log')
        )
        
        # Model definition     
        self.model = Sequential()

        for idx,layer in enumerate(hidden_leyers):
            conf = {
                    'activation'        : layer.get('activation',DEFAUTL_ACTIVATION), 
                    'dropout'           : layer.get('dropout', DEFAULT_DROPOUT) ,  
                    'use_bias'          : layer.get('bias',True),
                    'recurrent_dropout' : layer.get('recurrent_dropout', 0.0),
                    'return_sequences'  : idx == len(hidden_leyers)
            }
            if idx != len(hidden_leyers) -1:
                conf['return_sequences']  = True
            if idx == 0:
                conf['input_shape'] = (self.window, self.vec_size)
            self.model.add( 
                LSTM(layer.get('units',DEFAULT_LAYER_SIZE), **conf)
            )
        
        # Output layer
        self.model.add( Dense( self.window, activation='sigmoid') )
        
        # Compile model from parameters
        self.model.compile( loss=loss, 
            optimizer='adam',  
            metrics=metrics
        )

        # Result
        log('MODEL ARQUITECTURE\n'+self.model.to_json(indent=4),level='info')
        if verbose != 0:
            print self.model.summary()
     

    def fit_tagged(self,testing_fraction=0.2, verbose=2, neg_as=False):    
        
        opinions = dp.get_tagged('manually') 
        if not opinions: raise Exception('Nothing to train')
        
        X , Y = [] , []
        total = opinions.count(with_limit_and_skip=True)
        for idx,opinion in enumerate(opinions):
            progress("Loading training data",total,idx)
            x_curr,y_curr = self.format_opinion(opinion['text'], neg_as)
            X += x_curr
            Y += y_curr
        self.fit(X,Y, testing_fraction, verbose)
        scores = self.get_scores(X,Y,verbose)
        if verbose != 0:
            log('MODEL EVALUATION\n'+str(scores),level='info')
            print        
            for metric,score in scores: print "%-20s: %.1f%%" % ( metric, score )
            print "_________________________________________________________________"
        return scores
        

    def get_scores(self, X,Y, verbose=2):
        scores = self.model.evaluate(X,Y,batch_size=10,verbose=verbose)
        return zip( self.model.metrics_names , [ round(score*100,1) for score in scores ] )
         

    def format_opinion(self, opinion, neg_as=False):
        x_curr = [np.array(dp.get_word_embedding(token['word'])) for token in opinion ]
        y_curr = [token.get('negated') if token.get('negated') is not None else neg_as for token in opinion ]
        rest = self.window - len(x_curr) % self.window 
        if rest > 0:
            x_curr.extend([self.end_vecotr for i in range(rest)])
            y_curr.extend([False for i in range(rest)]) 
        X = [ x_curr[i*self.window : (i+1)*self.window] for i in range(len(x_curr)/self.window) ]
        Y = [ y_curr[i*self.window : (i+1)*self.window] for i in range(len(y_curr)/self.window) ]
        return X,Y

    def fit(self, X,Y, testing_fraction=0.2, verbose=2):
        X = np.array(X)
        Y = np.array(Y)
        self.model.fit( X , Y , 
            callbacks=self.callbacks , 
            verbose=verbose,
            epochs=100 , 
            validation_split=testing_fraction
        )
    
    def predict_untagged(self,tofile=None,limit=None):
        opinions = list( dp.get_untagged(limit=limit) )
        results = {}
        total = len(opinions)#opinions.count(with_limit_and_skip=True)
        for idx,opinion in enumerate(opinions): 
            
            progress("Predicting on new data (%i words)" % len(opinion['text']),total,idx)
            x_curr = [np.array(dp.get_word_embedding(token['word'])) for token in opinion['text'] ]
            rest = self.window - len(x_curr) % self.window 
            if rest > 0:
                x_curr.extend([self.end_vecotr for i in range(rest)])

            X = np.array([ x_curr[i*self.window : (i+1)*self.window] for i in range(len(x_curr)/self.window) ])
            try :            
                Y = self.model.predict( X ).flatten()
            except:
                print 'ERROR'
            results[ opinion['_id'] ] =  [ round(y) == 1 for y in Y.tolist()[:len(opinion['text'])] ]
            
            if idx % 500 == 0: # partial dump
                dp.save_negations(results,tagged_as='automatically')
                result = {}
                
        if tofile: save(results,"predict_untagged_LMST_window_%i" % (self.window),tofile)
        dp.save_negations(results,tagged_as='automatically')
        return results
    
    def predict_opinion(self, opinion):
        x =  [np.array(dp.get_word_embedding(token)) for token in opinion ]
        rest = self.window - len(x) % self.window 
        if rest > 0:
            x.extend([self.end_vecotr for i in range(rest)])
        X = np.array([ x[i*self.window : (i+1)*self.window] for i in range(len(x)/self.window) ])
        Y = self.model.predict( X ).flatten()
        return [ round(y) == 1 for y in Y.tolist()[:len(opinion)] ]
        
        
if __name__ == '__main__':
    if new_model():
        window, config = get_params('mono')
        ann = ANN(window)
        ann.set_model(**config)
        ann.fit_tagged( testing_fraction=0.20 , verbose=1 )
        ann.save_model("LSTM")
    else:
        ann = ANN(get_window())
        ann.load_model('./outputs/models/model_LSTM.h5')

    start_evaluator(ann.predict_opinion)
    if raw_input("Predict all? > "):
        import time
        start_time = time.time()
        ann.predict_untagged(tofile="./outputs/tmp")
        elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
        log( "LSTM predict - Elapsed: %s" % elapsed , level="INFO")
        print "LSTM predict - Elapsed time: %s" % elapsed
        