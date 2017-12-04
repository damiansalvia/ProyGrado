# -*- encoding: utf-8 -*-
'''
Module with a set of common metrics

@author: Nicolás Mechulam, Damán Salvia
'''
import keras.backend as K
import sklearn.metrics as sk_metrics


def binary_accuracy(y_true, y_pred):
    '''
    Calculates the binary accuracy.
    '''
    return K.mean(K.equal(y_true, K.round(y_pred)), axis=-1)


def cosine_proximity(y_true, y_pred):
    '''
    Calculates the cosine proximity of two vectors.
    '''
    y_true = K.l2_normalize(y_true, axis=-1)
    y_pred = K.l2_normalize(y_pred, axis=-1)
    return -K.mean(y_true * y_pred)


def binary_crossentropy(y_true, y_pred):
    '''
    Calculates the binary cross-entropy.
    '''
    return K.mean(K.binary_crossentropy(y_pred, y_true))


def mean_squared_error(y_true, y_pred):
    '''
    Calculates the mean squered error.
    '''
    return K.mean(K.square(y_pred - y_true))


def precision(y_true, y_pred):
    '''
    Calculates the precision, a metric for multi-label classification of
    how many selected items are relevant.
    '''
    if isinstance(y_pred,list):
        return sk_metrics.precision_score(y_true, y_pred)
    else:
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision


def recall(y_true, y_pred):
    '''
    Calculates the recall, a metric for multi-label classification of
    how many relevant items are selected.
    '''
    if isinstance(y_pred,list):
        return sk_metrics.recall_score(y_true, y_pred)
    else:   
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall


def fbeta_score(y_true, y_pred, beta=1):
    '''
    Calculates the F score, the weighted harmonic mean of precision and recall.
    This is useful for multi-label classification, where input samples can be
    classified as sets of labels. By only using accuracy (precision) a model
    would achieve a perfect score by simply assigning every class to every
    input. In order to avoid this, a metric should penalize incorrect class
    assignments as well (recall). The F-beta score (ranged from 0.0 to 1.0)
    computes this, as a weighted mean of the proportion of correct class
    assignments vs. the proportion of incorrect class assignments.
    With beta = 1, this is equivalent to a F-measure. With beta < 1, assigning
    correct classes becomes more important, and with beta > 1 the metric is
    instead weighted towards penalizing incorrect class assignments.
    '''
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')
    
    if isinstance(y_pred,list):
        return sk_metrics.fbeta_score(y_true, y_pred, beta)
    else:            
        # If there are no true positives, fix the F score at 0 like sklearn.
        if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
            return 0
        p = precision(y_true, y_pred)
        r = recall(y_true, y_pred)
        bb = beta ** 2
        fbeta_score = (1 + bb) * (p * r) / (bb * p + r + K.epsilon())
        return fbeta_score 


def fmeasure(y_true, y_pred):
    '''
    Calculates the f-measure, the harmonic mean of precision and recall.
    '''
    return fbeta_score(y_true, y_pred, beta=1)


# Aliases
binacc = binary_accuracy
f1score = fscore = f1_score = fmeasure 
precision_score = precision
recall_score = recall
mse = MSE = mean_squared_error
bce = binary_crossentropy
cosine = cosine_proximity

