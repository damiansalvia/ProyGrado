# -*- encoding: utf-8 -*-
'''
Module for getting statistics over the dataset 

@author: Nicolás Mechulam, Damián Salvia
'''
from cldas.db.crud import db


# ----------------------------------------------------------------------------------------------------------------------

def size_corporea():
    return db.reviews.find(
        {}
    ).count()


def size_corporea_by_source():
    return list( db.reviews.aggregate([
        {"$group"   : { "_id":"$source", "count":{ "$sum":1 } }},
        {"$project" : {"_id":0, "source":"$_id", "count":1}}
    ]) )    


# ----------------------------------------------------------------------------------------------------------------------

def size_vocabulary():
    return list( db.reviews.aggregate([
        {"$group":{"_id":None,"count":{"$sum":{"$size":"$text"}}}}
    ]) )[0]['count']

    
def size_vocabulary_by_word():
    return len( db.reviews.distinct("text.word") )


def size_vocabulary_by_lemma():
    return len( db.reviews.distinct("text.lemma") )

# ----------------------------------------------------------------------------------------------------------------------

def avg_tokens_by_source():
    return list( db.reviews.aggregate([
        {"$group"   : { "_id":"$source", "count":{ "$avg":{"$size":"$text"} } }},
        {"$project" : {"_id":0, "source":"$_id", "count":1}}
    ]) )

# ----------------------------------------------------------------------------------------------------------------------

def size_reviews_category():
    return list( db.reviews.aggregate([
        {"$group":{ "_id":"$category", "count":{ "$sum":1 } }},
        {"$project" : {"_id":0, "category":"$_id", "count":1}}
    ]) )

# ----------------------------------------------------------------------------------------------------------------------

def size_manually_tagged():
    try: 
        return list( db.reviews.aggregate([
            {'$match' : {'tagged': 'manually'} },
            {'$unwind': '$text'},
            {'$group': {
                '_id': None, 
                'total': { '$sum' : 1 }
                } 
            }
        ]) )[0]['total']
    except:
        return None


def size_manually_tagged_by_cat():
    try: 
        return list( db.reviews.aggregate([
            {'$match' : {'tagged': 'manually'} },
            {'$unwind': '$text'},
            {'$group': {
                '_id': '$source', 
                'total': { '$sum' : 1 }
                } 
            },
            {'$project' : {'count' :'$total', 'category': '$_id','_id':0}}
        ]) )
    except:
        return None

# ----------------------------------------------------------------------------------------------------------------------

def size_nagated_words():
    return list( db.reviews.aggregate([
        { '$unwind' : '$text' },
        { '$match' : { 'text.negated' : True } },
        { '$group' : { '_id' : "$text.word", 'total' : { '$sum' : 1 } } },
        { '$group' : { '_id':None, 'total':{ '$sum': 1 } } },
    ]) )[0].get('total')


def size_negators():
    return list(db.reviews.aggregate([
        { '$unwind' : '$text' },
        { '$match' : { 'text.negated' :None } },
        { '$group' : { '_id' : "$text.word", 'total' : { '$sum' : 1 } } },
        { '$match' : { 'total' : { '$gt' : 28 } } }, # FIX-ME: BIO-tag is wrong, but high-frequency words are negators
        { '$group' : { '_id':None, 'total':{ '$sum': 1 } } },
    ]) )[0]['total']

# ----------------------------------------------------------------------------------------------------------------------

def size_neutral_reviews():
    return db.reviews.find(
        { 'category' : { '$gt': (100/3)*1, '$lt': (100/3)*2 } }
    ).count()


def size_positive_reviews():
    return db.reviews.find(
        { 'category' : { '$gte': (100/3)*2 } }
    ).count()


def size_negative_reviews():
    return db.reviews.find(
        { 'category' : { '$lte': 100/3 } }
    ).count()    

# ----------------------------------------------------------------------------------------------------------------------

def size_neutral_words():
    return list( db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$gt' : 100/3, '$lt' : (100/3)*2  } } },
        { '$group': {'_id':None, 'total': {'$sum':1} } }
    ]) )[0]['total']


def size_positive_words():
    return list( db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$gte' : (100/3)*2 } } },
        { '$group': {'_id':None, 'total': {'$sum':1} } }
    ]) )[0]['total']


def size_negative_words():
    return list( db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$lte' : 100/3 } } },
        { '$group': {'_id':None, 'total': {'$sum': 1} }}
    ]) )[0]['total']    

# ----------------------------------------------------------------------------------------------------------------------

def get_balance():
    return list( db.reviews.aggregate([
        {'$group': {
            '_id': None, 
            'size': { '$sum' : 1 },
            'total': { '$sum' : '$category' }
            } 
        },
        {'$project': {'balance': {'$divide' :['$total','$size'] } } }
    ]) )[0]['balance']  


def get_balance_by_source() :
    return list( db.reviews.aggregate([
        {'$group': {
            '_id': '$source', 
            'size': { '$sum' : 1 },
            'total': { '$sum' : '$category' }
            } 
        },
        {'$project': {'count': {'$divide' : ['$total','$size'] }, "source":"$_id", "_id":0 } }
    ]) )

# ----------------------------------------------------------------------------------------------------------------------

def size_embeddings():
    return db.embeddings.find(
        {}
    ).count()


def size_embeddings_used():
    return db.embeddings.find({
        "similars": { "$ne" : [] }
    }).count()


def size_embeddings_unused():
    return db.embeddings.find({
        "similars" : []
    }).count()


def size_embeddings_exact_match():
    return list( db.embeddings.aggregate([
        { "$unwind" : "$similars" },
        { "$project" : {'_id':1, 'similars':1, 'equals':{ '$eq': [ '$_id', '$similars' ] } } },
        { "$match" : { "equals" : True } },
        { "$group" : { "_id" : None, "total" : { "$sum" : 1 } } }
    ]) )[0]['total']


def size_embeddings_near_match():
    return list( db.embeddings.aggregate([
        { "$unwind" : "$similars" },
        { "$project" : {'_id':1, 'similars':1, 'equals':{ '$eq': [ '$_id', '$similars' ] } } },
        { "$match" : { "equals" : False } },
        { "$group" : { "_id" : None, "total" : { "$sum" : 1 } } }
    ]) )[0]['total']


def size_embeddings_null_match():
    return list( db.embeddings.aggregate([
        { '$match' : { "_id" : "__null__" } },
        { '$project': { "total" : { '$size' : '$similars' } } }
    ]) )[0]['total']


