# -*- encoding: utf-8 -*-
'''
Example of how to use negation manual tagging by command-line
@author: Nicolás Mechulam, Damián Salvia
'''
import sys
sys.path.append('../src')

from cldas.neg.model import NegScopeLSTM
from cldas.neg.interface import interactive_prediction, manual_tagging
import cldas.db.crud as dp

'''
---------------------------------------------
    Manual tagging of corporea
---------------------------------------------
'''
path='./neg/manual'

manual_tagging(dp,tofile=path)

dp.save_negations_from_files(path+'/*')

