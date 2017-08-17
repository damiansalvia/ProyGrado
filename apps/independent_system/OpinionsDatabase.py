 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities')

from pymongo import MongoClient



print "Connecting Mongo database"
db = MongoClient().ProyGrado



def get_opinion(id):
    return db.reviews.find_one({'_id':id})


def get_by_idx(source, idx):
    return db.reviews.find_one({'source': source, 'idx': idx})


def save_opinions(opinions):
    if opinions:
        db.reviews.insert_many(opinions)


def save_negations(opinions):
    for id in opinions:
        options = { 'tagged' : 'manually' }
        for idx, tag in opinions[id]:
            opinions['text.' + str(idx) + '.negated'] = tag
        db.reviews.update( {'_id': id}, {'$set': options} )


def get_sample(quantity, source, identifiers = None):
    if not identifiers:
        return list(db.reviews.aggregate([ 
            { '$match' : { "source" : source } },
            { '$sample': { 'size': quantity } } 
        ]))
    else:
        return list(db.reviews.find({
            'source': source,
            'idx' :{ '$in': identifiers} 
        }))


def get_tagged(tagger):
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
        { '$match' : { 'accepted': True, 'corpus_len' : { '$gte' : min_matches }, 'pol': {'$ne': '0'} } }
    ] 

    if filter_neutral:
        query.append({ '$match' : {'pol': {'$ne': '0'} } })
        
    query.extend([
        { '$project' : {'_id': 0, 'accepted' : 0} },
        { '$sort' : { 'corpus_len' : -1 } }
    ])
    
    if limit:
       query.append({ '$limit': limit }) 
       
    return db.reviews.aggregate(query)
