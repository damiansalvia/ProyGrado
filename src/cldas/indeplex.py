# -*- encoding: utf-8 -*-
'''
Module for generating an minimal context independent lexicon from positive and negative opinions
@author: Nicolás Mechulam, Damián Salvia
'''

import numpy as np
from utils import progress, save
from collections import defaultdict
    

def _valid_tag(tag, tagset):
    for prefix in tagset:
        if tag.startswith(prefix): return True
    return False    
    
    
def _TF(Xcdt, Xt):
    '''
    Calculates the Term Frequency from frequency vector and presence vector 
    '''
    num = Xcdt
    den = sum(Xt)
    return num/den


def _IDF(Xt, X, eps=1e-3):
    '''
    Calculates Inverse Document Frequency from presence vector and document quantity 
    '''
    num = X + eps
    den = Xt + eps
    return np.log2( num/den )


def _PMI(Xctd, Xt, X, Tctd, Tt, T, eps=1e-3):
    '''
    Calculates Pointwise Mutual Information from frequency vector, presence vector and document quantity in target and total
    '''
    num = _TF( Xctd , Xt ) * sum( _TF( Tctd , Tt ) ) * T + eps
    den = 2.0 * _TF( Xctd , Xt ) * X + eps
    return np.log2( num/den )  


def _QTF(Xctd, Xt, Tt, Tctd, eps=1e-3):
    '''
    Calculates Quotient Term Frequency from frequency vector and presence vector in target and total 
    '''
    num = _TF( Xctd , Xt ) + eps
    den = _TF( Tctd , Tt ) + eps
    return num/den


def _TFIDF(Xctd, Xt, X, eps=1e-3):
    '''
    Calculates Term Frequency Inverse Document Frequency from frequency vector, presence vector and document quantity 
    '''
    return _TF(Xctd, Xt) * _IDF(Xt, X, eps)


def _AVG(Xctd, Xt, X, eps=1e-3):
    '''
    Calculates Average from frequency vector, presence vector and document quantity 
    '''
    num = _TF( Xctd , Xt ) + eps
    den = X + eps
    return num/den 


def _LD(ds_pos, ds_neg, eps=1e-3):
    '''
    Calculates Logaritmic Differential from positive and negative valences
    '''
    num = ds_pos + eps
    den = ds_neg + eps
    ld = np.log2( num/den )  
    ld[ np.isnan( ld ) ] = 0.0
    ld[ np.isinf( ld ) ] = np.nanmin( ld[ld != -np.inf] )
    return ld  


def _get_structures(pos_op, neg_op, strategy, filter_tags=None, lemmas=None, verbose=True):
    '''
    Generates frequency vector, presence vector and document quantity from positive and negative opinion sets
    '''
    
    pos_op = list(pos_op) ; neg_op = list(neg_op) 
    
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
        if verbose : progress("Building lexicon by %s (%i words)" % (strategy , len(opinion['text']) ), total, jth)
        
        cat = opinion['category']
        
        Pfreq = defaultdict(lambda:0)
        Nfreq = defaultdict(lambda:0)
        has_negation = False
        
        for item in opinion['text']:
            
            if not _valid_tag(item['tag'], filter_tags):
                continue
            
            neg = item.get('negated',False)
            if not neg: neg = False
            has_negation |= neg
            
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
        
        if has_negation: 
            if   cat > 50: N += 1
            elif cat < 50: P += 1
            
    return lemmas, P, Pctd, Pt, N, Nctd, Nt



def by_senti_tfidf(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of TFIDF
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'TFIDF', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    ds_pos = _TFIDF(Pctd, Pt, P, eps) 
    ds_neg = _TFIDF(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(val,3) for idx,val in enumerate(ld) }
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda elem : abs(elem[1]), reverse=True)[:limit] )
        
    if tofile:
        suffix = "_top%i" % limit if limit else ""  
        save( lexicon , "indeplex_by_senti_tfidf" + suffix , tofile )
    
    return lexicon
    
    
    
def by_senti_qtf(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of QTF
    '''
    
    lemmas, _, Pctd, Pt, _, Nctd, Nt = _get_structures(pos_op, neg_op, 'QTF', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt
    
    ds_pos = _QTF(Pctd, Pt, Tctd, Tt)
    ds_neg = _QTF(Nctd, Nt, Tctd, Tt)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(val,3) for idx,val in enumerate(ld) }
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda elem : abs(elem[1]), reverse=True)[:limit] )
    
    if tofile:
        suffix = "_top%i" % limit if limit else ""  
        save( lexicon , "indeplex_by_senti_qtf" + suffix , tofile )
    
    return lexicon    



def by_senti_pmi(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of PMI
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'PMI', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    Tctd = Pctd+Nctd ; Tt = Pt+Nt ; T = P+N
    
    ds_pos = _PMI(Pctd, Pt, P, Tctd, Tt, T, eps)
    ds_neg = _PMI(Nctd, Nt, N, Tctd, Tt, T, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(val,3) for idx,val in enumerate(ld) }
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda elem : abs(elem[1]), reverse=True)[:limit] )
    
    if tofile:
        suffix = "_top%i" % limit if limit else "" 
        save( lexicon , "indeplex_by_senti_pmi" + suffix , tofile )
    
    return lexicon



def by_senti_avg(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of AVG
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'AVG', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    ds_pos = _AVG(Pctd, Pt, P, eps)
    ds_neg = _AVG(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = { lemmas[idx]:round(val,3) for idx,val in enumerate(ld) }
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda elem : abs(elem[1]), reverse=True)[:limit] )
    
    if tofile:
        suffix = "_top%i" % limit if limit else "" 
        save( lexicon , "indeplex_by_senti_avg" + suffix , tofile )
    
    return lexicon 
