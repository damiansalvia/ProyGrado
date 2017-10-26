# -*- encoding: utf-8 -*-
'''
Example of how evaluate a lexicon.
@author: Nicolás Mechulam, Damián Salvia
'''

import sys
sys.path.append('../src')

import time

from cldas.evaluator import evaluate
from cldas.utils.misc import Iterable
from cldas.utils.file import save
from cldas.utils import USEFUL_TAGS
from cldas.morpho import Preprocess

from cldas.utils.logger import Log, Level
log = Log('./')

import cldas.db.crud as dp



'''
---------------------------------------------
      Retrieval stage
---------------------------------------------
'''
start_time = time.time()

from cldas.retrieval import CorpusReader


# ---------------------------------------------
#       Get general lexicon
# ---------------------------------------------
reader = CorpusReader( 
    '../genlex', 
    'ElhPolar_esV1.lex.txt', 
    op_pattern='(.*?)\t.*?\n', 
    file_pattern='\t(negative|positive)\n', 
    start_from=35
)
general_lexicon = { item['text']: item['category'] for item in reader.data( mapping= {'negative': -1, 'positive': 1 } )}

# ---------------------------------------------
#       Get Testing Corpus
# ---------------------------------------------
reader = CorpusReader( 
    '../corpus/corpus_cine_mvdcomm', 
    '*.csv', 
    op_pattern=r';([^;]*);\d;\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\s', 
    file_pattern=r';(\d);\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+\s', 
    start_from=2
)
testing_corpus = reader.data(mapping = {'0': -1, '1': -1, '2': -1, '3': 1, '4': 1, '5': 1 } )
preproc = Preprocess( 'testing', testing_corpus )
untagged = preproc.data()


from cldas.neg.model import NegScopeLSTM, NegScopeFFN

win = 10
vec_size = len( dp.get_null_embedding() )
lstm = NegScopeLSTM( win, vec_size )
 
fname = "model_NegScopeLSTM_w%i.h5" % win
lstm.load_model(path+fname)
negations = {} ; total = len( untagged )
for idx,opinion in enumerate(untagged):
    progress("Predicting on new data",total,idx)
    X_pred ,_ = dp.get_lstm_dataset( [opinion], win , verbose=False)
    Y_pred = lstm.predict( X_pred )
    Y_pred = Y_pred.flatten().tolist()[: len( opinion['text'] ) ] # Only necessary with LSTM
    negations[ opinion['_id'] ] = Y_pred 

evaluate(general_lexicon,testing_corpus)


elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Retrieval stage - Elapsed: %s" % elapsed , level=Level.DEBUG)

