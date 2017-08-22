 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError



print "Connecting Mongo database"
try:
    client = MongoClient(serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client.ProyGrado
except ServerSelectionTimeoutError:
    raise Exception("Couldn't connect Mongo database")


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

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    negations = {
        '72355624354ff30d03038b818044ac46': [False, False],
        '97609c4dd3e893bce2c035bea586bbdd': [False, True, True, True, True, False, False, False, False, False], #10
        'd93708dbb4ebc3e6711118ef20a77669': [ False, True, True, False], #4
    } 
    save_negations(negations)



