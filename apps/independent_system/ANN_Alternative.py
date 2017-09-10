# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *

from keras.models import Sequential
from keras.layers import Dense
from keras.layers.core import Dropout
from keras.callbacks import EarlyStopping,CSVLogger

import DataProvider as dp 

import os
import numpy as np



np.random.seed(005)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

tmp = os.popen('stty size', 'r').read().split()
WIDTH = int(tmp[1])-15 if tmp else 100

log = Log("./log")



sources = dp.get_sources()
sources_size = len(sources)


class ANN:
     
    def __init__(self,
            win_left,
            win_right,
            layers_dims     = [750,500],
            activation      = ['relu','relu','sigmoid'],
            loss            = 'binary_crossentropy', 
            optimizer       = 'adam', 
            early_monitor   ='val_acc',
            early_min_delta = 0,
            early_patience  = 2,
            early_mode      = 'auto',
            drop_rate       = [0.2,0.0],
        ):
        
        assert len(layers_dims) == len(drop_rate)
        assert len(layers_dims)+1 == len(activation)
                    
        # Parameters calculation
        vec_size  = dp.get_size_embedding()        
        input_dim = (vec_size + 1) * (win_right + win_left + 1) - 1
        
        # Attributes settings
        self.right = win_right
        self.left  = win_left
        self.dim   = input_dim
        
        # Callbacks settings
        self.callbacks = []
        self.callbacks.append(
            EarlyStopping(
                monitor   = early_monitor,
                min_delta = early_min_delta,
                patience  = early_patience, 
                mode      = early_mode,
                verbose   = 0
            )
        )
        self.callbacks.append(
            CSVLogger('./log/training.log')
        )
        
        # Model definition     
        self.model = Sequential()
        
        # Input layer
        self.model.add( Dense( layers_dims[0], input_dim=input_dim, activation=activation[0] ) )
        self.model.add( Dropout( drop_rate[0] ) )
        
        # Intermediate layers
        for i in range( 1 , len(layers_dims) ):
            self.model.add( Dense( layers_dims[i], activation=activation[i] ) )
            self.model.add( Dropout( drop_rate[i] ) ) 
        
        # Output layer
        self.model.add( Dense( 1, activation=activation[-1] ) )
        
        # Compile model from parameters
        self.model.compile( loss=loss, optimizer=optimizer )
        
        # Result
        log('MODEL ARQUITECTURE\n'+self.model.to_json(indent=4),level='info')
        print self.model.summary()
     
     
    def fit_tagged(self,testing_fraction=0.2,verbose=0):    
        opinions = dp.get_tagged('manually') 
        
        if not opinions: raise Exception('Nothing to train')
        
        X , Y = [] , []
        total = len(opinions)
        for idx,opinion in enumerate(opinions):
            progress("Loading training data",total,idx)
            x_curr,y_curr = dp.get_text_embeddings( opinion['text'], self.left, self.right )

            for idx in range(len(x_curr)):
                x_curr[idx].extend(y_curr[max(0, idx - self.win_left) : , idx ])
                x_curr[idx].extend(y_curr[idx + 1 : min(len(x_curr) - 1, idx + self.win_right + 1) ])


            X += x_curr
            Y += y_curr
        
        X = np.array(X)
        Y = np.array(Y)
        self.model.fit( X , Y , callbacks=self.callbacks , verbose=verbose )
            
    
    def predict_untagged(self,tofile=None):
        opinions = dp.get_untagged()
        results = {}
        total = len(opinions)
        for idx,opinion in enumerate(opinions): 
            progress("Predicting on new data",total,idx)
            results[ opinion['_id'] ] = []
            for X in dp.get_text_embeddings( opinion['text'], self.left, self.right )[0]:
                X = X.reshape((1, -1))
                Y = self.model.predict( X )
                Y = ( round(Y) == 1 ) # 0 <= Y <= 1 -- Round is ok?
                results[ opinion['_id'] ].append( Y ) 
        if tofile: save(results,"predict_untagged_l%i_r%i_d%i" % (self.left,self.right,self.dim),tofile)
        return results
    
     
    def save(self,odir = './outputs/models'):
        odir = odir if odir[-1] != "/" else odir[:-1]
        if not os.path.isdir(odir): os.makedirs(odir)
        self.model.save( odir+"/model_neg_l%i_r%i_d%i.h5" % (self.left,self.right,self.dim) )
#         plot_model( self.model, to_file=odir+'/model_neg_l%i_r%i_d%i.png' % (self.left,self.right,self.dim) , show_shapes=True )    

        
        
if __name__ == '__main__':
    ann = NeuralNegationTagger( 3 , 1 )     
    ann.fit_tagged( testing_fraction=0.20 , verbose=1 )
    ann.predict_untagged( tofile="./outputs/tmp" )   
        