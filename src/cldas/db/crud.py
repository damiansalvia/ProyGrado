 # -*- encoding: utf-8 -*-
'''
Module with a set of models for determining the scope negation 

@author: Nicolás Mechulam, Damián Salvia
'''

import re
import numpy as np
import random, glob
from difflib import get_close_matches
from colorama import init, Fore, Style
init(autoreset=True) 

from cldas.utils import progress, load
from cldas.utils.logger import Log, Level 
from cldas.utils.misc import EnumItems, Iterable, get_levinstein_pattern


log = Log("./log")


try:
    print "Connecting Mongo database"
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError
    client = MongoClient(serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client.CLDAS
except ServerSelectionTimeoutError:
    raise Exception("Couldn't connect Mongo database.")



print "Creating Mongo indexes"
db.reviews.create_index('source', name='source_index')
db.reviews.create_index('category', name='category_index')
db.reviews.create_index('tagged', name='negation_index')



class TaggedType(EnumItems):
    MANUAL    = "manually"
    AUTOMATIC = "automatically" 
    
    
    
class DataSetType(EnumItems):
    TRAIN   = 0
    PREDICT = 1     
        
        
        
def save_opinions(opinions, verbose=True):
    '''
    Saves a set of opinions in the database.
    @param opinions: Collection of opinions (check cldas.utils.misc.OpinionType, value 2)
    '''
    if not opinions:
        return
    total = len( opinions ) ; tosave = []
    for idx,opinion in enumerate(opinions):
        if verbose: progress("Saving opinions", total, idx)
        if not db.reviews.find_one( opinion['_id'] ):
            tosave.append( opinion )
        if tosave and idx % 500 == 0:
            db.reviews.insert_many( tosave )
            tosave = []
    if tosave:
        db.reviews.insert_many(tosave)


def save_negations(negations,tag_as,do_correction=False):
    '''
    Saves negation scope for a set of opinions.
    @param negations     : Set of _id:collection where _id is the identifier of a review and collection a set of 
                           boolean values correlated to words in the opinion which will be negated or not.
    @param tag_as        : Can be manually (TaggedType.MANUAL) or automatically (TaggedType.AUTOMATIC)
    @param do_corrections: Display UI for correct missmatch.  
    '''
    
    for _id in negations:
        
        opinion = db.reviews.find_one({'_id':_id})
        if not opinion:
            log("Opinion %s skipped (not found)" %  _id , level=Level.ERROR)
            continue
        
        negation = { 'tagged' : tag_as }
        for idx, tag in enumerate( negations[_id] ):
            negation['text.' + str(idx) + '.negated'] = tag
        
        if 'tagged' in opinion.keys() and do_correction:
            currtags = [ item['negated'] for item in opinion['text'] ] 
            if negations[_id] == currtags: # skip if all tags equal
                continue
            negation = _do_correction(opinion,negation)
            
        db.reviews.update( { '_id': _id } , { '$set': negation } )


def save_negations_from_files(sources,verbose=True):
    '''
    Saves negation scope read from a set of source files.
    @param source_dir : Pattern source directory to files (e.g. "my/path/*") or specific file path.
    @param verbose    : For print progress.  
    '''
    sources = glob.glob(sources)
    total = len(sources)
    for idx,source in enumerate(sources):
        if verbose: progress("Load negation tags from %s" % source,total,idx)
        content = load(source)   
        save_negations(content,TaggedType.MANUAL)


def get_opinion(_id):
    '''
    Gets an opinions.
    @param _id: Identiifier of the opinion.  
    '''
    return db.reviews.find_one( {'_id':_id } ) 


def get_opinions(ids=None, cat_cond=None,source=None):
    '''
    Gets a set of opinions.
    @param ids: Filter by ids. 
    @param category: Filter by category condition. 
    @param source: Filter by source.  
    '''
    query = {}
    if ids:
        query.update({'_id': {'$in': ids} })
    if cat_cond:
        query.update({ 'category' : cat_cond })
    if source:
        query.update({ 'source' : source })
    result = db.reviews.find(query)
    return Iterable( result )


def get_sources(pattern=None):
    '''
    Gets a set of sources.
    @param pattern: Filter sources given a pattern. 
    '''
    if pattern:
        result = db.reviews.distinct("source", {'source' : { '$regex' : pattern } })
    else:
        result = db.reviews.distinct("source")
    return Iterable( result )


def get_lemmas(source=None):
    '''
    Gets vocabulary by lemma.
    @param source: Filter by source. 
    '''
    if source:
        result = db.reviews.distinct('text.lemma', { "source" : source })
    else:
        result = db.reviews.distinct('text.lemma')
    return Iterable( result )


def get_words(source=None):
    '''
    Gets vocabulary by word.
    @param source: Filter by source. 
    '''
    if source:
        result = db.reviews.distinct('text.word', {"source" : source })
    else:
        result = db.reviews.distinct('text.word')
    return Iterable( result )


def get_sample(quantity, source, identifiers=None):
    '''
    Gets an opinion sampling.
    @param quantity: How many reviews will be in the sample.
    @param source : Filter by source.
    @param indexes: Ignores Quantity and retrieves a fix sample from a list of identifiers. 
    '''
    if identifiers:
        result = db.reviews.find({ 'source': source, '_id' :{ '$in': identifiers} })
    else:
        result = db.reviews.aggregate([ 
            { '$match' : { "source" : source, "tagged" :{ "$exists" : False } } },
            { '$sample': { 'size' : quantity } }
        ]) 
    return Iterable( result )


def get_tagged(tag_as,source=None):
    '''
    Gets those opinions tagged with negation scope.
    @param tag_as: Can be manually (TaggedType.MANUAL) or automatically (TaggedType.AUTOMATIC)
    @param source: Filter by source. 
    '''
    query = { "tagged" : tag_as  }
    if source:
        query.update({ "source" : source })
    result = db.reviews.find(query)#.batch_size(50)
    return Iterable( result )


def get_untagged(limit=None,seed=None):
    '''
    Gets those opinions untagged with negation scope.
    @param limit: Quantity of opinions retrieved.
    @param seed : For setting the seed of random selection. 
    '''
    result = db.reviews.find({ "tagged" : { "$exists" : False } })#.batch_size(10) 
    if limit:
        random.seed( seed )  
        rand = int( random.random() * db.reviews.find({}).count() ) 
        result = result.skip( rand ).limit( limit )
    result = result#.batch_size(50)
    return Iterable( result )


def split_sample(ids=None, fraction=0.2, seed=1):
    query = []
    random.seed(seed)
    slice_1, slice_2 = [],[]
    if ids:
        query.append({"$match": {"_id": {"$in": ids } } })
    query.append({
        "$group":{
            "_id": "$source",
            "ids": { "$push": "$_id" }
        }
    })
    ids = db.reviews.aggregate(query)
    for e in ids:
        id_list = e.get('ids')
        random.shuffle(id_list)
        frac = int(len(id_list) * fraction)
        slice_1.extend(id_list[:frac])
        slice_2.extend(id_list[frac:])

    return slice_1, slice_2


# ----------------------------------------------------------------------------------------------------------------------


def save_embeddings(embeddings):
    '''
    Saves a set of embeddings in the database.
    @param embeddings: Collection of embeddings with format ["<word>":{'embedding':[X1,...,Xn],...}]
    '''
    if embeddings: db.embeddings.insert_many(embeddings)


def get_null_embedding(null_as='.'):
    '''
    Gets a null embedding.
    @param null_as: Which word will cosider null. By default, dot word ('.').
    '''
    result = db.embeddings.find_one({ '_id':null_as })['embedding']
    return result 


def get_embedding(word):
    '''
    Gets the embedding for the given word. 
    Can be None if the word has not an associated embedding. 
    @param word: Word which embedding will be retrieved
    '''
    result = db.embeddings.find_one({ "_id" : word })
    return result


def get_aprox_embedding(word):
    '''
    Gets an approximated embedding for the given word.
    Priors the embedding for such word.
    @param word: Word which approximated embedding will be retrieved
    '''
    item = db.embeddings.find_one({ "_id" : word })
    if item is not None:
        return item['embedding']

    item = db.embeddings.find_one({ "similar":{ "$elemMatch":{ "$eq":word } } })
    if item is not None:
        return item['embedding']

    regex = get_levinstein_pattern(word)
    candidates = list( 
        db.embeddings.aggregate([
            { "$match": { "_id" : regex } },
            { "$group": { "_id" : None, 'words' : {'$push':'$_id' } } }
        ]) 
    )
    if candidates:
        candidates = candidates[0]['words']
        match = get_close_matches(word,candidates,1,0.75)
        if match:
            item = db.embeddings.find_one({ "_id" : match[0] })
            db.embeddings.update({ '_id': item['_id'] } , { '$addToSet': { "similar": word } })
            return item['embedding']

    item = db.embeddings.find_one({ "_id" : "." })
    return item['embedding']


def update_embeddings(femb='../embeddings/emb39-word2vec.npy', ftok='../embeddings/emb39-word2vec.txt', verbose=True):
    '''
    Reads embeddings and saves only if the word is in the current vocabulary.
    @param femb   : Embedding file (.npy).
    @param ftok   : Word list file (.txt).
    @param verbose: Print progress. 
    '''
      
    stats = { "ByWord":0,"ByRepl":0,"ByClos":0,"IsNull":0 }
    
    # Load vectors and its words
    vocabulary  = unicode( open(ftok).read().lower().replace("_","") ,'utf8' )    
    index_for   = { token:index for index,token in enumerate(vocabulary.splitlines()) }
    embeddings  = np.load(femb)
    
    # Get dimension and create the null vector
    dimension  = len(embeddings[0])
    nullvector = np.zeros(dimension)
    
    # Get vocabulary
    vocabulary = get_words()  
    
    # Get difference of vector-words and vocabulary-words for improving get_close_matches performance 
    # PROBLEM: 'pizería' is excluded although 'pizerías' is in the vocabulary (i.e. won't have a closest match)
    dif_keys = set(index_for.keys()) - set(vocabulary)
    for key in list(dif_keys): index_for.pop(key,None)
    
    replaces = {u'a':u'á',u'e':u'é',u'i':u'í',u'o':u'ó',u'u':u'ú'}
    
    def get_nearest_vector( # Get the associated vector of a word and its match (null if it is the same or null vector)
            word
        ):
        
        if index_for.has_key(word):
            stats['ByWord'] += 1
            return None , embeddings[ index_for[ word ] ]
        
        vowels = {idx:char for idx,char in enumerate(word) if char in 'aeiou'}
        for idx,vowel in vowels.items():
            replaced = word[:idx] + replaces[vowel] + word[idx+1:]
            if index_for.has_key(replaced):
                stats['ByRepl'] += 1
                return replaced , embeddings[ index_for[ replaced ] ]

        size = len(word)
        if size > 1 and size < 20 and ('_' not in word): # Prevents unnecessary calculation
            possibilities = filter( lambda x: size-2 < len(x) < size+2 , index_for.keys() )
            match = get_close_matches( word , possibilities , 1 , 0.75 )
            if match:
                stats['ByClos'] += 1
                return match[0] , embeddings[ index_for[ match[0] ] ]
        
        stats['IsNull'] += 1
        return None , nullvector 
    
    
    # For each word in vocabulary find its embedding    
    result = []
    total = len(vocabulary)
    
    for idx,word in enumerate(vocabulary):
        if verbose: progress("Updating embeddings [W:%*i|R:%*i|C:%*i|N:%*i]" % ( 6,stats['ByWord'],6,stats['ByRepl'],6,stats['ByClos'],6,stats['IsNull'] ),total,idx)
        if not get_embedding(word):
            nearest , vector = get_nearest_vector( word )
            result.append({ 
                '_id'      :word,
                'embedding':vector.tolist(),
                'nearestOf':nearest,
                'similar':[] 
            })
        if idx % 500 == 0 and result:
            save_embeddings(result)
            result = []
    
    # Save statistics results
    log("Embeddings integration result. %s" % str(stats),level=Level.INFO)
    if verbose:
        total = sum(stats.values())
        if total == 0: total = 1 
        for case in stats: print "%-17s : %*i (%4.2f%%)" % ( case, 6, stats[case], 100.0*stats[case]/total )     
    
    # Save results in database
    save_embeddings(result)
    

# ----------------------------------------------------------------------------------------------------------------------

def _format_ffn(opinions, wleft, wright, null_as, neg_as, verbose):
    top = len(opinions)
    null = get_null_embedding( null_as )
    for idx,opinion in enumerate(opinions):
        X,Y = [], []
        is_train = opinion.has_key('tagged') and opinion['tagged'] == TaggedType.MANUAL 
        text = opinion['text']
        total = len(text) ; jdx=0
        # if verbose: progress("Training FFN (word %4i of %4i)" % (jdx+1,total), top, idx, width=70)
        x_prev = [ null for _ in range(wleft) ]
        x_post = [ [ get_aprox_embedding( text[jdx]['word'] ) ] for idx in range(0,wright+1) ] # includes current - range(0,...)
        x_curr = np.array(x_prev).flatten().tolist() + np.array(x_post).flatten().tolist()
        x_curr = np.array( x_curr ).flatten()
        y_curr = None if not is_train else text[jdx]['negated'] if text[jdx]['negated'] is not None else neg_as
        X.append( x_curr ) ; Y.append( y_curr )
        del x_curr; del y_curr
        for jdx in range(1,total):   
            if len(X) % 32 == 0:
                yield np.asarray(X), np.asarray(Y)
            # if verbose: progress("Training FFN (word %4i of %4i)" % (jdx+1,total), top, idx, width=70)
            x_next = [ get_aprox_embedding( text[jdx+wright]['word'] ) ] if jdx+wright < total else [ null ]
            x_curr = np.array(x_prev[1:]).flatten().tolist() + np.array(x_post).flatten().tolist() + x_next[0]
            x_curr = np.array( x_curr ).flatten()
            y_curr = None if not is_train else text[jdx]['negated'] if text[jdx]['negated'] is not None else neg_as
            X.append( x_curr ) ; Y.append( y_curr )
            del x_curr; del y_curr
            x_prev = x_prev[1:] + x_post[0]
            x_post = x_post[1:] + [ x_next ]
        if len(X) % 32 == 0:
            yield np.asarray(X), np.asarray(Y)


def _format_lstm(opinions, win, null_as, neg_as, verbose):
    top = len(opinions)
    null = get_null_embedding( null_as )
    for idx,opinion in enumerate(opinions):
        X,Y = [], []
        is_train = opinion.has_key('tagged') and opinion['tagged'] == TaggedType.MANUAL 
        text = opinion['text']
        total = len(text) ; jdx=0
        # if verbose: progress("Training LSTM (word %4i of %4i)" % (jdx+1,total), top, idx, width=70)
        x_curr = [ get_aprox_embedding( text[jdx+i]['word'] ) if jdx+i < total else null for i in range(0,win) ]
        y_curr = [ None if not is_train else False if jdx+i >= total else text[jdx+i]['negated'] if text[jdx+i]['negated'] is not None else neg_as for i in range(0,win) ]
        X.append( np.asarray(x_curr) ) ; Y.append( np.asarray(y_curr) )
        del x_curr; del y_curr
        rest = (win - total) % win 
        for jdx in range(win,total+rest,win):
            if len(X) % 32 == 0:
                yield np.asarray(X), np.asarray(Y)
            # if verbose: progress("Training LSTM (word %4i of %4i)" % (jdx+1,total), top, idx, width=70)
            x_curr = [ get_aprox_embedding( text[jdx+i]['word'] ) if jdx+i < total else null for i in range(0,win) ]
            y_curr = [ None if not is_train else False if jdx+i >= total else text[jdx+i]['negated'] if text[jdx+i]['negated'] is not None else neg_as for i in range(0,win) ]
            X.append( np.asarray(x_curr) ) ; Y.append( np.asarray(y_curr) )
            del x_curr; del y_curr
        if len(X) % 32 == 0:
            yield np.asarray(X), np.asarray(Y)


def _generate_data(formatter, *args, **kwargs):
    while True:
        try: yield next(gen)
        except (StopIteration, UnboundLocalError):
            gen = formatter(*args,**kwargs)


def get_ffn_dataset(opinions, wleft, wright, test_frac=0.2, null_as='.', neg_as=True, verbose=True):
    '''
    Given an opinion set and windows left/right returns the correct dataset format for FFN model
    '''
    test_data, train_data = opinions.split_sample(test_frac) 
    train_gen = _generate_data( _format_ffn, train_data, wleft=wleft, wright=wright, null_as=null_as, neg_as=neg_as,  verbose=verbose )
    test_gen  = _generate_data( _format_ffn, test_data , wleft=wleft, wright=wright, null_as=null_as, neg_as=neg_as,  verbose=verbose )
    train_gen = Iterable( train_gen, sum(1 for op in train_data for _ in op['text'] ) )
    test_gen  = Iterable( test_gen , sum(1 for op in test_data  for _ in op['text'] ) )
    return train_gen, test_gen


def get_lstm_dataset(opinions, win, test_frac=0.2, null_as='.', neg_as=True, verbose=True):
    test_data,  train_data = opinions.split_sample(test_frac)
    train_gen = _generate_data( _format_lstm, train_data, win=win, null_as=null_as, neg_as=neg_as,  verbose=verbose )
    test_gen  = _generate_data( _format_lstm, test_data , win=win, null_as=null_as, neg_as=neg_as,  verbose=verbose )
    train_gen = Iterable( train_gen, sum(1 for op in train_data for _ in op['text'] ) )
    test_gen  = Iterable( test_gen , sum(1 for op in test_data  for _ in op['text'] ) )
    return train_gen, test_gen


# ----------------------------------------------------------------------------------------------------------------------


def _do_correction(opinion,negation):
    negs = {x:negation[x] for x in negation}
    diff = []
    print "\n%s vs. %s" % ( opinion['tagged'].upper() , negs['tagged'].upper() )
    for idx,item in enumerate(opinion['text']):
        print "%s%s" % (
                item['word'],
                Fore.MAGENTA+Style.BRIGHT+"(%s:%s)[%i]"+Fore.RESET+Style.RESET_ALL % (
                    'i' if item['negated'] else 'n' , 
                    'i' if negs['text.' + str(idx) + '.negated'] else 'n',
                    idx
                ) if item['negated'] != negs['text.' + str(idx) + '.negated'] \
                else Fore.BLUE+Style.BRIGHT+"/%sm"+Fore.RESET+Style.RESET_ALL % (
                    'i' if item['negated'] else 'n'
                ),
            ),
        if item['negated'] != negs['text.' + str(idx) + '.negated']: diff.append(idx)
    print
    diff = list(reversed(diff))
    queue = []
    while diff:
        idx = diff.pop()
        op = raw_input("Q(uit), B(ack), L(eft) or R(ight) for [%i] > " % idx)
        op = op.lower()
        if op == 'q':
            negs = negation
            break  
        elif op == 'l':
            queue.append(idx)
            negs['text.' + str(idx) + '.negated'] = opinion['text'][idx]['negated']
        elif op == 'r':
            queue.append(idx)
            negs['text.' + str(idx) + '.negated'] = negs['text.' + str(idx) + '.negated']
        elif op == 'b':
            diff.append(idx)
            if queue: diff.append(queue.pop())
        else:
            diff.append(idx)
    return negs


# ----------------------------------------------------------------------------------------------------------------------


def save_evaluation(results):
    tosave = []
    for idx,result in enumerate(results):
        tosave.append(result)
        if tosave and idx % 10 == 0:
            db.evaluation.insert_many( tosave )
            tosave = []
    if tosave:
        db.evaluation.insert_many(tosave)

