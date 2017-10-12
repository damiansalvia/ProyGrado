# -*- encoding: utf-8 -*-
'''
Module with a set of models for determining the scope negation 
@author: Nicol�s Mechulam, Dami�n Salvia
'''

from cldas.utils import progress, save, Log
from cldas.utils.metrics import precision, recall, fmeasure, mse, bce, binacc
from cldas.neg import _DEFAULT_LAYER_SIZE, _DEFAULT_DROPOUT, _DEFAULT_ACTIVATION

from keras.models import Sequential,load_model
from keras.layers import Dense,LSTM
from keras.layers.core import Dropout
from keras.callbacks import EarlyStopping

import os
import numpy as np


_DEFAULT_LAYER_SIZE = 750
_DEFAULT_DROPOUT    = 0.0
_DEFAULT_ACTIVATION = 'relu'


np.random.seed(666)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


log = Log("../log")



class _NegScopeModel(object):
    
    def __init__(self, null_vec,
            layers    = [{'units':750, 'activation': 'relu', 'dropout': 0.2 }],
            metrics   = [binacc, precision, recall, fmeasure, mse, bce],
            loss      = 'binary_crossentropy', 
            optimizer = 'adam',
            verbose   = 2,
        ):
        self._vec_size = len( null_vec ) 
        self._layers   = layers
        self._verbose  = verbose
        self._metrics  = metrics
        self._loss     = loss
    
    
    def save_model(self, filename, dirpath= './'):
        dirpath = dirpath if dirpath [-1] != "/" else dirpath[:-1]
        if not os.path.isdir(dirpath): 
            os.makedirs(dirpath)
        self._model.save( dirpath+"/model_%s.h5" % filename )
       
        
    def load_model(self, source):
        self._model = load_model(source , custom_objects={
            'binary_accuracy':binacc,
            'precision': precision,
            'recall':recall,
            'fmeasure':fmeasure,
            'mean_squared_error':mse,
            'binary_crossentropy':bce,
        })
        
        
    def fit(self, X, Y, testing_fraction=0.2, early_monitor='val_binary_accuraty', verbose=0):
        
        callbacks = []
        if early_monitor:
            callbacks.append( EarlyStopping( monitor = early_monitor, min_delta = 0, patience = 2, mode = 'auto', verbose = 0 ) )
            
        self._model.fit( X, Y, 
            callbacks=callbacks , 
            batch_size=32 , epochs=100 , 
            validation_split=testing_fraction , 
            verbose=verbose 
        )

    
    def predict(self,X):
        Y = self._model.predict( X )
        Y = np.array(Y).flatten()
        Y = [ round(y) == 1 for y in Y.tolist() ] 
        return Y if len(Y) > 1 else Y[0]
    
    
    def get_scores(self, X, Y, verbose=2):
        scores = self._model.evaluate(X,Y,batch_size=10,verbose=verbose)
        return zip( self._model.metrics_names , [ round(score*100,1) for score in scores ] )        

    

class NegScopeFFN(_NegScopeModel):
    
    def __init__(self, window_left, window_right, **kwargs):
        super(NegScopeFFN,self).__init__(**kwargs)
    
        # Model definition     
        self._model = Sequential()
        
        # Input layer
        layer = self._layers[0]
        config = {
            'input_dim'  : self._vec_size * (window_left + window_right + 1),
            'activation' : layer.get('activation',_DEFAULT_ACTIVATION),
            'units'      : layer.get('units',_DEFAULT_LAYER_SIZE)
        }
        self._model.add( Dense( **config ) )
        self._model.add( Dropout( layer.get('dropout',_DEFAULT_DROPOUT) , seed=666 ) )
         
        # Intermediate layers
        for layer in self._layers[1:]:
            config = {
                'activation' : layer.get('activation',_DEFAULT_ACTIVATION),
                'units'      : layer.get('units',_DEFAULT_LAYER_SIZE)
            }
            self._model.add( Dense( **config ) )
            self._model.add( Dropout( layer.get('dropout',_DEFAULT_DROPOUT) , seed=666 ) )
         
        # Output layer
        self._model.add( Dense( 1, activation='sigmoid' ) )
        
        # Compile model from parameters
        self._model.compile( loss=self._loss, optimizer=self._optimizer , metrics=self._metrics )
        
        # Print model
        if self._verbose != 0: print self._model.summary()

    
    
class NegScopeLSTM(_NegScopeModel):
    
    def __init__(self, window, **kwargs):
        super(NegScopeFFN,self).__init__(**kwargs)
        
        # Model definition     
        self._model = Sequential()
        
        # Input layer
        layer = self._layers[0]
        config = {
            'input_shape'       : (window, self._vec_size),
            'activation'        : layer.get('activation',_DEFAULT_ACTIVATION), 
            'dropout'           : layer.get('dropout', _DEFAULT_DROPOUT) ,  
            'use_bias'          : layer.get('bias',True),
            'recurrent_dropout' : layer.get('recurrent_dropout', 0.0),
            'return_sequences'  : True
        }
        self._model.add( LSTM( **config ) )
        
        # Intermediate layers
        for layer in self._layers[1:]:
            config = {
                    'activation'        : layer.get('activation',_DEFAULT_ACTIVATION), 
                    'dropout'           : layer.get('dropout', _DEFAULT_DROPOUT) ,  
                    'use_bias'          : layer.get('bias',True),
                    'recurrent_dropout' : layer.get('recurrent_dropout', 0.0),
                    'return_sequences'  : True
            }
            self._model.add( LSTM(layer.get('units',_DEFAULT_LAYER_SIZE), **config) )
        
        # Output layer
        self._model.add( Dense( window, activation='sigmoid')  )
        
        # Compile model from parameters
        self._model.compile( loss=self._loss, optimizer=self._optimizer , metrics=self._metrics )
        
        # Print model
        if self._verbose != 0: print self._model.summary()



