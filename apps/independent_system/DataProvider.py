 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')
from utilities import *

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import numpy as np
from itertools import combinations


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


def get_sources():
    return list(db.reviews.distinct("source"))


def get_opinion(id):
    return db.reviews.find_one({'_id':id})


def get_by_idx(source, idx):
    return db.reviews.find_one({'source': source, 'idx': idx})


def save_opinions(opinions):
    if opinions:
        db.reviews.insert_many(opinions)


def save_negations(opinions):
    for _id in opinions:
        negation = { 'tagged' : 'manually' }
        for idx, tag in enumerate(opinions[_id]):
            negation['text.' + str(idx) + '.negated'] = tag
        if opinions[_id]:
            db.reviews.update( { '_id': _id } , { '$set': negation }  )


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
    if source:
        return list(db.reviews.find({ "tagged" : tagger , "source" : source }))
    return list(db.reviews.find({ "tagged" : tagger }))


def get_untagged():
    return list(db.reviews.find({ "tagged" : { "$exists" : False } }))


def save_result(opinions):
    for id in opinions:
        options = { 'tagged' : 'automatically' }
        for idx, tag in opinions[id]:
            opinions['text.' + str(idx) + '.negated'] = tag
        db.reviews.update( {'_id': id}, {'$set': options} )


def get_corproea_size():
    return len(db.reviews.distinct("source"))


def get_indepentent_lex(limit=None, tolerance=0, filter_neutral=False):
    min_matches = int(round(get_corproea_size()*(1.0-tolerance),0))
    query = [
        { '$unwind' : '$text' },{ 
            '$group': {
                '_id'  : { 'source': '$source', 'lemma': '$text.lemma'},
                'sent' : { '$avg' : { 
                        '$cond' : {
                            'if'  :  '$text.neg',
                            'then': { '$subtract': [ 100 , "$category"] },
                            'else': '$category'
                        }
                    } 
                }      
            }
        },{
            '$group': {
                '_id' : '$_id.lemma',
                'polarities' : {
                    '$push' : {
                        '$switch' : { 'branches' : [
                            {'case' : { '$gte' : ['$sent', 60] }, 'then': '+'},    
                            {'case' : { '$lte' : ['$sent', 30] }, 'then': '-'},    
                            {'case' : True, 'then': '0'},    
                        ]}
                    }
                }
            }
        },
        {
            '$project' : {
                'lemma' : "$_id",
                'corpus_len' : { '$size': "$polarities" } ,
                'pol' : { '$arrayElemAt': [ "$polarities", 0] },
                'accepted' : {
                   '$let': {
                       'vars': {
                          'first': { '$arrayElemAt': [ "$polarities", 0] },
                       },
                       'in': { 
                            '$reduce' : {
                                'input': "$polarities",
                                'initialValue': True,
                                'in': { '$and': ["$$value", { '$eq' : ["$$this", "$$first" ]}] }
                            } 
                        }
                    }
                },
                'polarities' : "$polarities"
            }
        },
        { '$match' : { 'accepted': True, 'corpus_len' : { '$gte' : min_matches } } }
    ] 

    if filter_neutral:
        query.append({ '$match' : {'pol': {'$ne': '0'} } })
        
    query.extend([
        { '$project' : {'_id': 0, 'accepted' : 0} },
        { '$sort' : { 'corpus_len' : -1 } }
    ])
    
    if limit:
       query.append({ '$limit': limit }) 
       
    return list(db.reviews.aggregate(query))


def get_indepentent_lex2(limit=None, tolerance=0, filter_neutral=False):
    min_matches = int(round(get_corproea_size()*(1.0-tolerance),0))
    sum_pos = list(db.reviews.aggregate([
        { '$match': { 'category': { '$gt': 50 } } },
        { '$unwind' : '$text' },
        {
            '$group': {
                '_id':None,
                'value': { '$sum': '$category'}
            }
        }
    ]))[0].get('value')
    sum_neg = list(db.reviews.aggregate([
        { '$match': { 'category': { '$lt': 50 } } },
        { '$unwind' : '$text' },
        {
            '$group': {
                '_id':None,
                'value': { '$sum': '$category'}
            }
        }
    ]))[0].get('value')
    query = [
        { '$unwind' : '$text' },
        { 
            '$project' : {
                "_id"      : 1,
                'category' : { '$subtract': ['$category', -50] },
                "source"   : 1,
                "idx"      : 1,
                "text"     : 1,
                "tagged"   : 1
            
            }
        },{ 
            '$group': {
                '_id'  : { 'source': '$source', 'lemma': '$text.lemma'},
                'sent' : { 
                    '$sum': { 
                        '$cond': [ {'$gt': ['$category',50]}, 
                            { '$divide': [ 
                                {'$subtract': ['$category', 50]}, 
                                sum_pos 
                            ]},   
                            {'$cond': [{'$lt': ['$category',50]},
                                { '$divide': [ 
                                    {'$subtract': [0,{'$subtract': [50,'$category']}]}, 
                                    sum_neg 
                                ]},
                                0,
                            ]}
                        ]
                    } 
                }
            }
        },{
            '$group': {
                '_id' : '$_id.lemma',
                'polarities' : {
                    '$push' : {
                        '$switch' : { 'branches' : [
                            {'case' : { '$gt' : ['$sent', 0] }, 'then': '+'},    
                            {'case' : { '$lt' : ['$sent', 0] }, 'then': '-'},    
                            {'case' : True, 'then': '0'},    
                        ]}
                    }
                }
            }
        },
        {
            '$project' : {
                'lemma' : "$_id",
                'corpus_len' : { '$size': "$polarities" } ,
                'pol' : { '$arrayElemAt': [ "$polarities", 0] },
                'accepted' : {
                   '$let': {
                       'vars': {
                          'first': { '$arrayElemAt': [ "$polarities", 0] },
                       },
                       'in': { 
                            '$reduce' : {
                                'input': "$polarities",
                                'initialValue': True,
                                'in': { '$and': ["$$value", { '$eq' : ["$$this", "$$first" ]}] }
                            } 
                        }
                    }
                },
                'polarities' : "$polarities"
            }
        },
        { '$match' : { 'accepted': True, 'corpus_len' : { '$gte' : min_matches } } }
    ] 

    if filter_neutral:
        query.append({ '$match' : {'pol': {'$ne': '0'} } })
        
    query.extend([
        { '$project' : {'_id': 0, 'accepted' : 0} },
        { '$sort' : { 'corpus_len' : -1 } }
    ])
    
    if limit:
       query.append({ '$limit': limit }) 
       
    return list(db.reviews.aggregate(query))


def get_indep_lex_rules(treshold=0.9):
    items = db.reviews.find({})
    balance = int( round( sum( item['category'] for item in items ) / items.count() ) )
    words = db.reviews.aggregate([
        { '$project': { '_id':0,'text':1, 'category':1 } },
        { '$unwind': '$text' },
        { '$project': {'lemma':'$text.lemma', 'category':1 } },
        { '$group' : { 
                '_id': '$category', 
                'tokens': { '$push': '$lemma' } 
           } 
        }
    ])
    print balance;raw_input()
    pass


def get_vocabulary():
    return list(db.reviews.aggregate([
        { '$project': { '_id':0,'text':1 } },
        { '$unwind': "$text" },
        { '$project': { 'lemma':'$text.lemma', 'word':'$text.word' } }
    ]))


replacements = [
    (u'á',u'a'),(u'é',u'e'),(u'í',u'i'),(u'ó',u'o'),(u'ú',u'u'),
    (u'a',u'á'),(u'e',u'é'),(u'i',u'í'),(u'o',u'ó'),(u'u',u'ú')
]
combinations = sum([map(list, combinations(replacements, i+1)) for i in range(len(replacements))], [])
stats = { "ByWord":0,"BySingular":0,"ByLemma":0,"ByWordCorrection" :0,"ByLemmaCorrection":0,"IsNull":0,"Fails":0,"Total":0 }

def update_embeddings(
        femb='../../embeddings/emb39-word2vec.npy',
        ftok='../../embeddings/emb39-word2vec.txt',
        verbose=False
    ):
    
    index_for   = { token.lower().replace("_",""):index for index, token in enumerate(open(ftok).read().splitlines()) }
    embeddings  = np.load(femb)
    vector_size = len(embeddings[0])
    nullvector  = np.zeros(vector_size) 
    
    
    def get_vectors(word,lemma):
        
        word = word.lower()
            
        stats['Total'] += 1
        
        if index_for.has_key(word):
            stats['ByWord'] += 1
            return word , embeddings[ index_for[ word ] ] 
        
        if index_for.has_key(word[:-1]):
            stats['BySingular'] += 1
            return word , embeddings[ index_for[ word[:-1] ] ]  
        
        if index_for.has_key(lemma):
            stats['ByLemma'] += 1 
            return lemma , embeddings[ index_for[ lemma ] ]
        
        
        vector = nullvector
        tokens = word.split('_')
        left = len(tokens)
        for token in tokens:            
            for combination in combinations:                    
                for fr,to in combination:
                    token = token.replace(fr,to)
                if index_for.has_key(token):
                    vector += embeddings[ index_for[ token ] ]
                    left -= 1 
        if left <= 1:
            stats['ByWordCorrection'] += 1
            return word , vector                    
        
        vector = nullvector
        tokens = lemma.split('_')
        left = len(tokens)
        for token in tokens:            
            for combination in combinations:                    
                for fr,to in combination:
                    token = token.replace(fr,to)
                if index_for.has_key(token):
                    vector += embeddings[ index_for[ token ] ]
                    left -= 1 
        if left <= 1:
            stats['ByLemmaCorrection'] += 1
            return lemma , vector
        
        stats['IsNull'] += 1
        return word , nullvector 
    
        
    result = {}
    vocabulary = get_vocabulary()
    total = len(vocabulary)
    
    for idx,item in enumerate(vocabulary):
        progress("Updating embeddings",total,idx)
        word  = item['word']
        lemma = item['lemma'] 
        if result.has_key(word) or result.has_key(lemma):
            continue
        token,vector = get_vectors(word,lemma)
        result.update({ token:vector })
    
    if verbose:    
        for case in stats: print "%-17s : %i (%4.2f%%)" % (case,stats[case],100.0*stats[case]/stats['Total'])
        raw_input()
    
    result = [{ 'token':item, 'embedding':result[item].tolist() } for item in result]
    db.embeddings.insert_many(result)

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    get_indep_lex_rules()


