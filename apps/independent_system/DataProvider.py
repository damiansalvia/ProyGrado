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

        
        
def save_opinions(opinions):
    if opinions:
        db.reviews.insert_many(opinions)


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
    

def get_indepentent_lex(limit=None, tolerance=0.0, filter_neutral=False):
    sources_qty = len( get_sources() )
    min_matches = int(round(sources_qty*(1.0-tolerance),0))
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


def get_indepentent_lex2(limit=None, tolerance=0.0, filter_neutral=False):
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


def get_indep_lex_by_rules(treshold=0.9):
    balance = get_stat_balanced()
    words = db.reviews.aggregate([
            { '$project': { '_id':0,'text':1, 'category':1 } },
            { '$unwind': '$text' },
            { '$project': {
                    'lemma':'$text.lemma', 
                    'category':{ 
                        '$cond' : { 
                            'if':'$text.negated', 
                            'then':{'$subtract': [100,'$category']}, 
                            'else':'$category' 
                        } 
                    } 
                } 
            }
    ])
    pass


def get_vocabulary(get_by=None):
    query = [
        { '$project': { '_id':0,'text':1 } },
        { '$unwind': "$text" }
    ]
    if not get_by:
        query.append( { '$project': { 'lemma':'$text.lemma', 'word':'$text.word' } } )
    elif get_by not in ["word","lemma"]:
        raise Exception("Values for get_by parameter must be 'word' or 'lemma'")
    else:
        query.append( { '$project': { get_by:'$text.%s'%get_by} } )
    return list( db.reviews.aggregate(query) )


def update_embeddings(
        femb='../../embeddings/emb39-word2vec.npy',
        ftok='../../embeddings/emb39-word2vec.txt',
        split_tolerance=1,
        verbose=False
    ):
    
    replacements = [
        (u'á',u'a'),(u'é',u'e'),(u'í',u'i'),(u'ó',u'o'),(u'ú',u'u'),(u'ü',u'u'),
        (u'a',u'á'),(u'e',u'é'),(u'i',u'í'),(u'o',u'ó'),(u'u',u'ú'),(u'u',u'ü')
    ]
    alternatives = sum([map(list, combinations(replacements, i+1)) for i in range(len(replacements))], [])
    stats = { "ByWord":0,"BySingular":0,"ByLemma":0,"ByWordCorrection" :0,"IsNull":0,"Fails":0,"Total":0 }
    
    content     = open(ftok).read().lower().replace("_","")    
    index_for   = { token:index for index, token in enumerate(content.splitlines()) }
    embeddings  = np.load(femb)
    vector_size = len(embeddings[0])
    nullvector  = np.zeros(vector_size) 
    
    
    def get_vectors(word,lemma):
        
        stats['Total'] += 1
        
        if index_for.has_key(word):
            stats['ByWord'] += 1
            return embeddings[ index_for[ word ] ] 
        
        singular = word[:-1]
        if index_for.has_key(singular):
            stats['BySingular'] += 1
            return embeddings[ index_for[ singular ] ]  
          
        if index_for.has_key(lemma):
            stats['ByLemma'] += 1 
            return embeddings[ index_for[ lemma ] ]
#          
#         vector = nullvector.copy()
#         tokens = word.split('_')
#         left = len(tokens)
#         for token in tokens:            
#             for replace_set in alternatives: 
#                 correct = token                   
#                 for fr,to in replace_set:
#                     correct = correct.replace(fr,to)
#                 if index_for.has_key(correct):
#                     vector += embeddings[ index_for[ correct ] ]
#                     left -= 1 
#                     break # Try next token
#         if left <= split_tolerance:
#             stats['ByWordCorrection'] += 1
#             return vector   
            
        for replace_set in alternatives: 
            correct = token                   
            for fr,to in replace_set:
                correct = correct.replace(fr,to)
            if index_for.has_key(correct):
                return embeddings[ index_for[ correct ] ]                 
        
        stats['IsNull'] += 1
        return nullvector 
    
        
    result = {}
    vocabulary = get_vocabulary()
    total = len(vocabulary)
    
    for idx,item in enumerate(vocabulary):
        progress("Updating embeddings",total,idx)
        word  = item['word'].lower()
        lemma = item['lemma'].lower()
        if result.has_key(word):
            continue
        vector = get_vectors( word , lemma )
        result.update({ word:vector })
    
    if stats['Total']:
        for case in stats:
            log("Embeddings integration. %s : %i (%4.2f%%)" % (case,stats[case],100.0*stats[case]/stats['Total']),level='info')     
            if verbose: print "%-17s : %i (%4.2f%%)" % (case,stats[case],100.0*stats[case]/stats['Total']) 
        if verbose: raw_input("Press enter to continue...")    
    
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


