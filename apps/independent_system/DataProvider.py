 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
from utilities import *

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import numpy as np
from itertools import combinations
from difflib import get_close_matches



log = Log("./log")



print "Connecting Mongo database"
try:
    client = MongoClient(serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client.ProyGrado
except ServerSelectionTimeoutError:
    raise Exception("Couldn't connect Mongo database")



print "Creating Mongo indexes"
db.reviews.create_index('idx', name='position_index')
db.reviews.create_index('source', name='source_index')
db.reviews.create_index('category', name='category_index')
db.reviews.create_index('tagged', name='negation_index')

        
        
def save_opinions(opinions):
    if opinions: db.reviews.insert_many(opinions)


def save_negations(opinions,tagged_as):
    if tagged_as not in ['manually','automatically']:
        raise Exception("Values for 'tagged_as' must be 'manually' or 'automatically'")
    for _id in opinions:
        negation = { 'tagged' : tagged_as }
        for idx, tag in enumerate(opinions[_id]):
            negation['text.' + str(idx) + '.negated'] = tag
        if opinions[_id]:
            db.reviews.update( { '_id': _id } , { '$set': negation }  )


def get_sources():
    return list(db.reviews.distinct("source"))


def get_opinion(id):
    return db.reviews.find_one({'_id':id})


def get_opinions(source=None):
    query = {'source': source} if source else {}
    return db.reviews.find(query)


def get_by_idx(source, idx):
    return db.reviews.find_one({'source': source, 'idx': idx})


def get_sample(quantity, source, indexes = None):
    if indexes:
        return list(db.reviews.find({
            'source': source,
            'idx' :{ '$in': indexes} 
        }))
    return list(db.reviews.aggregate([ 
        { '$match' : { "source" : source,"tagged" : { "$exists" : False } } },
        { '$sample': { 'size': quantity } } 
    ]))


def get_tagged(tagger,source=None):
    query = { "tagged" : tagger  } 
    if source and not source.isdigit(): # TO-DO : por algun motivo me llega un source=2
        query.update({ "source" : source })
    return list(db.reviews.find(query))


def get_untagged():
    return list(db.reviews.find({ "tagged" : { "$exists" : False } }))


def get_size_embedding():
    return len(db.embeddings.find_one({},{ '_id':0 })['embedding'])
    

def get_word_embedding(word):
    res = db.embeddings.find_one({ "_id" : word })
    if res: return res['embedding']
    raise Exception("Couldn't find embedding for '%s'" % word)


def get_text_embeddings(text, wleft, wright):
    
    size_embedding = get_size_embedding()
    
    def get_entry(text, pos):
        if  0 <= pos < len(text) :
            word =  text[pos]['word'].lower()
            return get_word_embedding(word)
        else :
            return np.zeros( size_embedding )
    
    data,pred = [],[]
    
    for idx, word in enumerate(text):
    
        embeddings = []        
        for i in range(wleft + wright + 1):
            embeddings.append( get_entry( text , idx-wleft+i ) )
        
        embeddings = np.array( embeddings ).flatten()
        data.append(embeddings)
        
        if text[idx].has_key('negated'): # for training
            prediction = np.array(text[idx]['negated'])
            pred.append( prediction )
    
    return data, pred


def update_embeddings(
        femb='../../embeddings/emb39-word2vec.npy',
        ftok='../../embeddings/emb39-word2vec.txt',
        split_tolerance=1,
        verbose=False
    ):
      
    stats = { "ByWord":0,"ByClosest":0,"IsNull":0,"Fails":0,"Total":0 }
    
    # Load vectors and its words
    content     = open(ftok).read().lower().replace("_","")
    content     = unicode(content,'utf8')    
    index_for   = { token:index for index, token in enumerate(content.splitlines()) }
    embeddings  = np.load(femb)
    
    # Get simension and create the null vector
    dimension  = len(embeddings[0])
    nullvector = np.zeros(dimension)
    
    # Get vocabulary
    vocabulary = db.reviews.distinct("text.word")  
    
    # Get difference of vector-words and vocabulary-words 
    # for improving get_close_matches performance
    dif_keys = set(index_for.keys()) - set(vocabulary)
    for key in list(dif_keys): index_for.pop(key,None)
    
    
    def get_vectors( # Get the associated vector of a word
            word
        ):
        
        stats['Total'] += 1
        
        if index_for.has_key(word):
            stats['ByWord'] += 1
            return embeddings[ index_for[ word ] ]

        size = len(word)
        if size > 1 and size < 15 and ('_' not in word):
            possibilities = filter( lambda x: size-2 < len(x) < size+2 , index_for.keys() )
            match = get_close_matches( word , possibilities , 1 , 0.60 )
            if match:
                stats['ByClosest'] += 1
                return embeddings[ index_for[ match[0] ] ]
        
        if size > 1:
            print "\n", word;import pdb; pdb.set_trace()
        
        stats['IsNull'] += 1
        return nullvector 
    
    
    # For each word find its embedding    
    result = {}
    total = len(vocabulary)
    
    for idx,word in enumerate(vocabulary):
        progress("Updating embeddings (%i,%i,%i)" % ( stats['ByWord'],stats['ByClosest'],stats['IsNull'] ),total,idx)
        if result.has_key(word):
            continue
        vector = get_vectors( word )
        result.update({ word:vector })
    
    # Save statistics results
    log("Embeddings integration result. %s" % str(stats),level='info')
    if verbose:
        if stats['Total']:
            for case in stats: print "%-17s : %i (%4.2f%%)" % (case,stats[case],100.0*stats[case]/stats['Total']) 
            raw_input("Press enter to continue...")
        else:
            print "No embeddings has been processed"    
    
    # Save results in database
    result = [{ '_id':word, 'embedding':result[word].tolist() } for word in result]
    db.embeddings.insert_many(result)

# ----------------------------------------------------------------------------------------------------------------------


def get_stat_balanced(source=None):
    query = {}
    if source:
         query.update({ 'source':source })
    items = db.reviews.find(query)
    balance = int( round( sum( item['category'] for item in items ) / items.count() ) )
    return balance

if __name__ == '__main__':
    pass


