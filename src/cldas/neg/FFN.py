# -*- encoding: utf-8 -*-
'''
Module for determining scope negation by using a Feed Forward Network (FFN) 
@author: Nicolás Mechulam, Damián Salvia
'''

from cldas.utils import progress, save, Log
from cldas.utils.metrics import precision, recall, fmeasure, mse, bce, binacc

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers.core import Dropout
from keras.callbacks import EarlyStopping

import os
import numpy as np


np.random.seed(666)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


log = Log("../log")


class NegScopeFFN:
    '''
    Feed Forward Neural Network for determining negation scope
    '''
    
    def __init__(self, wleft, wright):
                    
        # Parameters calculation
        vec_size  = dp.get_size_embedding()        
        input_dim = vec_size * (wright + wleft + 1)
        
        # Attributes settings
        self.wright    = wright
        self.wleft     = wleft
        self.dimension = input_dim
        self.model     = None
    
    
    def save_model(self,name,path= '../../outputs/models'):
        path = path if path [-1] != "/" else path[:-1]
        if not os.path.isdir(path): 
            os.makedirs(path)
        self.model.save( path+"/model_%s.h5" % name )
        
    
    def load_model(self,source):
        self.model = load_model(source , custom_objects={
            'binary_accuracy':binacc,
            'precision': precision,
            'recall':recall,
            'fmeasure':fmeasure,
            'mean_squared_error':mse,
            'binary_crossentropy':bce,
        })
    
    
    def set_model(self,
            out_dims        = [750,500],
            activation      = ['relu','relu','sigmoid'],
            loss            = 'binary_crossentropy', 
            optimizer       = 'adam', 
            metrics         = [binacc, precision, recall, fmeasure, mse, bce],
            early_monitor   ='val_binary_accuracy',
            drop_rate       = [0.2,0.2],
        ):
        
        assert len(out_dims) == len(drop_rate)
        assert len(out_dims)+1 == len(activation)
        
        # Model definition     
        self.model = Sequential()
        
        # Input layer
        self.model.add( Dense( out_dims[0], input_dim=self.dimension, activation=activation[0] ) )
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
     
     
    def fit_tagged(self,neg_as,testing_fraction=0.2,verbose=0,early_monitor='val_binary_accuraty',limit=None):    
        opinions = dp.get_tagged('manually')
        if limit: # Only for testing
            opinions = opinions.limit(limit)
        total = opinions.count(with_limit_and_skip=True)       
        if total == 0: raise Exception('Nothing to train')
                
        callbacks = []
        if early_monitor:
            callbacks.append(
                EarlyStopping(
                    monitor   = early_monitor,
                    min_delta = 0,
                    patience  = 2, 
                    mode      = 'auto',
                    verbose   = 0
                )
            )
        
        X , Y = [] , []
        for idx,opinion in enumerate(opinions):
            progress("Getting embeddings for trainning (%i words)"  % len(opinion['text']),total,idx)
            x_curr,y_curr = dp.get_text_embeddings( opinion['text'], self.wleft, self.wright ,neg_as=neg_as )
            X += x_curr
            Y += y_curr         
        X = np.array(X)
        Y = np.array(Y)   
        
        self.model.fit( X, Y, 
            callbacks=callbacks , 
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
        for idx,opinion in enumerate(opinions): 
            progress("Predicting on new data",total,idx)
            results[ opinion['_id'] ] = []
            for X in dp.get_text_embeddings( opinion['text'], self.wleft, self.wright )[0]:
                X = X.reshape((1, -1))
                Y = self.model.predict( X )
                Y = ( round(Y) == 1 ) # 0 <= Y <= 1 -- Round is ok?
                results[ opinion['_id'] ].append( Y ) 
        if tofile: save(results,"prediction",tofile,overwrite=False)
        #dp.save_negation(result,tagged_as='automatically')
        return results   
    
    
    def input_guess(self):
        
        from analyzer import Analyzer
        from CorpusReader import review_correction
        an = Analyzer()
        
        while True:
#             try:
                
            os.system('clear')
            print '\n\033[4mYOUR SENTENCE\033[0m'
            sentence = raw_input("> ")
            if not sentence: # exit
                os.system('clear') ; break
            sentence = review_correction(sentence)
            analized_sentence = an.analyze(sentence)
            analized_sentence = [ {'word': item['form']} for item in analized_sentence ]
            
            result = []
            for X in dp.get_text_embeddings( analized_sentence , self.wleft , self.wright )[0]:
                X = X.reshape((1, -1))
                Y = self.model.predict( X )
                Y = ( round(Y) == 1 )
                result.append( Y )
            
            os.system('clear') 
            print '\n\033[4mPREDICTION RESULT\033[0m'        
            print '>',' '.join([
                "%s" % ("\033[91m"+wd+"\033[0m" if tg else wd) 
                for wd,tg in zip( [text['word'] for text in analized_sentence] , result ) 
            ])
            
#             except Exception as e:
#                 print 'An error has ocurred during processing (',str(e),")"
                  
            raw_input("\nPress enter to continue...")

