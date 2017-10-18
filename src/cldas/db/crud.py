 # -*- encoding: utf-8 -*-
'''
Module with a set of models for determining the scope negation 

@author: Nicolás Mechulam, Damián Salvia
'''

import numpy as np
import random, glob
from difflib import get_close_matches
from colorama import init, Fore, Style
init(autoreset=True) 

from cldas.utils import progress, load
from cldas.utils.logger import Log, Level 
from cldas.utils.misc import EnumItems, Iterable


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
        save_negations(content,tagged_as=TaggedType.MANUAL)


def get_opinion(_id):
    '''
    Gets an opinions.
    @param _id: Identiifier of the opinion.  
    '''
    return db.reviews.find_one( {'_id':_id } ) 


def get_opinions(cat_cond=None,source=None):
    '''
    Gets a set of opinions.
    @param category: Filter by category condition. 
    @param source: Filter by source.  
    '''
    query = {}
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
    result = db.reviews.find(query)
    return Iterable( result )


def get_untagged(limit=None,seed=None):
    '''
    Gets those opinions untagged with negation scope.
    @param limit: Quantity of opinions retrieved.
    @param seed : For setting the seed of random selection. 
    '''
    result = db.reviews.find({ "tagged" : { "$exists" : False } }) 
    if limit:
        random.seed( seed )  
        rand = int( random.random() * db.reviews.find({}).count() ) 
        result = result.skip( rand ).limit( limit )
    return Iterable( result )


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
    item = get_embedding(word)
    if not item:
        vocabulary = db.embeddings.distinct("_id")
        match = get_close_matches( word , vocabulary , 1 , 0.75 )
        if match: item = db.embeddings.find_one({ "_id" : match[0] })
        else    : item = db.embeddings.find_one({ "_id" : "." })
    result = item['embedding']
    return result


def update_embeddings(femb='../../embeddings/emb39-word2vec.npy', ftok='../../embeddings/emb39-word2vec.txt', verbose=True):
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
        if verbose: progress("Updating embeddings (%i,%i,%i,%i)" % ( stats['ByWord'],stats['ByRepl'],stats['ByClos'],stats['IsNull'] ),total,idx)
        if not get_embedding(word):
            nearest , vector = get_nearest_vector( word )
            result.append({ 
                '_id'      :word,
                'embedding':vector.tolist(),
                'nearestOf':nearest 
            })
        if idx % 500 == 0 and result:
            save_embeddings(result)
            result = []
    
    # Save statistics results
    log("Embeddings integration result. %s" % str(stats),level=Level.INFO)
    if verbose: 
        for case in stats: print "%-17s : %i (%4.2f%%)" % ( case,stats[case],100.0*stats[case]/sum(stats.values()) )     
    
    # Save results in database
    save_embeddings(result)

# ----------------------------------------------------------------------------------------------------------------------


def _format_ffn(text, wleft, wright, null, neg_as, is_train):
    X,Y = [],[]
    for idx, token in enumerate(text):       
        x_curr = [ get_aprox_embedding( token['word'] ) if 0 <= idx < len(text) else null for idx in range(wleft + wright + 1) ]
        x_curr = np.array( x_curr ).flatten()
        y_curr = None if not is_train else token['negated'] if token['negated'] is not None else neg_as
        X.append( x_curr )
        Y.append( y_curr )
    return X,Y


def _format_lstm(text, win, null, neg_as, is_train):
    x_curr = [ get_aprox_embedding( token['word'] ) for token in text ]
    y_curr = [ None if not is_train else token['negated'] if token['negated'] is not None else neg_as for token in text ]
    rest = (win - len(x_curr)) % win 
    if rest > 0:
        x_curr.extend( [ null for _ in range(rest) ] )
        y_curr.extend( [ False for _ in range(rest) ] )
    X = [ x_curr[i*win : (i+1)*win] for i in range(len(x_curr)/win) ]
    Y = [ y_curr[i*win : (i+1)*win] for i in range(len(y_curr)/win) ]
    return X,Y


def _format_embeddings(formatter, opinions, **kwargs):
    verbose  = kwargs.pop('verbose')
    null_as  = kwargs.pop('null_as')
    null     = get_null_embedding(null_as)
    total    = len( opinions )
    X , Y = [] , []
    for idx,opinion in enumerate(opinions):
        is_train = opinion.has_key('tagged') and opinion['tagged'] == TaggedType.MANUAL
        if verbose: progress("Loading training data (%i words)"  % len(opinion['text']),total,idx)
        x_curr, y_curr = formatter( opinion['text'], null=null, is_train=is_train, **kwargs )
        X += x_curr
        Y += y_curr if is_train else []    
    yield np.array(X)
    yield np.array(Y)


def get_ffn_dataset(opinions, wleft, wright, null_as='.', neg_as=False, verbose=True):
    '''
    Given an opinion set and windows left/right returns the correct dataset format for FFN model
    '''
    return _format_embeddings( _format_ffn, opinions, wleft=wleft, wright=wright, null_as=null_as, neg_as=neg_as,  verbose=verbose )


def get_lstm_dataset(opinions, win, null_as='.', neg_as=False, verbose=True):
    '''
    Given an opinion set and windows left/right returns the correct dataset format for LSTM model
    '''
    return _format_embeddings( _format_lstm, opinions, win=win, null_as=null_as, neg_as=neg_as,  verbose=verbose )


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
