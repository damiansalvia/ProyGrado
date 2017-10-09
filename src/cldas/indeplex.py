# -*- encoding: utf-8 -*-
'''
Module for generating an minimal context independent lexicon from multiple corporea
@author: Nicolás Mechulam, Damián Salvia
'''

import numpy as np
from utils import progress, save
from _collections import defaultdict
    
    
def _TF(Xcdt, Xt):
    return Xcdt / sum(Xt)


def _IDF(Xt, X, eps=1e-10):
    return np.log2( X / (Xt + eps ) )


def _PMI(Xctd, Xt, X, Tctd, Tt, T, eps=1e-10):
    den = _TF( Xctd , Xt ) * sum( _TF( Tctd , Tt ) ) * T 
    div = 2 * _TF( Xctd , Xt ) * X
    return np.log2( den / ( div + eps ) )  


def _QTF(Xctd, Xt, Tt, Tctd):
    return _TF( Xctd , Xt ) / _TF( Tctd , Tt )


def _TFIDF(Xctd, Xt, X, eps=1e-10):
    return _TF(Xctd, Xt) * _IDF(Xt, X, eps)


def _LDT(ds_pos, ds_neg, eps=1e-10):
    ldt = np.log2( ds_pos / (ds_neg + eps) )
    where_are_NaNs = np.isnan( ldt ) 
    ldt[where_are_NaNs] = 0.0
    return ldt  


def _get_structures(pos_op, neg_op, lemmas, verbose=True):
    index = { lemma:idx for idx,lemma in enumerate(lemmas) }
    size  = len( lemmas )
    
    P = len(pos_op) * 1.0 ; N = len(neg_op) * 1.0
    
    Pctd = np.zeros(size) ; Nctd = np.zeros(size)
    Pt   = np.zeros(size) ; Nt   = np.zeros(size)  
    
    opinions = pos_op + neg_op ; del pos_op ; del neg_op 
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



def by_senti_tfidf(pos_op,neg_op,lemmas,limit=None,eps=1e-10,verbose=True):
    
    P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    ds_pos = _TFIDF(Pctd, Pt, P, eps) 
    ds_neg = _TFIDF(Nctd, Nt, N, eps)
    
    ldt = _LDT(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ldt) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon
    
    
    
def by_senti_qtf(pos_op,neg_op,lemmas,limit=None,eps=1e-10,verbose=True):
    
    _, Pctd, Pt, _, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt
    
    ds_pos = _QTF(Pctd, Pt, Tctd, Tt)
    ds_neg = _QTF(Nctd, Nt, Tctd, Tt)
    
    ldt = _LDT(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ldt) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon    



def by_senti_pmi(pos_op,neg_op,lemmas,limit=None,eps=1e-10,verbose=True):
    
    P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, lemmas, verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt ; T = P+N
    
    ds_pos = _PMI(Pctd, Pt, P, Tctd, Tt, T, eps)
    ds_neg = _PMI(Nctd, Nt, N, Tctd, Tt, T, eps)
    
    ldt = _LDT(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(pol,3) for idx,pol in enumerate(ldt) }
    
    if limit:
        lexicon = sorted(lexicon, key=lambda lem : abs(lexicon[lem]), reverse=True)
    
    return lexicon



def by_avg(pos_op,neg_op,lemmas,limit=None,eps=1e-10,verbose=True):
    pass
