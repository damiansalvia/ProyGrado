# -*- encoding: utf-8 -*-
'''
Module for generating an minimal context independent lexicon from positive and negative opinions
@author: Nicolás Mechulam, Damián Salvia
'''

import numpy as np
from cldas.utils import progress, save, save_word_cloud
from collections import defaultdict
    
    
def _postprocess(method, lemmas, ld, limit, tofile):
    lexicon = { lemmas[idx]:round(val,3) for idx,val in enumerate(ld) }
    
    if limit:
        lexicon = dict( sorted(lexicon.items(), key=lambda elem : abs(elem[1]), reverse=True)[:limit] )
    
    lexicon = dict( sorted( lexicon.items(), key=lambda x:x[0] ) )
    
    if tofile:
        name = "_top%i" % limit if limit else "" 
        name = method + name
        save( lexicon , name , tofile )
        save_word_cloud( lexicon, name, tofile )    
    
    return lexicon



def _valid_tag(tag, tagset):
    for prefix in tagset:
        if tag.startswith(prefix): return True
    return False    

    
    
def _TF(Xctd, Xt):
    '''
    Calculates the Term Frequency from frequency vector and presence vector 
    '''
    num = Xctd
    den = sum(Xt)
    return num/den



def _IDF(Xt, X, eps=1e-3):
    '''
    Calculates Inverse Document Frequency from presence vector and document quantity 
    '''
    num = X + eps
    den = Xt + eps
    return np.log2( num/den )



def _TFIDF(Xctd, Xt, X, eps=1e-3):
    '''
    Calculates Term Frequency Inverse Document Frequency from frequency vector, presence vector and document quantity 
    '''
    return _TF(Xctd, Xt) * _IDF(Xt, X, eps)



def _P(Xctd, Xt, X, eps=1e-3):
    num = _TF(Xctd, Xt) + eps
    den = X + eps
    return num/den



def _PC(Pctd, Pt, P, Nctd, Nt, N, eps=1e-3):
    Ptf = _TF(Pctd, Pt)
    Ntf = _TF(Nctd, Nt)
    num = Ptf * Ntf + eps
    den = np.dot(P, N) + eps
    return num/den



def _PMI(Xctd, Xt, X, Tctd, Tt, T, eps=1e-3):
    '''
    Calculates Pointwise Mutual Information from frequency vector, presence vector and document quantity in target and total
    '''
    num = _TF( Xctd , Xt ) * sum( _TF( Tctd , Tt ) ) * T + eps
    den = 2.0 * _TF( Xctd , Xt ) * X + eps
    return np.log2( num/den )   



def _AVG(Xctd, Xt, X, eps=1e-3):
    '''
    Calculates Average from frequency vector, presence vector and document quantity 
    '''
    num = _TF( Xctd , Xt ) + eps
    den = X + eps
    return num/den 



def _LD(ds_num, ds_den, eps=1e-3):
    '''
    Calculates Logaritmic Differential from two vectors of same lenght
    '''
    num = ds_num + eps
    den = ds_den + eps
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
    
    opinions = pos_op + neg_op
    
    if not lemmas: 
        lemmas = list( set([ tok['lemma'] for op in opinions for tok in op['text'] ]) )
        
    index  = { lemma:idx for idx,lemma in enumerate(lemmas) }
    size   = len( lemmas )
    
    Pctd = np.zeros(size,dtype=float) ; Nctd = np.zeros(size,dtype=float)
    Pt   = np.zeros(size,dtype=float) ; Nt   = np.zeros(size,dtype=float) 
    
    total = len( opinions )
    
    for jth,opinion in enumerate(opinions):
        if verbose : progress("Building lexicon by %s (%*i words)" % (strategy , 4, len(opinion['text']) ), total, jth)
        
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
    
    
    
def by_senti_qtf(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of QTF
    @param pos_op     : Set of positive opinions.
    @param neg_op     : Set of negative opinions.
    @param lemmas     : Set of lemmas in positive and negative opinions (an optimization).
    @param filter_tags: Consider only a set of tags. Requires 'tag' tag in opinion structure.
    @param limit      : Limit output.
    @param eps        : Small number consider for division calculus.
    @param verbose    : Verbose output.
    @param tofile     : Directory where lexicon and wordcloud will be saved.
    @param wdcloud    : Generate a word cloud image. Argument tofile required.
    '''
    
    lemmas, _, Pctd, Pt, _, Nctd, Nt = _get_structures(pos_op, neg_op, 'QTF', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    ds_pos = _TF(Pctd, Pt)
    ds_neg = _TF(Nctd, Nt)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = _postprocess("indeplex_by_senti_qtf",lemmas, ld, limit, tofile)
    
    return lexicon   



def by_senti_tfidf(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of TFIDF
    @param pos_op     : Set of positive opinions.
    @param neg_op     : Set of negative opinions.
    @param lemmas     : Set of lemmas in positive and negative opinions (an optimization).
    @param filter_tags: Consider only a set of tags. Requires 'tag' tag in opinion structure.
    @param limit      : Limit output.
    @param eps        : Small number consider for division calculus.
    @param verbose    : Verbose output.
    @param tofile     : Directory where lexicon and wordcloud will be saved.
    @param wdcloud    : Generate a word cloud image. Argument tofile required.
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'TFIDF', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    ds_pos = _TFIDF(Pctd, Pt, P, eps) 
    ds_neg = _TFIDF(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = _postprocess("indeplex_by_senti_tfidf",lemmas, ld, limit, tofile)
    
    return lexicon 



def by_senti_pmi(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of PMI
    @param pos_op     : Set of positive opinions.
    @param neg_op     : Set of negative opinions.
    @param lemmas     : Set of lemmas in positive and negative opinions (an optimization).
    @param filter_tags: Consider only a set of tags. Requires 'tag' tag in opinion structure.
    @param limit      : Limit output.
    @param eps        : Small number consider for division calculus.
    @param verbose    : Verbose output.
    @param tofile     : Directory where lexicon and wordcloud will be saved.
    @param wdcloud    : Generate a word cloud image. Argument tofile required.
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'PMI', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
#     ds_pos = _PMI(Pctd, Pt, P, Tctd, Tt, T, eps)
#     ds_neg = _PMI(Nctd, Nt, N, Tctd, Tt, T, eps)
#     
#     ld = _LD(ds_pos, ds_neg, eps)
    pr_pos = _P( Pctd , Pt, P )
    pr_neg = _P( Nctd , Nt, N )
    
    pr_con = _PC( Pctd , Pt, P, Nctd , Nt, N )
    
    ds_num = pr_pos * pr_neg
    ds_den = pr_con 
    
    ld = _LD(ds_num, ds_den, eps)
    
    lexicon = _postprocess("indeplex_by_senti_pmi",lemmas, ld, limit, tofile)
    
    return lexicon



def by_senti_avg(pos_op, neg_op, lemmas=None, filter_tags=None, limit=None, eps=1e-3, verbose=True, tofile=None):
    '''
    Generates a lexicon from positive and negative opinion sets by Logaritmic Diferential of AVG
    @param pos_op     : Set of positive opinions.
    @param neg_op     : Set of negative opinions.
    @param lemmas     : Set of lemmas in positive and negative opinions (an optimization).
    @param filter_tags: Consider only a set of tags. Requires 'tag' tag in opinion structure.
    @param limit      : Limit output.
    @param eps        : Small number consider for division calculus.
    @param verbose    : Verbose output.
    @param tofile     : Directory where lexicon and wordcloud will be saved.
    @param wdcloud    : Generate a word cloud image. Argument tofile required.
    '''
    
    lemmas, P, Pctd, Pt, N, Nctd, Nt = _get_structures(pos_op, neg_op, 'AVG', filter_tags=filter_tags, lemmas=lemmas, verbose=verbose)
    
    ds_pos = _AVG(Pctd, Pt, P, eps)
    ds_neg = _AVG(Nctd, Nt, N, eps)
    
    ld = _LD(ds_pos, ds_neg, eps)
    
    lexicon = _postprocess("indeplex_by_senti_avg",lemmas, ld, limit, tofile)
    
    return lexicon 
