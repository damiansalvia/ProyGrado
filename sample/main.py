# -*- encoding: utf-8 -*-
'''
Example of a complete execution
@author: Nicolás Mechulam, Damián Salvia
'''

import sys
sys.path.append('../src')

import time, os

from cldas.utils import USEFUL_TAGS
from cldas.utils.misc import Iterable
from cldas.utils.file import save
from cldas.utils.visual import progress

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
 
corporea = []

if not dp.get_opinions(source='corpus_apps_android'): 
    reader = CorpusReader( '../corpus/corpus_apps_android', '*/*.json', op_pattern='\"(.*?)\"[,(?:\\r\\n)]', path_pattern='(neg|pos)/', decoding='unicode-escape' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = {'neg': 20, 'pos': 80 }
    corporea.append( ( reader, mapping) )

if not dp.get_opinions(source='corpus_tweets'):  
    reader  = CorpusReader( '../corpus/corpus_tweets', '*.tsv', op_pattern='\d\t\d\t(.*?)\t.*?\n', file_pattern='(\d\t\d)\t.*?\n', start_from=1 )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { '3\t1': 10,  '3\t2': 20, '2\t4': 90, '2\t2': 70, '2\t3': 60, '4\t2': 30, '2\t1': 80, '5\t1': 40, '1\t5': 50, '1\t4': 30, '4\t1': 50, '1\t1': 40, '1\t3': 60, '1\t2': 70 }
    corporea.append( ( reader, mapping) )

if not dp.get_opinions(source='corpus_tweets_2'):  
    reader = CorpusReader( '../corpus/corpus_tweets_2', '*.csv', op_pattern='\"(.*?)\",', file_pattern='(N|P|NEU|NONE)(?:\\s|$)', start_from=1 )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { 'N':0, 'NEU' :50, 'NONE':50, 'P':100 }
    corporea.append( ( reader, mapping) )
 
if not dp.get_opinions(source='corpus_prensa_uy'): 
    reader = CorpusReader( '../corpus/corpus_prensa_uy', 'train.csv', op_pattern='/(.*(?!TRUE|FALSE)),[^ ]/g', file_pattern=',(Neg|Neu|Pos)\n' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { 'Neg': 0, 'Neu': 50, 'Pos': 100 }
    corporea.append( ( reader, mapping) )
    
if not dp.get_opinions(source='corpus_emotiblog'):  
    reader = CorpusReader( '../corpus/corpus_emotiblog', '*.xml', op_pattern='/<phrase.*?polarity=\".*?\".*?>(.*?)<\/phrase>/g', file_pattern='/<phrase.*?polarity=\"(.*?)\".*?>.*?<\/phrase>/g', decoding='cp1252')
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { 'negative': 0, '': 50, 'positive': 100 }
    corporea.append( ( reader, mapping) )

if not dp.get_opinions(source='corpus_hoteles'): 
    reader = CorpusReader( '../corpus/corpus_hoteles', '*.xml', op_pattern='<coah:review>(.*?)</coah:review>', file_pattern='<coah:rank>([1-5])<\/coah:rank>' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { '1': 0, '2': 25, '3': 50, '4': 75, '5': 100 }
    corporea.append( ( reader, mapping) )
    
if not dp.get_opinions(source='corpus_restaurantes'): 
    reader = CorpusReader( '../corpus/corpus_restaurantes', '*/*.json', op_pattern='\"(.*?)\"[,\\n]', path_pattern='(neg|pos)/', decoding='unicode-escape' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = {'neg': 20, 'pos': 80 }
    corporea.append( ( reader, mapping) )
 
if not dp.get_opinions(source='corpus_cine'):
    reader = CorpusReader( '../corpus/corpus_cine', '*.xml', op_pattern='<body>(.*?)</body>', file_pattern='rank=\"([1-5])\"', decoding='cp1252' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { '1': 0, '2': 25, '3': 50, '4': 75, '5': 100 }
    corporea.append( ( reader, mapping) )
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Retrieval stage - Elapsed: %s" % elapsed , level=Level.DEBUG)
 
 
 
'''
---------------------------------------------
      Preprocessing stage
---------------------------------------------
'''
start_time = time.time()
 
from cldas.morpho import Preprocess
 
for (reader,mapping) in corporea:
    source  = reader.source
    data    = reader.data( mapping=mapping )
    preproc = Preprocess( source, data )
    print "Classes:", preproc.categories()
    print "Success:", len( preproc.sents() ),", Fails:", len( preproc.failures() ) 
     
    dp.save_opinions( preproc.data() )
 
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Preprocessing stage - Elapsed: %s" % elapsed , level=Level.DEBUG)



'''
---------------------------------------------
      Adding Negation Scope tagging
---------------------------------------------
'''
start_time = time.time()

dp.save_negations_from_files('./neg/manual/*')    

if not dp.get_opinions(source='corpus_variado_sfu_neg'):    
    reader = CorpusReader( '../corpus/corpus_variado_sfu_neg', '*/*.xml', scope_pattern='<scope>(.*?)<\/scope>', negexp_pattern='<negex.*?>(.*?)<\/negexp>', op_pattern='<review.*?>(.*?)<\/review>', wd_pattern='<.*?wd=\"(.*?)\".*?\/>', file_pattern='<review.*?polarity=\"(.*?)\">' )
    print "Classes:", reader.categories()
    print "Opinions:", len( reader.opinions() )
    mapping = { 'negative':20, 'positive':80 }
    
    source  = reader.source
    data    = reader.data( mapping=mapping )
    preproc = Preprocess( source, data )
    print "Classes:", preproc.categories()
    print "Success:", len( preproc.sents() ),", Fails:", len( preproc.failures() ) 
    
    dp.save_opinions( preproc.data( tagged=dp.TaggedType.MANUAL ) )
   
elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Adding negations - Elapsed: %s" % elapsed , level=Level.DEBUG)



'''
---------------------------------------------
      Adding embeddings to database
---------------------------------------------
'''
start_time = time.time()

if not dp.get_embedding('.'):
    dp.update_embeddings(femb='../embeddings/emb39-word2vec.npy', ftok='../embeddings/emb39-word2vec.txt')

elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Adding embeddings- Elapsed: %s" % elapsed , level=Level.DEBUG)



'''
---------------------------------------------
      Negation Scope stage
---------------------------------------------
'''
start_time = time.time()

from cldas.neg.model import NegScopeLSTM, NegScopeFFN

tagged   = dp.get_tagged(dp.TaggedType.MANUAL)
untagged = dp.get_untagged()
vec_size = len( dp.get_null_embedding() )

path = './neg/models/'

######### Feed-Forward Neural Network ######### 
# wleft, wright = 2, 2
# ffn = NegScopeFFN( wleft, wright, vec_size )
#  
# fname = "model_NegScopeFFNl%i_r%i" % (wleft,wright)
# if os.path.exists(path+fname):
#     lstm.load_model(path+fname)
# else:
#     X_train, Y_train = dp.get_ffn_dataset( tagged, wleft, wright )
#     ffn.fit( X_train, Y_train )
#      
#     ffn.save_model(fname, './neg/models')
#      
# negations = {} ; total = len( untagged )
# for opinion in untagged:
#     progress("Predicting on new data",total,idx)
#     X_pred, _ = dp.get_ffn_dataset( [opinion], wleft , wright )
#     Y_pred = ffn.predict( X_pred )
#     Y_pred = Y_pred[0].tolist()
#     negations[ opinion['_id'] ] = Y_pred  
#     if idx % 500 == 0: # Optimization
#         dp.save_negations(negations, dp.TaggedType.AUTOMATIC)
#         negations = {}
# if negations: 
#     dp.save_negations(negations, dp.TaggedType.AUTOMATIC)    


####### LSTM Recurrent Neural Network ########
win = 10
lstm = NegScopeLSTM( win, vec_size )

fname = "model_NegScopeLSTM_w%i.h5" % win
if os.path.exists(path+fname):
    lstm.load_model(path+fname)
else:
    X_train, Y_train = dp.get_lstm_dataset( tagged, win )
    lstm.fit( X_train, Y_train )
    
    lstm.save_model(fname, './neg/models')
    
negations = {} ; total = len( untagged )
for idx,opinion in enumerate(untagged):
    progress("Predicting on new data",total,idx)
    X_pred ,_ = dp.get_lstm_dataset( [opinion], win , verbose=False)
    Y_pred = lstm.predict( X_pred )
    Y_pred = Y_pred.flatten().tolist()[: len( opinion['text'] ) ] # Only necessary with LSTM
    negations[ opinion['_id'] ] = Y_pred 
    if idx % 500 == 0: # Optimization
        dp.save_negations(negations, dp.TaggedType.AUTOMATIC)
        negations = {}   
if negations:
    dp.save_negations(negations, dp.TaggedType.AUTOMATIC)    


elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Negation stage - LSTM - Elapsed: %s" % elapsed , level=Level.DEBUG)



'''
---------------------------------------------
      Statistics over dataset
---------------------------------------------
'''
from cldas.db.stats import *

def table_print(fs):
    print '%-38s | %s' % ("Metric","Value")
    print '%-38s-+-%s' % ("-"*38,"-"*20)
    for f in fs:
        fname = f.__name__.replace('_',' ')
        fname = fname[0].upper()+fname[1:]
        res = f()
        if type(res) == list:
            print '%-38s | %s' % ( fname, "")
            for r in res:
                val = r.pop('count')
                key = r.keys()[0]
                key = "   %s: %s" % (key,r[key])
                print '%-38s | %s' % ( key, val if type(val) == int else round(a,4))
        else:
            print '%-38s | %s' % ( fname, res)
    print 
                
stats = []
stats.append( size_vocabulary             )
stats.append( size_vocabulary_by_word     )
stats.append( size_vocabulary_by_lemma    )
stats.append( size_manually_tagged        )
stats.append( size_corporea               )
stats.append( size_corporea_by_source     )
stats.append( size_reviews_category       )
stats.append( size_embeddings             ) 
stats.append( size_near_match             )
stats.append( size_null_match             )
stats.append( size_exact_match            )
stats.append( size_manually_tagged        )
stats.append( size_manually_tagged_by_cat )
stats.append( size_negative_words         )
stats.append( size_negators               )
stats.append( size_neutral_reviews        )
stats.append( size_neutral_words          )
stats.append( size_positive_reviews       ) 
stats.append( size_positive_words         )
stats.append( get_balance                 )
stats.append( get_balance_by_source       )

table_print(stats)



'''
---------------------------------------------
      Independent Lexicon stage
---------------------------------------------
'''
start_time = time.time()

from cldas.indeplex import by_senti_tfidf, by_senti_avg, by_senti_qtf, by_senti_pmi

pos = dp.get_opinions( cat_cond={"$gt":50} )
neg = dp.get_opinions( cat_cond={"$lt":50} )
lemmas = dp.get_lemmas()

indep_lexicons = []

li = by_senti_tfidf( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150 )
save(li, 'li_by_senti_tfidf', './indeplex')
indep_lexicons.append( li )

li = by_senti_qtf( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150 )
save(li, 'by_senti_qtf', './indeplex')
indep_lexicons.append( li )

li = by_senti_avg( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150 )
save(li, 'by_senti_avg', './indeplex')
indep_lexicons.append( li )
 
li = by_senti_pmi( pos, neg, lemmas, filter_tags=USEFUL_TAGS, limit=150 ) 
save(li, 'by_senti_pmi', './indeplex')
indep_lexicons.append( li )

elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Indeplex stage - Elapsed: %s" % elapsed , level=Level.DEBUG)



'''
---------------------------------------------
      Dependent Lexicon stage
---------------------------------------------
'''
start_time = time.time()

from cldas.deplex import by_influence, by_bfs
from cldas.utils.graph import MultiGraph

for corpus in dp.get_sources():
    
    opinions = dp.get_opinions( source=corpus )
    
    graph = MultiGraph( opinions, corpus, filter_tags=USEFUL_TAGS )
    
    for li in indep_lexicons:
        
        ld = by_bfs( graph, li, limit=300 )
        save(ld, 'ld_by_bfs', './deplex')
        
        ld = by_influence( graph, li, limit=300 )
        save(ld, 'ld_by_influence', './deplex')

elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
print "\n","Elapsed:",elapsed,"\n"
log( "Deplex stage - Elapsed: %s" % elapsed , level=Level.DEBUG)
