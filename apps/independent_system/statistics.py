from DataProvider import db


# ----------------------------------------- source -----------------------------------------

# Count all negated words  
def size_nagated_words():
    return db.reviews.aggregate([{
            '$match' : { "source" : "source_test.json" }
        },{
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
    ])

# Count negatives reviews
def size_negative_reviews():
    return db.reviews.find({
        'source' : "source_test.json",
        'sentiment' : { '$lte': 100/3 }
    }).count()

# Count negative words
def size_negative_words():
    return db.reviews.aggregate([
        { '$match' : { "source" : "source_test.json" } },
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "sentiment" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$sentiment" }
        }},
        { '$match' : { "sen" : { '$lte' : 100/3 } } }
    ])

# Count negators -- NO FUNCIONA, NO SE POR QUE 
def size_negators():
    return db.reviews.aggregate([
        { '$match' : { "source" : "source_test.json" } },
        {
            '$group' : {
                '_id' : None,
                'total': { 
                    '$sum' : { 
                        '$size' : {
                            '$filter' : {
                                'input' : "$text",
                                'as' : "w",
                                'cond' : { '$in' : [ {'$toLower': "$$w.word"},[
                                    "aunque", "denegar", "jamás", "nada", "nadie", "negar","negativa", 
                                    "ni", "ninguna", "ninguno", "ningún","no", "nunca", "pero", "rehúso", 
                                    "tampoco"
                                ] ] }
                            }
                        } 
                    }
                }
            }   
        }
    ])

# Count neutral reviews
def size_neutral_reviews():
    return db.reviews.find({
        'source' : "source_test.json",
        'sentiment' : { '$gt': (100/3)*1, '$lt': (100/3)*2 }
    }).count()

#  Count neutral words
def size_neutral_words():
    return db.reviews.aggregate([
        { '$match' : { "source" : "source_test.json" } },
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "sentiment" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$sentiment" }
        }},
        { '$match' : { "sen" : { '$gt' : 100/3, '$lt' : (100/3)*2  } } }
    ])

# count positive reviews
def size_positive_reviews():
    return db.reviews.find({
        'source' : "source_test.json",
        'sentiment' : { '$gte': (100/3)*2}
    }).count()

# Count positive words
def size_positive_words():
    return db.reviews.aggregate([
        { '$match' : { "source" : "source_test.json" } },
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1 , "sentiment" : 1 , "_id":0  }},
        { '$group' : {
            '_id' : "$text.lemma",
            'sen' : { '$avg' : "$sentiment" }
        }},
        { '$match' : { "sen" : { '$gte' : (100/3)*2 } } }
    ])

# Total reviews
def size_source():
    return db.reviews.find({
        'source' : "source_test.json",
    }).count()

# Vocabulary size:
def size_vocabulary():
    return db.reviews.aggregate([
        { '$match' : { "source" : "source_test" } },
        { '$unwind': "$text" },
        { '$project' : { "text.lemma" : 1, "_id":0  }},
        { '$group' : { '_id' : "$text.lemma" } },
        { '$group' : {'_id':1, 'count': {'$sum' : 1 }}}
    ])


#=====================================================================================================
if __name__ == "__main__":

    print 'Size nagated words', size_nagated_words
    print 'Size negative words', size_negative_words
    print 'Size negative words', size_negative_words
    print 'Size negators', size_negators
    print 'Size neutral reviews', size_neutral_reviews
    print 'Size neutral words', size_neutral_words
    print 'Size positive reviews', size_positive_reviews
    print 'Size positive words', size_positive_words
    print 'Size source', size_source
    print 'Size vocabulary', size_vocabulary