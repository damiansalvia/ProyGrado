 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

from ANN_LSTM import ANN as LSTM
import operator
import itertools
from utilities import *
import time 
import datetime

log = Log("./log")

grid = {
    'type': ['LSTM'], 
    'window': [10], 
    'testing_fraction': [0.2]
}


LSTM_SET_MODEL = ['hidden_leyers','metrics','loss','optimizer',
    'early_monitor','early_min_delta','early_patience','early_mode']

LSTM_FIT = ['testing_fraction', 'verbose', 'neg_as']

MODELS_DIR = './outputs/models'




class Model:

    def __init__(self, params):
        self.params = params
        self.ann = LSTM(self.params['window'])
        self.ann.set_model(**{ key:self.params[key] for key in self.params.keys() if key in LSTM_SET_MODEL })

    def fit(self):
        self.ann.fit_tagged(**{ key:self.params[key] for key in self.params.keys() if key in LSTM_FIT })

    def save(self):
        date = '{:%Y%m%d_%H-%M-%S}'.format(datetime.datetime.now())
        self.ann.save_model(self, date , odir=MODELS_DIR)
        name = 'model_' + date
        log("Saved model : %s -- %s " % (name, jsons.dumps(self.params) ), level='INFO')

scores = []
try:
    keys, values = zip(*grid.items())
    total = reduce(operator.mul, [ len(v) for v in values ], 1)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        iteration = int(sys.argv[1])
    else:
        iteration = 0
    for element in itertools.product(*values):
        iteration += 1
        params = dict(zip(keys,element))
        try:
            model = Model(params)
            scores = model.fit()
            model.save()
            scores += (params, scores)
        except Exception as e:
            time.sleep(2)
            log("There was an error on iteration %d: " % (iteration, str(e))  )

    print scores

except Exception as error:
    raise error