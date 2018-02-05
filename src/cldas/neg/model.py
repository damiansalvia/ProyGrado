# -*- encoding: utf-8 -*-
'''
Module with a set of models for determining the scope negation 

@author: Nicolás Mechulam, Damián Salvia
'''

import os
import numpy as np

np.random.seed(666)
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from cldas.utils import Log, Level
from cldas.utils.metrics import *
from cldas.utils.visual import title

from keras.models import Sequential,load_model
from keras.layers import Dense,LSTM
from keras.layers.core import Dropout
from keras.callbacks import EarlyStopping


_DEFAULT_LAYER_SIZE = 750
_DEFAULT_DROPOUT    = 0.0
_DEFAULT_ACTIVATION = 'relu'

log = Log("./log")



class _NegScopeModel(object):
    '''
    Base class of negation scope models.
    '''
    
    def __init__(self, dimension,
            layers    = [{'units':750, 'activation': 'relu', 'dropout': 0.2 }],
            metrics   = [binacc, precision, recall, fmeasure, mse, bce],
            loss      = 'binary_crossentropy', 
            optimizer = 'adam',
            verbose   = 2,
        ):
        self._dimension = dimension 
        self._layers    = layers
        self._metrics   = metrics
        self._loss      = loss
        self._optimizer = optimizer
        self._verbose   = verbose
        
        print title("%s (%i)" % (self.__class__.__name__, self._dimension), width=61)
    
       
    def __repr__(self):
        return "< %s.%s - dim(%i) >" % (self.__class__.__module__, self.__class__.__name__, self._dimension)
    
    
    def __str__(self):
        return "%s" % self.__class__.__name__ 
    
    
    def save_model(self, filename, dirpath= './'):
        dirpath = dirpath if dirpath [-1] != "/" else dirpath[:-1]
        if not os.path.isdir(dirpath): 
            os.makedirs(dirpath)
        filename = filename+'.h5' if not filename.endswith('.h5') else filename
        self._model.save( dirpath+filename )
       
        
    def load_model(self, source):
        self._model = load_model(source , custom_objects={
            'binary_accuracy':binacc,
            'precision': precision,
            'recall':recall,
            'fmeasure':fmeasure,
            'mean_squared_error':mse,
            'binary_crossentropy':bce,
        })


    def fit(self, gen_XY, gen_XY_test=None, batch_size=512, early_monitor='val_binary_accuracy', verbose=1):
        
        callbacks = []
        if early_monitor:
            callbacks.append( EarlyStopping( monitor=early_monitor, min_delta=0, patience=2, mode='auto', verbose=0 ) )
                  
        self._model.fit_generator( gen_XY.get_iterator(), 
            callbacks=callbacks , 
            epochs=100 , 
            steps_per_epoch=len(gen_XY)/batch_size,
            validation_data=gen_XY_test.get_iterator(), 
            validation_steps=len(gen_XY_test)/batch_size,
            max_queue_size=5,
            verbose=verbose 
        )


    def predict(self, gen_X, verbose=2):
        Y = self._model.predict_generator( 
            gen_X.get_iterator(), 
            steps=1,
            max_queue_size=10,
            verbose=verbose
        )
        Y = np.array(Y).round() == 1 
        return Y


    def get_scores(self, gen_XY, verbose=2):
        scores = self._model.evaluate_generator( 
            gen_XY.get_iterator(), 
            steps=5,
            max_queue_size=5 
        )
        return zip( self._model.metrics_names , [ round(score*100,1) for score in scores ] )         

    

class NegScopeFFN(_NegScopeModel):
    '''
    Class of Feed-Forward Network model
    '''
    
    def __init__(self, window_left, window_right, dimension, **kwargs):
        super(NegScopeFFN,self).__init__(dimension,**kwargs)
    
        # Model definition     
        self._model = Sequential()
        
        # Input layer
        layer = self._layers[0]
        config = {
            'input_dim'  : self._dimension * (window_left + window_right + 1),
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
    '''
    Class of Long Short Term Memory model
    '''
    
    def __init__(self, window, dimension, **kwargs):
        super(NegScopeLSTM,self).__init__(dimension,**kwargs)
        
        # Model definition     
        self._model = Sequential()
        
        # Input layer
        layer = self._layers[0]
        config = {
            'input_shape'       : (window, self._dimension),
            'activation'        : layer.get('activation',_DEFAULT_ACTIVATION), 
            'dropout'           : layer.get('dropout', _DEFAULT_DROPOUT) ,  
            'use_bias'          : layer.get('bias',True),
            'recurrent_dropout' : layer.get('recurrent_dropout', 0.0),
            'return_sequences'  : len(self._layers[-1]) == 1
        }
        self._model.add( LSTM(layer.get('units',_DEFAULT_LAYER_SIZE), **config) )
        
        # Intermediate layers
        for idx,layer in enumerate(self._layers[1:]):
            config = {
                    'activation'        : layer.get('activation',_DEFAULT_ACTIVATION), 
                    'dropout'           : layer.get('dropout', _DEFAULT_DROPOUT) ,  
                    'use_bias'          : layer.get('bias',True),
                    'recurrent_dropout' : layer.get('recurrent_dropout', 0.0),
                    'return_sequences'  : len(self._layers[-1])-2 != idx 
            }
            self._model.add( LSTM(layer.get('units',_DEFAULT_LAYER_SIZE), **config) )
        
        # Output layer
        self._model.add( Dense( window, activation='sigmoid')  )
        
        # Compile model from parameters
        self._model.compile( loss=self._loss, optimizer=self._optimizer , metrics=self._metrics )
        
        # Print model
        if self._verbose != 0: print self._model.summary()



