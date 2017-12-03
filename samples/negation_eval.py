import sys
sys.path.append('../src')

import itertools
from cldas.neg.model import NegScopeLSTM, NegScopeFFN
from cldas.utils.metrics import *
import cldas.db.crud as dp 
from cldas.db.crud import db

tagged   = dp.get_tagged(dp.TaggedType.MANUAL)
vec_size = len( dp.get_null_embedding() )
path = './neg/models/eval/'

params = {
    'window'   :[5, 8, 10, 20],
    'dimension':[vec_size],
    'layers'   :[[{'units':750, 'activation': 'relu', 'dropout': 0.2 }]],
    'metrics'  :[[binacc, precision, recall, fmeasure, mse, bce]],
    'loss'     :['binary_crossentropy'],
    'optimizer':['adam'],
    'verbose'  :[1]
}

keys = params.keys()
for par in itertools.product(*params.values()):
    lstm = NegScopeLSTM( **dict(zip(keys,par)))
    fname = "model_NegScopeLSTM_w%i.h5" % win
    X_train, Y_train = dp.get_lstm_dataset( tagged, win )
    lstm.fit( X_train, Y_train )  
    scores = dict(lstm.get_scores(X_train, Y_train, verbose=2))
    id = db.results.insert({'type': 'Negation', 'params': dict(zip(keys,par)),'scores': scores})
    lstm.save_model(fname, './neg/eval/models')



# params = {
#     'a': [1,2,3],
#     'b': ['a','b','c'],
#     'c': ['x','y','z'],
# }


    
    # def __init__(self, window, dimension, **kwargs):
    #     super(NegScopeLSTM,self).__init__(dimension,**kwargs)

    #         window    = 10, 
    #         dimension =
    #         layers    = [{'units':750, 'activation': 'relu', 'dropout': 0.2 }],
    #         metrics   = [binacc, precision, recall, fmeasure, mse, bce],
    #         loss      = 'binary_crossentropy', 
    #         optimizer = 'adam',
    #         verbose   = 2,
