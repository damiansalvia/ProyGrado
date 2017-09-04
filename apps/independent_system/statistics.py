 # -*- coding: utf-8 -*-
from DataProvider import db

NEGATORS = [
    u'aunque', u'denegar', u'jamás', u'nada', u'nadie', u'negar',u'negativa', 
    u'ni', u'ninguna', u'ninguno', u'ningún',u'no', u'nunca', u'pero', u'rehúso', 
    u'tampoco'
]


# ----------------------------------------- source -----------------------------------------


def size_corporea():
    return db.reviews.find({}).count()

def size_embeddings():
    return db.embeddings.find({}).count()

def size_manually_tagged():
    try: 
        return list(db.reviews.aggregate([
            {'$match' : {'tagged': 'manually'} },
            {'$unwind': '$text'},
            {'$group': {
                '_id': None, 
                'total': { '$sum' : 1 }
                } 
            }
        ]))[0]['total']
    except:
        return 0

def size_manually_tagged_by_cat():
    try: 
        return list(db.reviews.aggregate([
            {'$match' : {'tagged': 'manually'} },
            {'$unwind': '$text'},
            {'$group': {
                '_id': '$source', 
                'total': { '$sum' : 1 }
                } 
            },
            {'project' : {'total' :'$total', 'category': '$_id'}}
        ]))
    except:
        return 0

# Count all negated words  
def size_nagated_words():
    return list(db.reviews.aggregate([{
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
    ]))[0].get('total')

# Count negatives reviews
def size_negative_reviews():
    return db.reviews.find({
        'category' : { '$lte': 100/3 }
    }).count()

# Count negative words
def size_negative_words():
    return list(db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$lte' : 100/3 } } },
        { '$group': {'_id':None, 'total': {'$sum': 1} }}
    ]))[0]['total']

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
    ]))[0]['total']

# Count neutral reviews
def size_neutral_reviews():
    return db.reviews.find({
        'category' : { '$gt': (100/3)*1, '$lt': (100/3)*2 }
    }).count()

#  Count neutral words
def size_neutral_words():
    return list(db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$gt' : 100/3, '$lt' : (100/3)*2  } } },
        { '$group': {'_id':None, 'total': {'$sum':1} } }
    ]))[0]['total']

# count positive reviews
def size_positive_reviews():
    return db.reviews.find({
        'category' : { '$gte': (100/3)*2}
    }).count()

# Count positive words
def size_positive_words():
    return list(db.reviews.aggregate([
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "category" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$category" }
        }},
        { '$match' : { "sen" : { '$gte' : (100/3)*2 } } },
        { '$group': {'_id':None, 'total': {'$sum':1} } }
    ]))[0]['total']

# Vocabulary size:
def size_vocabulary():
    return db.reviews.distinct("text.word").count()

def size_vocabulary_by_lemma():
    return db.reviews.distinct("text.lemma").count()

def get_balance():
    return list(db.reviews.aggregate([
        {'$group': {
            '_id': None, 
            'size': { '$sum' : 1 },
            'total': { '$sum' : '$category' }
            } 
        },
        {'$project': {'balance': {'$divide' :['$total','$size'] } } }
    ]))[0]['balance']  

def get_balance_by_source() :
    return list(db.reviews.aggregate([
        {'$group': {
            '_id': '$source', 
            'size': { '$sum' : 1 },
            'total': { '$sum' : '$category' }
            } 
        },
        {'$project': {'balance': {'$divide' :['$total','$size'] } } }
    ]))



def size_loose_match():
    return db.embeddings.find({"nearestOf":{'$ne':None}}).count()

def size_null_embedings():
    return db.embeddings.find({"embedding":{ '$all':[0.0]}}).count()

def size_exact_match_embeddins():
    return db.embeddings.find({"embedding":{ "$not":{ '$all':[0.0]} }, "nearestOf":{'$eq':None}}).count()

#=====================================================================================================
if __name__ == "__main__":

    # print 'Size nagated words', size_nagated_words()
    print 'Size negative words', size_negative_words()
    print 'Size negators', size_negators()
    print 'Size neutral reviews', size_neutral_reviews()
    print 'Size neutral words', size_neutral_words()
    print 'Size positive reviews', size_positive_reviews()
    print 'Size positive words', size_positive_words()
    print 'Size vocabulary', size_vocabulary()
    print 'Size manually tagged', size_manually_tagged()
    print 'Size corporea', size_corporea()
    print 'Size embeddings', size_embeddings()
    print 'Size manually tagged', size_manually_tagged()
    print 'Size manually tagged by cat', size_manually_tagged_by_cat()
    print 'Get balance', get_balance()
    print 'Get balance by source', get_balance_by_source() 
    print 'Size loose match embedings' , size_loose_match()
    print 'Size null embedings' , size_null_embedings()
    print 'Size exact match embeddins' , size_exact_match_embeddins()