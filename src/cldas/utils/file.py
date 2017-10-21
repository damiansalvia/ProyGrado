# -*- coding: utf-8 -*-
'''
Module for managing temporal resources

@author: Nicolás Mechulam, Damián Salvia
'''

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from time import gmtime, strftime
import os, io, json



def save(data,name,path,overwrite=True):
    
    if not data:
        print "Nothing to be saved" 
        return    
    
    path = path.replace("\\", "/")
    path = path if path[-1] != "/" else path[:-1]
    
    if not os.path.isdir(path): os.makedirs(path)
        
    suffix = "" if overwrite else strftime("%Y%m%d_%H-%M-%S", gmtime()) 
            
    path = "%s/%s%s.json" % (path,name,suffix)         
    
    with io.open(path,"w",encoding='utf8') as fp:
        content = json.dumps(data,indent=4,ensure_ascii=False)
        if not isinstance(content, unicode):
            content = unicode(content,'utf8')
        fp.write(content)
    print "Saved at",path
    
    
    
def load(abspath):
    
    abspath = abspath.replace("\\", "/")
    
    if not abspath or not os.path.exists(abspath) or abspath.split('.')[-1] <> 'json':
        print "Nothing to be load from",abspath
        return 
    
    with io.open(abspath,"r",encoding='utf8') as fp:
        content = json.load(fp,'utf8')
        
    return content

 

def _pos_color(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = 120
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)  

def _neu_color(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = 220
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)  

def _neg_color(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
    h = 20
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)  
    
def save_word_cloud(lexicon,name,path,neu_treshold=0):
    
    if not lexicon:
        print "Nothing to be saved" 
        return  
    
    lexicon = {word:item['val'] for word,item in lexicon.items()}
    
    print "Saving...",
    
    path = path.replace("\\", "/")
    path = path if path[-1] != "/" else path[:-1]
    path = "%s/%s.png" % (path,name)  
    
    tot = len(lexicon) * 1.0
    pos = dict([ (lem,val) for lem,val in lexicon.items() if val >  neu_treshold ])
    neu = dict([ (lem,val) for lem,val in lexicon.items() if -neu_treshold <= val <= neu_treshold ])
    neg = dict([ (lem,val) for lem,val in lexicon.items() if val <  -neu_treshold ])
    
    width = 600
    
    avgs = [len(neg)/tot,len(neu)/tot,len(pos)/tot]
    avgs = [x for x in avgs if x]   
    qty  = len(avgs)
    
    fig, ax = plt.subplots( qty, sharex=True, gridspec_kw={'height_ratios':[int(round(10*x))+1 for x in avgs]} )
    
    if pos:
        qty -= 1
        height = int(round(width*avgs[qty]))
        wc = WordCloud(background_color="white", width=width, height=height, max_words=400, max_font_size=40, random_state=42, color_func=_pos_color)
        wc = wc.generate_from_frequencies(pos)
        ax[qty].imshow(wc, interpolation="bilinear", aspect='auto')
        ax[qty].axis('off')
        
    if neu:
        qty -= 1
        height = int(round(width*avgs[qty]))
        wc = WordCloud(background_color="white", width=width, height=height, max_words=400, max_font_size=40, random_state=42,color_func=_neu_color)
        wc = wc.generate_from_frequencies(neu)
        ax[qty].imshow(wc, interpolation="bilinear", aspect='auto')
        ax[qty].axis('off')
        
    if neg:
        qty -= 1
        height = int(round(width*avgs[qty]))
        wc = WordCloud(background_color="white", width=width, height=height, max_words=400, max_font_size=40, random_state=42,color_func=_neg_color)
        wc = wc.generate_from_frequencies(neg)
        ax[qty].imshow(wc, interpolation="bilinear", aspect='auto')
        ax[qty].axis('off')
    
    fig.subplots_adjust(wspace=0, hspace=0)    
    fig.savefig(path, facecolor='k', bbox_inches='tight', dpi=1200, figsize=(20,20), transparent=True, frameon=False, pad_inches=0)
    print "\rWord cloud saved at",path        
    