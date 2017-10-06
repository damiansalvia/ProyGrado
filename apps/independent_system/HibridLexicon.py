# -*- coding: utf-8 -*-
import sys
from _collections import defaultdict
sys.path.append('../utilities')
from utilities import *

from DataProvider import db
import codecs
import numpy as np

output_dir = 'outputs/tmp/'


reviews = db.reviews.find({},no_cursor_timeout=True).limit(10)
lemmas  = db.reviews.distinct("text.lemma")
index = { lemma:idx for idx,lemma in enumerate(lemmas) }
alias = { item['_id']:item['nearestOf'] 
    for item in db.embeddings.find({"nearestOf":{"$ne":None}},{"nearestOf":1}) 
    if item['nearestOf'] in lemmas }

P = db.reviews.find({"category":{ "$gt":50 }}).count() * 1.0
N = db.reviews.find({"category":{ "$lt":50 }}).count() * 1.0

size = len(lemmas)

Pctd = np.zeros(size)
Pt   = np.zeros(size) 
Nctd = np.zeros(size)
Nt   = np.zeros(size) 
 
total = reviews.count()
for jth,review in enumerate(reviews):
    
    cat = review['category']
    
    Pfreq = defaultdict(lambda:0)
    Nfreq = defaultdict(lambda:0)
    has_negation = False
    for item in review['text']:
        neg = item.has_key('negated') and item['negated']
        has_negation |= neg

        lem = item['lemma']
        if alias.has_key(lem): # Correct some lemmas
            lem = alias[ lem ]
         
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
        if cat > 50:
            N += 1
        elif cat < 50:
            P += 1

reviews.close()

# TF      = (Nctd + Pctd) / (sum(Nt) + sum(Pt))
# TF_neg  = Nctd / sum(Nt)
# TF_pos  = Pctd / sum(Pt)

# IDF_pos = np.log2( P / (Pt + 1e-10 ) )
# IDF_neg = np.log2( N / (Nt + 1e-10 ) )

# PMI_pos = np.log2( (TF_pos * sum(TF) * (P+N) ) / ( 2 * TF_pos * P) )
# PMI_neg = np.log2( (TF_neg * sum(TF) * (P+N) ) / ( 2 * TF_neg * N) )

def TF(frecuency, pertenence):
    return frecuency / sum(pertenence)

def IDF(pertenence, documents):
    return np.log2( documents / (pertenence + 1e-10 ) )

def PMI(target_f, comp_f, target_p, comp_p, target_D, comp_D):
    return np.log2( 
        (
            TF(target_f, target_p) * 
            sum(TF(target_f + comp_f, target_p + comp_p)) * 
            (target_D + comp_D) 
        ) /  ( 
            2 * 
            TF(target_f, target_p) * 
            target_D
        ) 
    )
  

def ldt(ds_pos, ds_neg):
    LDT = np.log2( ds_pos / (ds_neg + 1e-10) )
    where_are_NaNs = np.isnan( LDT ) 
    LDT[where_are_NaNs] = 0.0
    return LDT  

# weighting 1
def ds_TF(Nctd, Pctd, Nt, Pt):
    ds_TF_pos = TF(Pctd, Pt) / TF(Nctd + Pctd, Nt + Pt )
    ds_TF_neg = TF(Nctd, Nt) / TF(Nctd + Pctd, Nt + Pt )
    return ds_TF_pos, ds_TF_neg

# weighting 2
def ds_TFIDF(Nctd, Pctd, Nt, Pt, N, P):
    ds_TFIDF_pos = TF(Pctd, Pt) * IDF(Pt, P)
    ds_TFIDF_neg = TF(Nctd, Nt) * IDF(Nt, N)
    return ds_TFIDF_pos, ds_TFIDF_neg

# weighting 3
def ds_PMI(Nctd, Pctd, Nt, Pt, N, P):
    ds_PMI_pos = PMI(Pctd, Nctd, Pt, Nt, P, N)
    ds_PMI_neg = PMI(Nctd, Pctd, Nt, Pt, N, P)
    return ds_PMI_pos, ds_PMI_neg  


with codecs.open('outputs/hibird_TF.json' , "w", "utf-8") as f:
    ds_1, ds_2 = ds_TF(Nctd, Pctd, Nt, Pt)
    LDT = ldt( ds_1, ds_2 )
    json.dump({lemma:LDT[index[lemma]] for lemma in index}, f, indent=4, ensure_ascii=False)

# with codecs.open('outputs/hibird_TFIDF.json' , "w", "utf-8") as f:
#     LDT = ldt( ds_TFIDF(Nctd, Pctd, Nt, Pt, N, P) )
#     json.dump({lemma:LDT[index[lemma]] for lemma in index}, f, indent=4, ensure_ascii=False)

# with codecs.open('outputs/hibird_PMI.json' , "w", "utf-8") as f:
#     LDT = ldt( ds_PMI(Nctd, Pctd, Nt, Pt, N, P) )
#     json.dump({lemma:LDT[index[lemma]] for lemma in index}, f, indent=4, ensure_ascii=False)

