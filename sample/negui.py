# -*- encoding: utf-8 -*-
'''
Example of how to use interactive negation by command-line interface
@author: Nicolás Mechulam, Damián Salvia
'''
import sys
sys.path.append('../src')

from cldas.neg.model import NegScopeLSTM
from cldas.neg.interface import interactive_prediction, manual_tagging
import cldas.db.crud as dp

'''
---------------------------------------------
    Use interactive negation prediction
---------------------------------------------
'''

win = 10
dim = 300

lstm = NegScopeLSTM( win, dim )
lstm.load_model('../sample/neg/models/model_NegScopeLSTM_w10.h5')

interactive_prediction( lstm , dp.get_lstm_dataset, win=win )

'''
---------------------------------------------
    Manual tagging of corporea
---------------------------------------------
'''
path='./neg/manual'

manual_tagging(dp,tofile=path)

dp.save_negations_from_files(path+'/*')

