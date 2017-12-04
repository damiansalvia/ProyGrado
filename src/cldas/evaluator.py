# -*- encoding: utf-8 -*-
'''
Module of evaluation by using a rustic classifier and standard metrics

@author: Nicolás Mechulam, Damián Salvia
'''

import utils.metrics as metrics


class Classifier:

    def __init__(self, lexicon):
        self.lexicon = lexicon

    def __call__(self, review):
        sentiment = 0
        for token in review['text']:
            inv = -1 if token['negated'] else 1
            val = self.lexicon.get( token['lemma'], {} ).get('val',0)
            sentiment += val * inv 

        if sentiment > 0.3:
            return 1
        elif sentiment > -0.3:
            return 0
        else:
            return -1



def get_polarity(review):
    cat = review.get('category')
    if cat > 65:
        return 1
    elif cat > 35:
        return 0
    else:
        return -1



def get_precision(y_true, y_pred, val):
    true_pos  = sum(x and y for (x,y) in zip(y_true,y_pred) ) 
    retrived = sum(y_pred)
    return true_pos / retrived if retrived > 0 else 0

def get_recall(y_true, y_pred, val):
    true_pos  = sum(x == val and y == val for (x,y) in zip(y_true,y_pred) ) 
    retrived = sum( x == val for (x,y) in zip(y_true,y_pred) )
    return true_pos / retrived if retrived > 0 else 0

def get_fmesure(y_true, y_pred, val, beta = 1):
    p = get_precision (y_true,y_pred, val)
    r = get_recall(y_true,y_pred, val)
    if p > 0 or r > 0:
        return (1 + beta**2) * ( ( p * r ) / (beta**2 * p + r) )
    else:
        return 0

def get_accuracy(y_true, y_pred):
    length = len(y_true)
    if length > 0:
        return sum(y_true[idx] == y_pred[idx] for idx in range(length) ) / length
    else:
        return 0



def evaluate(lexicon, reviews):
    classifier = Classifier(lexicon)
    y_true = [ get_polarity(x) for x in reviews]
    y_pred = [ classifier(x) for x in reviews]

    result = {}

    # Positive
    result['positive_precision'] = metrics.precision(
        map(lambda x : x == 1, y_true),
        map(lambda x : x == 1, y_pred)
    )
    result['positive_recall'] = metrics.recall(
        map(lambda x : x == 1, y_true),
        map(lambda x : x == 1, y_pred)
    )
    result['positive_fmesure'] = metrics.fmeasure(
        map(lambda x : x == 1, y_true),
        map(lambda x : x == 1, y_pred)
    )

    # Neutral
    result['neutral_precision'] = metrics.precision(
        map(lambda x : x == 0, y_true),
        map(lambda x : x == 0, y_pred)
    )
    result['neutral_recall'] = metrics.recall(
        map(lambda x : x == 0, y_true),
        map(lambda x : x == 0, y_pred)
    )
    result['neutral_fmesure'] = metrics.fmeasure(
        map(lambda x : x == 0, y_true),
        map(lambda x : x == 0, y_pred)
    )

    # Negative
    result['negative_precision'] = metrics.precision(
        map(lambda x : x == -1, y_true),
        map(lambda x : x == -1, y_pred)
    )
    result['negative_recall'] = metrics.recall(
        map(lambda x : x == -1, y_true),
        map(lambda x : x == -1, y_pred)
    )
    result['negative_fmesure'] = metrics.fmeasure(
        map(lambda x : x == -1, y_true),
        map(lambda x : x == -1, y_pred)
    )

    result['accuracy']           = get_accuracy(y_true, y_pred)

    result['average_precision']  = \
        (result['positive_precision'] + result['neutral_precision'] + result['negative_precision']) / 3
    result['average_recall']     = \
        (result['positive_recall'] + result['neutral_recall'] + result['negative_recall']) / 3
    result['average_fmesure']    = \
        (result['positive_fmesure'] + result['neutral_fmesure'] + result['negative_fmesure']) / 3

    return result

