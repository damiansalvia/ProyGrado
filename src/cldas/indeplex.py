# -*- encoding: utf-8 -*-
'''
Module for generating an minimal context independent lexicon from positive and negative opinions
@author: Nicolás Mechulam, Damián Salvia
'''

import numpy as np
from utils import progress, save
from _collections import defaultdict
    
    
def _TF(Xcdt, Xt):
    '''
    Calculates the Term Frequency from frequency vector and presence vector 
    '''
    return 1.0 * Xcdt / sum(Xt)


def _IDF(Xt, X, eps=1e-5):
    '''
    Calculates Inverse Document Frequency from presence vector and document quantity 
    '''
    return np.log2( 1.0 * X / (Xt + eps ) )


def _PMI(Xctd, Xt, X, Tctd, Tt, T, eps=1e-5):
    '''
    Calculates Pointwise Mutual Information from frequency vector, presence vector and document quantity in target and total
    '''
    den = _TF( Xctd , Xt ) * sum( _TF( Tctd , Tt ) ) * T 
    div = 2.0 * _TF( Xctd , Xt ) * X
    return np.log2( den / ( div + eps ) )  


def _QTF(Xctd, Xt, Tt, Tctd):
    '''
    Calculates Quotient Term Frequency from frequency vector and presence vector in target and total 
    '''
    return _TF( Xctd , Xt ) / _TF( Tctd , Tt )


def _TFIDF(Xctd, Xt, X, eps=1e-5):
    '''
    Calculates Term Frequency Inverse Document Frequency from frequency vector, presence vector and document quantity 
    '''
    return _TF(Xctd, Xt) * _IDF(Xt, X, eps)


def _AVG(Xctd, Xt, X, eps=1e-5):
    '''
    Calculates Average from frequency vector, presence vector and document quantity 
    '''
    return _TF( Xctd , Xt ) / ( X + eps )


def _LD(ds_pos, ds_neg, eps=1e-5):
    '''
    Calculates Logaritmic Differential from positive and negative valences
    '''
    ld = np.log2( ds_pos / (ds_neg + eps) )
    where_are_NaNs = np.isnan( ld ) 
    ld[where_are_NaNs] = 0.0
    return ld  


def _get_structures(pos_op, neg_op, lemmas=None, verbose=True):
    
    P = 1.0 * len(pos_op) ; N = 1.0 * len(neg_op)  
    
    opinions = pos_op + neg_op ; del pos_op ; del neg_op
    
    if not lemmas: 
        lemmas = list( set([ tok['lemma'] for op in opinions for tok in op['text'] ]) )
        
    index  = { lemma:idx for idx,lemma in enumerate(lemmas) }
    size   = len( lemmas )
    
    Pctd = np.zeros(size) ; Nctd = np.zeros(size)
    Pt   = np.zeros(size) ; Nt   = np.zeros(size) 
    
    total = len(opinions)
    
    for jth,opinion in enumerate(opinions):
        if verbose : progress("Building (%i words)" % len(opinion['text']),total,jth)
        
        cat = opinion['category']
        
        Pfreq = defaultdict(lambda:0)
        Nfreq = defaultdict(lambda:0)
        for item in opinion['text']:
            neg = item.has_key('negated') and item['negated']
            
            lem = item['lemma']
             
            ith = index[ lem ]
            
            if (cat > 50 and not neg) or (cat < 50 and neg):
                Pfreq[ith] += 1
                continue
            
            if (cat < 50 and not neg) or (cat > 50 and neg):
                Nfreq[ith] += 1
                continue
        
        for idx in Pfreq:
            Pctd[idx] += Pfreq[idx]
            Pt[idx]   += 1
            
        for idx in Nfreq:
            Nctd[idx] += Nfreq[idx]
            Nt[idx]   += 1
    
    return P, Pctd, Pt, N, Nctd, Nt



def by_senti_tfidf(pos_op,neg_op,lemmas=None,limit=None,eps=1e-5,verbose=True):
    
    P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    ds_pos = _TFIDF(Pctd, Pt, P, eps) 
    ds_neg = _TFIDF(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ld) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon
    
    
    
def by_senti_qtf(pos_op,neg_op,lemmas=None,limit=None,eps=1e-5,verbose=True):
    
    _, Pctd, Pt, _, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt
    
    ds_pos = _QTF(Pctd, Pt, Tctd, Tt)
    ds_neg = _QTF(Nctd, Nt, Tctd, Tt)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ld) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon    



def by_senti_pmi(pos_op,neg_op,lemmas=None,limit=None,eps=1e-5,verbose=True):
    
    P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt ; T = P+N
    
    ds_pos = _PMI(Pctd, Pt, P, Tctd, Tt, T, eps)
    ds_neg = _PMI(Nctd, Nt, N, Tctd, Tt, T, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ld) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon



def by_senti_avg(pos_op,neg_op,lemmas=None,limit=None,eps=1e-5,verbose=True):
    
    P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    ds_pos = _AVG(Pctd, Pt, P, eps)
    ds_neg = _AVG(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ld) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon
    
  
    
    
