 # -*- encoding: utf-8 -*-
'''
Module with a set of models for determining the scope negation 

@author: Nicolás Mechulam, Damián Salvia
'''

import re, string

REGEX_PUNCT = '|'.join(re.escape(x) for x in string.punctuation)

import numpy as np
import random, glob
from pymongo.errors import BulkWriteError
from difflib import get_close_matches
from colorama import init, Fore, Style
init(autoreset=True) 

from cldas.utils import progress, load
from cldas.utils.logger import Log, Level 
from cldas.utils.misc import no_accent, EnumItems, Iterable, get_levinstein_pattern


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
db.reviews.ensure_index('source', name='source_index')
db.reviews.ensure_index('category', name='category_index')
db.reviews.ensure_index('tagged', name='negation_index')
db.embeddings.ensure_index('similars', name='similars_index')



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


def get_words(source=None,exclude=None):
    '''
    Gets vocabulary by word.
    @param source: Filter by source. 
    '''
    if source and exclude:
        result = db.reviews.distinct('text.word', {"source" : source , 'text.word' : { '$nin' : exclude } })
    elif source:
        result = db.reviews.distinct('text.word', {"source" : source})
    elif exclude:
        result = db.reviews.distinct('text.word', {'text.word' : { '$nin' : exclude } })
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
        result = db.reviews.find({ 'source': source, '_id' :{ '$in': identifiers } })
    else:
        result = db.reviews.aggregate([ 
            { '$match' : { "source" : source, "tagged" :{ "$exists" : False } } },
            { '$sample': { 'size' : quantity } }
        ]) 
    return Iterable( result )


def get_tagged(tag_as=None,source=None):
    '''
    Gets those opinions tagged with negation scope.
    @param tag_as: Can be manually (TaggedType.MANUAL) or automatically (TaggedType.AUTOMATIC)
    @param source: Filter by source. 
    '''
    if tag_as is None:
        query = { "$or" : [ { "tagged":'manually' }, { "tagged":'automatically' }] }
    else:
        query = { "tagged" : tag_as  }
    if source:
        query.update({ "source" : source })
    result = db.reviews.find(query).batch_size(10)
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
    result = result.batch_size(10)
    return Iterable( result )


def split_sample(ids=None, fraction=0.2, seed=1):
    '''
    Takes a random split sample of reviews.
    @param id       : A list of review's identifiers.
    @param fraction : Fraction consider for splitting.
    @param seed     : Seed consider for radomize.
    '''
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
    try:
        if embeddings: db.embeddings.insert_many(embeddings)
    except BulkWriteError as bwe:
        print bwe.details
        raise bwe


def get_null_embedding(null_as='__null__'):
    '''
    Gets a null embedding.
    @param null_as: Which word will cosider null. By default, dot word ('.').
    '''
    item = db.embeddings.find_one({ '_id':null_as })
    return item['embedding']


def get_embedding(word):
    '''
    Gets the embedding for the given word. 
    Can be None if the word has not an associated embedding. 
    @param word: Word which embedding will be retrieved
    '''
    item = db.embeddings.find_one({ "_id" : word })
    if item is None:
        item = db.embeddings.find_one({ "similars":{ "$elemMatch":{ "$eq":word } } })
    return item


def get_embedding_candidates(pattern):
    '''
    Gets a list of embeddings that matches a pattern
    @param pattern: Pattern for searching
    '''
    regex = re.compile(pattern, re.I|re.U)
    return list( db.embeddings.aggregate([
            { "$match": { "_id" : regex } },
            { "$group": { "_id" : None, 'words' : {'$push':'$_id' } } }
        ]) )


def get_aprox_embedding(word):
    '''
    Gets an approximated embedding for the given word.
    Priors the embedding for such word.
    @param word: Word which approximated embedding will be retrieved
    @param update: Updates similar embedding when no one matches
    '''
    item = get_embedding(word) 
    if item is not None:
        db.embeddings.update({ '_id': item['_id'] } , { '$addToSet': { "similars": word } })
        return item       

    match = re.search(REGEX_PUNCT,word)
    if match is None:
        pattern    = get_levinstein_pattern(word)
        candidates = get_embedding_candidates(pattern)

        if not candidates:
            pattern    = u'^{root}.+$'.format(root=word[:4])
            candidates = get_embedding_candidates(pattern)

        if candidates:
            candidates = candidates[0]['words']
            match = get_close_matches( no_accent(word), candidates, 1, 0.5 )

            if match:
                item = db.embeddings.find_one({ "_id" : match[0] })
                db.embeddings.update({ '_id': item['_id'] } , { '$addToSet': { "similars": word } })
                return item

    item = db.embeddings.find_one({ "_id" : "__null__" })
    db.embeddings.update({ '_id': '__null__' } , { '$addToSet': { "similars": word } })
    return item


def update_embeddings(femb, ftok, verbose=True):
    '''
    Reads embeddings and saves only if the word is in the current vocabulary.
    @param femb   : Embedding file (.npy).
    @param ftok   : Word list file (.txt).
    @param verbose: Print progress. 
    '''

    # Read embeddings and vocabulary
    embeddings = np.load(femb)
    vocabulary = unicode( open(ftok).read().lower() ,'utf8' ).splitlines()

    # Insert null embedding
    if db.embeddings.find_one({"_id":"__null__"}) is None:
        null = np.zeros( len(embeddings[0]) ).tolist()
        save_embeddings([{
            '_id'      :"__null__",
            'embedding':null,
            'similars':[]
        }])
        del null

    items = db.embeddings.find({}).batch_size(100)
    total = items.count() ; words = []; added = []
    for idx,item in enumerate(items):
        if verbose: progress("Getting emgeddings from database",total,idx)
        words.append( item['_id'] )
        added += item['similars'] # Already added
    words = set(words)

    # Filter words for avoid duplicates and irrelevants
    tmp = {}
    total = len(vocabulary)
    for idx,word in enumerate(vocabulary):
        if verbose: progress("Filtering words from database",total,idx)
        if len(word) < 80 and (word not in words) and re.search(u"^[a-zéúóúñü]+$|^[0-9]+$",word,re.U|re.I):
            tmp.update({word:idx})
    vocabulary = tmp

    # Dump filtered embeddings into database
    total = len(vocabulary)
    batch = []
    for idx, word in enumerate(vocabulary): 
        if verbose: progress("Loading embeddings from file",total,idx)
        batch.append({
            '_id'      :word,
            'embedding':embeddings[ vocabulary[word] ].tolist(),
            'similars':[]
        })
        if idx % 1000 == 0 and batch:
            save_embeddings(batch)
            batch = []     
    save_embeddings(batch)    
    del vocabulary ; del embeddings

    # For each word, find its most similar
    vocabulary = set( get_words() ) - set( added )
    total = len(vocabulary)
    for idx, word in enumerate(vocabulary):
        if verbose: progress("Updating embeddings from vocabulary", total, idx)
        get_aprox_embedding(word)


# ----------------------------------------------------------------------------------------------------------------------

def _format_ffn(opinions, wleft, wright, null_as, neg_as, verbose=1, **kwrgs):
    top = len(opinions)
    null = get_null_embedding( null_as )
    X_all, Y_all = [], []
    for idx,opinion in enumerate(opinions):
        is_train = opinion.has_key('tagged') and opinion['tagged'] == TaggedType.MANUAL 
        text = opinion['text']
        total = len(text)
        X_prev = [ null for _ in range(wleft) ]
        X_post = [ get_aprox_embedding( text[jdx]['word'] )['embedding'] if jdx < total else null for jdx in range(0,wright) ]
        for jdx in range(0,total,1):
            if verbose: progress("Getting data for FFN (word %4i of %4i)" % (jdx+1,total), top, idx, end=jdx+1==total)
            X_next = get_aprox_embedding( text[jdx+wright]['word'] )['embedding'] if jdx+wright < total else null
            X = X_prev + X_post + [ X_next ] ; X = sum(X,[])
            Y = None if not is_train else text[jdx]['negated'] if text[jdx]['negated'] is not None else neg_as
            X_all.append( np.asarray(X) ) ; Y_all.append( Y )
            del X ; del Y
            X_prev = X_prev[1:] + [ X_post[0] ]
            X_post = X_post[1:] + [ X_next ]
    return np.asarray(X_all), np.asarray(Y_all)


def _format_lstm(opinions, win, null_as, neg_as, verbose=1, **kwrgs):
    top = len(opinions)
    null = get_null_embedding( null_as )
    X_all, Y_all = [], []
    for idx,opinion in enumerate(opinions):
        is_train = opinion.has_key('tagged') and opinion['tagged'] == TaggedType.MANUAL 
        text = opinion['text']
        total = len(text) ; rest = (win - total) % win 
        for jdx in range(0,total+rest,win):
            if verbose: progress("Getting data for LSTM (word %4i of %4i)" % (jdx+1,total), top, idx, end=jdx+1==total)
            X = [ get_aprox_embedding( text[jdx+i]['word'] )['embedding'] if jdx+i < total else null for i in range(0,win) ]
            Y = [ None if not is_train else False if jdx+i >= total else text[jdx+i]['negated'] if text[jdx+i]['negated'] is not None else neg_as for i in range(0,win) ]
            X_all.append( np.asarray(X) ) ; Y_all.append( np.asarray(Y) )
            del X; del Y
    return np.asarray(X_all), np.asarray(Y_all)


def get_ffn_dataset(opinions, window_left, window_right, null_as='__null__', neg_as=True, **kwrgs):
    '''
    Given an opinion-set and windows left/right. returns the correct dataset format for FFN model
    @param opinions     : List of opinions.
    @param window_left  : Left context windows considered.
    @param window_right : Right context windows considered.
    @param null_as      : Embedding id consider as null.
    @param neg_as       : Consider negated item as True, False or None (as negator).
    '''
    return _format_ffn( opinions, wleft=window_left, wright=window_right, null_as=null_as, neg_as=neg_as, **kwrgs )


def get_lstm_dataset(opinions, window, null_as='__null__', neg_as=True, **kwrgs):
    '''
    Given an opinion-set and windows, returns the correct dataset format for LSTM model
    @param opinions : List of opinions.
    @param window   : Batch windows considered.
    @param null_as  : Embedding id consider as null.
    @param neg_as   : Consider negated item as True, False or None (as negator).
    '''
    return _format_lstm( opinions, win=window, null_as=null_as, neg_as=neg_as, **kwrgs )


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
    '''
    Saves evaluation result in the evaluation collection-
    @param results: List of results.
    '''
    tosave = []
    for idx,result in enumerate(results):
        tosave.append(result)
        if tosave and idx % 10 == 0:
            db.evaluation.insert_many( tosave )
            tosave = []
    if tosave:
        db.evaluation.insert_many(tosave)

