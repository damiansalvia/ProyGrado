# -*- coding: utf-8 -*-
import sys
sys.path.append('../utilities')
from utilities import *

from DataProvider import db
import DataProvider as dp
import numpy as np


SOURCE = 'corpus_apps_android'
output_dir = 'outputs/tmp/'



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
                polarities[vocabulary[idx]] = '+'
            else:
                polarities[vocabulary[idx]] = '-'

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
    print ' ----------------------------- MATRICES -----------------------------'
    print get_indepentent_lexicon_by_polarity_matrices(limit=20, tolerance=0.8)
    print ' ----------------------------- AVERAGE ------------------------------'
    print get_indepentent_lexicon_by_average(limit=20, tolerance=0.8)
    print ' ------------------------- WEIGHT FUNCTION --------------------------'
    print get_indepentent_lexicon_by_weight_function(limit=20, tolerance=0.8)