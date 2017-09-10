# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *

import numpy as np
import DataProvider as dp 

def data_train(wleft,wright,limit=None,seed=None,neg_as=None):
    opinions = dp.get_tagged('manually',limit,seed)
    if not opinions: 
        raise Exception('No data available')
    X , Y = [] , []
    total = opinions.count()
    for idx,opinion in enumerate(opinions):
        progress("Training data (%i words)"  % len(opinion['text']),total,idx)
        x_curr,y_curr = dp.get_text_embeddings( opinion['text'], wleft, wright , neg_as=neg_as )
        X += x_curr
        Y += y_curr       
    X = np.array(X)
    Y = np.array(Y)
    return X, Y

def data_pred(wleft,wright,limit=None,seed=None):
    opinions = dp.get_untagged(limit,seed)
    results = {}
    total = opinions.count(with_limit_and_skip=True)
    for idx,opinion in enumerate(opinions): 
        progress("Predicting data (%i words)" % len(opinion['text']),total,idx)
        for x_curr in dp.get_text_embeddings( opinion['text'], wleft, wright ):
            x_curr = x_curr.reshape((1, -1))
            X.append( ( opinion['_id'] , x_curr ) )
    X = np.array(X)
    import pdb;pdb_set_trace()
    return X
