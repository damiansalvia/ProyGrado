# -*- encoding: utf-8 -*-
'''
Module for getting statistics over the dataset 

@author: Nicolás Mechulam, Damián Salvia
'''
from cldas.db.crud import db


_CUSTOM_NEGATORS_LIST = [
    u'aunque', u'denegar', u'jamás', u'nada', u'nadie', u'negar',u'negativa', 
    u'ni', u'ninguna', u'ninguno', u'ningún',u'no', u'nunca', u'pero', u'rehúso', 
    u'tampoco'
]


# Review sizes
def size_corporea():
    return db.reviews.find(
        {}
    ).count()


def size_corporea_by_source():
    return list( db.reviews.aggregate([
        {"$group"   : { "_id":"$source", "count":{ "$sum":1 } }},
        {"$project" : {"_id":0, "source":"$_id", "count":1}}
    ]) )


# Vocabulary sizes
def size_vocabulary():
    return list( db.reviews.aggregate([
        {"$group":{"_id":None,"count":{"$sum":{"$size":"$text"}}}}
    ]) )[0]['count']

    
def size_vocabulary_by_word():
    return len( db.reviews.distinct("text.word") )


def size_vocabulary_by_lemma():
    return len( db.reviews.distinct("text.lemma") )


def size_embeddings():
    return db.embeddings.find(
        {}
    ).count()


# Reviews per category
def size_reviews_category():
    return list( db.reviews.aggregate([
        {"$group":{ "_id":"$category", "count":{ "$sum":1 } }},
        {"$project" : {"_id":0, "category":"$_id", "count":1}}
    ]) )


# Tagged sizes
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
            {'$project' : {'total' :'$total', 'category': '$_id','_id':0}}
        ]) )
    except:
        return None


# Count all negated words  
def size_nagated_words():
    return list( db.reviews.aggregate([{
            '$group' : {
                '_id' : None,
                'total': { 
                    '$sum' : { 
                        '$size' : {
                            '$filter' : {
                                'input' : "$text",
                                'as' : "word",
                                'cond' : "$$word.neg"
                            }
                        } 
                    }
                }
            }   
        }
    ]) )[0].get('total')


# Count negatives reviews
def size_negative_reviews():
    return db.reviews.find(
        { 'category' : { '$lte': 100/3 } }
    ).count()


# Count negative words
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


# Count negators -- NO FUNCIONA, NO SE POR QUE 
def size_negators(negators = NEGATORS ):
    return list(db.reviews.aggregate([
        {
            '$group' : {
                '_id' : None,
                'total': { 
                    '$sum' : { 
                        '$size' : {
                            '$filter' : {
                                'input' : "$text",
                                'as' : "w",
                                'cond' : { '$in' : [ {'$toLower': "$$w.word"}, negators ] }
                            }
                        } 
                    }
                }
            }   
        }
    ]) )[0]['total']


# Count neutral reviews
def size_neutral_reviews():
    return db.reviews.find(
        { 'category' : { '$gt': (100/3)*1, '$lt': (100/3)*2 } }
    ).count()


#  Count neutral words
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


# count positive reviews
def size_positive_reviews():
    return db.reviews.find(
        { 'category' : { '$gte': (100/3)*2 } }
    ).count()

# Count positive words
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
        {'$project': {'balance': {'$divide' :['$total','$size'] } } }
    ]) )


def size_near_match():
    return db.embeddings.find(
        { "nearestOf":{'$ne':None} }
    ).count()


def size_null_match():
    return db.embeddings.find(
        { "embedding":{ '$all':[0.0] } }
    ).count()


def size_exact_match():
    return db.embeddings.find(
        {"embedding":
            { "$not": { '$all':[0.0] } }, 
            "nearestOf": {'$eq':None }
    }).count()


