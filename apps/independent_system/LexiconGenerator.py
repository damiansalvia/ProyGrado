# -*- coding: utf-8 -*-
import sys
from _collections import defaultdict
sys.path.append('../utilities')
from utilities import *

from DataProvider import db
import DataProvider as dp
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


SOURCE = 'corpus_apps_android'
output_dir = 'outputs/tmp/'


def get_indepentent_lexicon_by_senti_tfidf(limit=None,useNeg=True,tolerance=0.0,threshold=1e-3):
    
    reviews = db.reviews.find({})
    
    lemmas  = db.reviews.distinct("text.lemma")
    index = { lemma:idx for idx,lemma in enumerate(lemmas) }
    size = len(index)
    
    pos_reviews = db.reviews.find({"category":{ "$gt":50 }})
    neg_reviews = db.reviews.find({"category":{ "$lt":50 }})
    
    P = pos_reviews.count() * 1.0
    N = neg_reviews.count() * 1.0
    
    Pctd = np.zeros(size)
    Pt   = np.zeros(size)
    Nctd = np.zeros(size)
    Nt   = np.zeros(size)
    
    total = pos_reviews.count() + neg_reviews.count()
    
    for idx,review in enumerate(pos_reviews):
        progress("Building Senti-TFIDF matrix",total,idx)
        visited = defaultdict(lambda:0)
        for item in review['text']: 
            visited[ item['lemma'] ] += 1
        for i,lemma in enumerate(visited.keys()):
            value = visited[lemma]
            negated = useNeg and review['text'][i].has_key('negated') and review['text'][i]['negated']
            Pctd[ index[lemma] ] += value if not negated else 0
            Pt  [ index[lemma] ] += 1 if not negated else 0
            Nctd[ index[lemma] ] += value if negated else 0
            Nt  [ index[lemma] ] += 1 if negated else 0
            
    offset = idx
    
    for idx,review in enumerate(neg_reviews):
        progress("Building Senti-TFIDF matrix",total,offset+idx)
        visited = defaultdict(lambda:0)
        for item in review['text']: 
            visited[ item['lemma'] ] += 1
        for i,lemma in enumerate(visited.keys()):
            value = visited[lemma]
            negated = useNeg and review['text'][i].has_key('negated') and review['text'][i]['negated']
            Nctd[ index[lemma] ] += value if not negated else 0
            Nt  [ index[lemma] ] += 1 if not negated else 0
            Pctd[ index[lemma] ] += value if negated else 0
            Pt  [ index[lemma] ] += 1 if negated else 0
    
    POSt = Pctd * np.log2(P/(Pt+1e-10))
    NEGt = Nctd * np.log2(N/(Nt+1e-10))
    
    LDT = np.log2( (POSt+1e-4) / (NEGt+1e-4) )
    where_are_NaNs = np.isnan(LDT)
    LDT[where_are_NaNs] = 0.0
    
    lexicon = {lemmas[idx]:pol for idx,pol in enumerate(LDT)}
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda x: abs(x[1]), reverse=True)[:limit] )
            
    for lemma in lexicon:
        pol = lexicon[lemma]
        if pol < -threshold:
            lexicon[ lemma ] = "NEG"
        elif pol > threshold:
            lexicon[ lemma ] = "POS"
        else:
            lexicon[ lemma ] = "NEU"
            
    return lexicon
     

# -----------------------------------------------------------------------------------------------------------

def get_indepentent_lexicon_by_polarity_matrices(limit=None, tolerance=0.0, window_left=2 , window_right=2):

    def get_vectors(text, window_left, window_right):
        vectors = []
        for idx, word in enumerate(text):
            vec = []
            for i in range(window_left + window_right + 1):
                if window_left != i:
                    vec.append(get_entry(text, idx - window_left + i))
                else:
                    target = get_entry(text, idx - window_left + i)
            vectors.append((target,vec))
        return vectors

    def get_entry(text, idx):
        if  0 <= idx < len(text) :
            return (text[idx]['lemma'], text[idx].get('negated',False)) 
        else:
            return None

    def get_matrices(source, vocabulary):
        vocabulary_size = len(vocabulary)
        pos_matrix = np.zeros((vocabulary_size,vocabulary_size))
        neg_matrix = np.zeros((vocabulary_size,vocabulary_size))
        opinions = dp.get_opinions(source)
        total = opinions.count()
        for idx, op in enumerate(opinions):
            progress("Building matrix for %s" % source,total,idx)
            cat = op['category']
            vectors = get_vectors(op['text'], window_left, window_right) 
            for v in vectors:
                target  = v[0]
                context = v[1]
                target_cat = 100 - cat if target[1] else cat
                for w in context:
                    if w:
                        if target_cat > 50:
                            pos_matrix[vocabulary.index(target[0])][vocabulary.index(w[0])] += target_cat - 50
                        else:
                            neg_matrix[vocabulary.index(target[0])][vocabulary.index(w[0])] += 50 - target_cat
        return pos_matrix, neg_matrix

    def all_equal(list):
        return all(map(lambda x: x == list[0], list))

    sources = dp.get_sources()
    sources_qty = len(sources)
    min_matches = int(round(sources_qty*(1.0-tolerance),0))
    polarities = {}
    for source in sources:
        vocabulary = [ elem['_id'] for elem in dp.get_soruce_vocabulary(source)]
        pos_matrix, neg_matrix = get_matrices(source, vocabulary)
        total = len(pos_matrix)
        for idx in range(total):
            progress("Assigning polarities in words for %s" % source,total,idx)
            if np.linalg.norm(pos_matrix[idx]) - np.linalg.norm(neg_matrix[idx]) > 0:
                polarities[vocabulary[idx]] = 'POS'
            else:
                polarities[vocabulary[idx]] = 'NEG'

    return { pol: polarities[pol][0] \
        for pol in polarities.keys() if len(polarities[pol])>= min_matches and all_equal(polarities[pol])}
  

#--------------------------------------------------------------------------------------


def get_indepentent_lexicon_by_average(limit=None, tolerance=0.0, filter_neutral=False):
    sources_qty = len( dp.get_sources() )
    min_matches = int(round(sources_qty*(1.0-tolerance),0))
    query = [
        { '$unwind' : '$text' },{ 
            '$group': {
                '_id'  : { 'source': '$source', 'lemma': '$text.lemma'},
                'sent' : { '$avg' : { 
                        '$cond' : {
                            'if'  :  '$text.negated',
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
                            {'case' : { '$gte' : ['$sent', 60] }, 'then': 'POS'},    
                            {'case' : { '$lte' : ['$sent', 30] }, 'then': 'NEG'},    
                            {'case' : True, 'then': 'NEU'},    
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
        query.append({ '$match' : {'pol': {'$ne': 'NEU'} } })
        
    query.extend([
        { '$project' : {'_id': 0, 'accepted' : 0} },
        { '$sort' : { 'corpus_len' : -1 } }
    ])
    
    if limit:
       query.append({ '$limit': limit }) 
    
    result = list(db.reviews.aggregate(query))
    return {item['lemma']:item['pol'] for item in result} 

#--------------------------------------------------------------------------------------


def get_indepentent_lexicon_by_weight_function(limit=None, tolerance=0.0, filter_neutral=False):
    sources_qty = len( dp.get_sources() )
    min_matches = int(round(sources_qty*(1.0-tolerance),0))
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
                            {'case' : { '$gt' : ['$sent', 0] }, 'then': 'POS'},    
                            {'case' : { '$lt' : ['$sent', 0] }, 'then': 'NEG'},    
                            {'case' : True, 'then': 'NEU'},    
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
        query.append({ '$match' : {'pol': {'$ne': 'NEU'} } })
        
    query.extend([
        { '$project' : {'_id': 0, 'accepted' : 0} },
        { '$sort' : { 'corpus_len' : -1 } }
    ])
    
    if limit:
       query.append({ '$limit': limit }) 
       
    result = list(db.reviews.aggregate(query))
    return {item['lemma']:item['pol'] for item in result} 


#--------------------------------------------------------------------------------------


def get_independent_lexicon_by_rules(treshold=0.9):
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


#--------------------------------------------------------------------------------------


if __name__ == '__main__':
    print ' --------------------------- SENTI-TFIDF ----------------------------'
    print get_indepentent_lexicon_by_senti_tfidf(limit=20,threshold=0.1)
    print ' ----------------------------- MATRICES -----------------------------'
    print get_indepentent_lexicon_by_polarity_matrices(limit=20, tolerance=0.8)
    print ' ----------------------------- AVERAGE ------------------------------'
    print get_indepentent_lexicon_by_average(limit=20, tolerance=0.8)
    print ' ------------------------- WEIGHT FUNCTION --------------------------'
    print get_indepentent_lexicon_by_weight_function(limit=20, tolerance=0.8)