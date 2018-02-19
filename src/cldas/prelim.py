# -*- coding: utf-8 -*-
'''
Module for preliminar preprocess of corporea text

@author: Nicolás Mechulam, Damián Salvia
'''

import freeling, os, enchant, re, md5
from ftfy import fix_text
from enchant.checker import SpellChecker
from difflib import get_close_matches
from collections import defaultdict, Counter

from cldas.utils import progress, save
from cldas.utils.misc import Iterable, Levinstein
from cldas.utils.misc import no_accent, levenshtein_no_accent, get_close_dist
from cldas.utils.logger import Log, Level

log = Log("./log")


DATA = "/usr/local/share/freeling/"
LANG = "es"
PWL  = os.path.join( os.path.dirname(__file__) , "files/aspell-es-lat.dic" )



class _SingletonSettings(object):
    '''
    Singleton base class with required settings
    '''
    
    _instance = None
    
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_SingletonSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self,data, lang, pwl, vocabulary):
                
        if not os.path.exists(pwl): 
            raise ValueError("%s cannot be found" % pwl)
        
        custom_dict = enchant.DictWithPWL( lang , pwl )
        
        freeling.util_init_locale( "default" )
        
        op = freeling.maco_options( lang )
        op.PunctuationFile  = data+"common/punct.dat"
        op.DictionaryFile   = data+lang+"/es-ar/dicc.src"
        op.AffixFile        = data+lang+"/afixos.dat"
        op.LocutionsFile    = data+lang+"/locucions.dat"
        op.NPdataFile       = data+lang+"/np.dat"
        op.QuantitiesFile   = data+lang+"/quantities.dat" 
        op.ProbabilityFile  = data+lang+"/probabilitats.dat" 
        
        self.Checker      = SpellChecker( custom_dict )
        self.Vocabulary   = Levinstein( vocabulary )
        self.Tokenizer    = freeling.tokenizer( data+lang+"/tokenizer.dat" )
        self.Splitter     = freeling.splitter( data+lang+"/splitter.dat" )
        self.Morfo        = freeling.maco( op )
        self.Tagger       = freeling.hmm_tagger( data+lang+"/tagger.dat" , True , 2 )
        self.Ortographic  = freeling.alternatives( data+lang+"/alternatives-ort.dat" )
        
        self.SessionId = self.Splitter.open_session()
        
        
    def __del__(self):
        self.Splitter.close_session(self.SessionId)
    

SUBSTITUTIONS = [
    # Eliminate contractions
    (u"(\w)'(\w)",u"\\1\\2"), (u"q'",u"q"),
    # Replace quotes variants by double quotes
    (u"[`´'\u201c\u201d]",u"\""),
    (u'\u2026',u'...'),   
    # Replace multiple periods by one
    (u"(\.\s*)+",u"."),
    # Repplace http or https URIs by tag
    (u"([^\s]?https?:\/\/\S+)",u"ENLACE"),
    # Replace email by tag 
    (u"[\w\.-]+@[\w\.-]+\.[\w]+",u"CORREO"),
    # Replace emojis by a special of emotion
    (u"\s<?[:;=8xX][-‑o\']?[\)\]3dDoOpP\*\}]|[\(\[cC\{][-‑o\*\']?[:;=8]>?\s",u" FELIZ "),
    (u"\s>?[:;=][-‑o\']?[\(\[cC\{\\\/\|@_]|[\)\]dD\}\\\/\|@_][-‑o\']?[:;=8xX]<?\s",u" TRISTE "),
    # Remove repetitive characters and expressions (except (ll)egar, pe(rr)o and a(cc)ion, and numbers) <-- will be corrected by aspell
    (u"([^lrc\d])\\1+",u"\\1"),
    (u"([lrc])\\1\\1+",u"\\1\\1"),
    (u'(\w\w)\\1+',u'\\1\\1'),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"([\d\W])",u" \\1 "),
    (u"([^0-9a-záéíóúñü_\s])",u" \\1 "),
    # Separate alphabetical from numerical 
    (u"(\d+)",u"  \\1 "),
    # Remove redundant quote marks  -- replace, delete, undo
    (u"(\")([^\"]*?)(?(1)\")",u"&quote;\\2&quote;"),
    (u"[\"]",u""),
    (u"&quote;\s+&quote;",u""),
    (u"&quote;",u"\""),
    # Remove redundant parenthesis -- replace, delete, undo
    (u"(\()([^\(]*?)(?(1)\))",u"&lquo;\\2&rquo;"),
    (u"[\(\)]",u""),
    (u"&lquo;",u"("),(u"&rquo;",u")"), 
    # Replace all non-alphabetical or special symbols by a whitespace
    (u"[^0-9a-záéíóúñü_¿\?¡!\(\),\.:;\"\$/<>]",u" "),
    # Replace multiple non-alphabetical characters by one
    (u'([^\w\d])\\1+',u'\\1 '), # Issue when nested quotes
    # Replace multiple blank spaces by one
    (u"\s\s+",u" "),
    # Rejoin number sequences separated by blankspace or single dot (e.g. 2.500.000)
    (u"(\d+)\s+(?=\d)",u"\\1"),
    (u"(\d+)\s+(\.)\s+(?=\d)",u"\\1\\2"),
    # Force dot ending
    (u"([^\w\?!\)\"])$",u""), 
    (u"([^\.])$",u"\\1 ."),
]
    
class _SpellCorrector(_SingletonSettings):
    '''
    Class for making text correction
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(_SpellCorrector, cls).__new__(cls, *args, **kwargs)
    
    
    def _clean_unbalanced(self,text):
        diff = text.count(u"(") - text.count(u")")
        while diff != 0:
            if diff > 0 : i = text.index(u"(") ; diff -= 1
            if diff < 0 : i = text.index(u")") ; diff += 1
            text = text[:i]+text[i+1:]
        diff = text.count(u"¿") - text.count(u"?")
        while diff != 0:
            if diff > 0 : i = text.index(u"¿") ; diff -= 1
            if diff < 0 : i = text.index(u"?") ; diff += 1
            text = text[:i]+u"."+text[i+1:]
        diff = text.count(u"¡") - text.count(u"!")
        while diff != 0:
            if diff > 0 : i = text.index(u"¡") ; diff -= 1
            if diff < 0 : i = text.index(u"!") ; diff += 1
            text = text[:i]+u"."+text[i+1:]
        if text.count(u"\"") % 2 == 1 :
            i = text.index(u"\"")
            text = text[:i]+u"."+text[i+1:]
        return text
    
    
    def _clean_tags(self,text):
        return re.sub(u"<.*?>",u"",text,flags=re.DOTALL|re.U)
    
    
    def _correct(self,text):
        if not isinstance(text,unicode):
            text = unicode(text,'utf8')
        
        text = fix_text(text)
            
        for source,target in SUBSTITUTIONS:
            text = re.sub(source,target,text,flags=re.DOTALL|re.U|re.I)
            text = text.strip()
            
        text = self._clean_tags(text)
        text = self._clean_unbalanced(text)
        
        self.Morfo.set_active_options(
            False, # User Map
            False, # Number Detection 
            True,  # Punctuation Detection 
            False, # Date Detection 
            True,  # Dictionary Search 
            True,  # Affix Analysis
            False, # Compound Analysis
            False, # Retok Contractions
            False, # Multiword Detection 
            False, # NER                    <-- REQUIRED
            False, # Quantities Detection
            False  # Probability Assignment <-- REQUIRED
        )
        
        ls = self.Tokenizer.tokenize( text )
        ls = self.Splitter.split( self.SessionId , ls , False )
        ls = self.Morfo.analyze( ls )
        ls = self.Ortographic.analyze( ls )
         
        ack = []  
        for sentence in ls :
            for token in sentence.get_words() :
                word = token.get_form()
                if token.found_in_dict():
                    ack += [ wd for wd in word.split('_') ]
        
        self.Morfo.set_active_options(
            False,  # User Map
            False,  # Number Detection 
            True,   # Punctuation Detection 
            False,  # Date Detection 
            True,   # Dictionary Search 
            True,   # Affix Analysis
            False,  # Compound Analysis
            False,  # Retok Contractions
            False,  # Multiword Detection 
            True,   # NER 
            False,  # Quantities Detection
            False   # Probability Assignment <-- REQUIRED
        )
        
        ls = self.Tokenizer.tokenize( text )
        ls = self.Splitter.split( self.SessionId , ls , False )
        ls = self.Morfo.analyze( ls )
        ls = self.Ortographic.analyze( ls )
        
        nouns = [] 
        for sentence in ls :
            for token in sentence.get_words() :
                word = token.get_form()
                if token.found_in_dict():
                    nouns += [ wd for wd in word.split('_') if wd not in ack ]
        nouns = { wd.lower():wd for wd in nouns }
        
        text = unicode( text.lower() )
        self.Checker.set_text( text )
        for err in self.Checker:
            word = err.word
            
            cand = self.Vocabulary.correction( word )
            
            sugg = self.Checker.suggest( word )
            sugg = get_close_dist( word, sugg, 0.9 )
            
            alts = get_close_matches( word, sugg, 5, 0.90 )
            alts = [ wd for wd in get_close_matches( word, sugg, 5, 0.90 ) if levenshtein_no_accent(word,wd) < 2 ]
            
            if alts and len(alts) <= 2:
                corr = alts[0]
            elif sugg and (word not in nouns):
                corr = sugg[0]
            elif (word in ack) and (word not in nouns):
                corr = word
            elif word in nouns:
                corr = nouns[word]
            else:
                corr = cand
            err.replace( corr )
            
        text = self.Checker.get_text()   
        return text, nouns.keys()



class _MorfoTokenizer(_SingletonSettings):
    '''
    Class for making text tokenizaion, lemmatization and POS-tagging
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(_MorfoTokenizer, cls).__new__(cls, *args, **kwargs)
    
    
    def _analyze(self,text,nouns):
        
        self.Morfo.set_active_options(
            False,  # User Map
            False,  # Number Detection 
            True,   # Punctuation Detection 
            False,  # Date Detection 
            True,   # Dictionary Search 
            True,   # Affix Analysis
            False,  # Compound Analysis
            False,  # Retok Contractions
            False,  # Multiword Detection 
            True,   # NER 
            False,  # Quantities Detection
            True    # Probability Assignment <-- Required
        )
        
        text = ' '.join( word if (word.lower() not in nouns) else word for word in text.split(' ') )
        
        ls = self.Tokenizer.tokenize( text )
        ls = self.Splitter.split( self.SessionId, ls, False )
        ls = self.Morfo.analyze( ls )
        ls = self.Tagger.analyze( ls )        
        
        sent = []
        for sentence in ls :
            for token in sentence.get_words() :
                sent.append({
                    "form"  : token.get_lc_form(),
                    "lemma" : token.get_lemma(), 
                    "tag"   : token.get_tag()
                })
                
        return sent


class Preprocess(_SpellCorrector,_MorfoTokenizer):
    '''
    Itemize text from corporea applying correction, tokenizaion, lemmatization and POS-tagging
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(Preprocess, cls).__new__(cls, *args, **kwargs)
    
    
    def __init__(self, source, opinions, data=DATA, lang=LANG, pwl=PWL, verbose=True, *args, **kwargs):
        vocabulary = Counter( word for opinion in opinions for word in re.findall(r'\w+',opinion['text'].lower()) )
        super(Preprocess, self).__init__(data, lang, pwl, vocabulary, *args, **kwargs)
        self.source = source
        self._lang   = lang
        self._sents  = defaultdict(list)
         
        self._run(opinions,verbose)
        
        
    def _run(self, opinions, verbose):
        if not opinions:
            return
        
        _ids = []
        total = len( opinions ) ; fails = 0 
        for idx, opinion in enumerate(opinions):
            
            if verbose: progress("Preprocessing %s (Fails %05.2f%%)" %  ( self.source, 100.0*fails/total ), total, idx )  
                         
            _id = md5.new( "%s %s" % (str(opinion['category']),opinion['text'].encode('ascii', 'ignore')) ).hexdigest()
            
            if _id in _ids:
                log("Repeated opinion '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self.source ) , level=Level.ERROR)
                continue
            
            text = opinion['text']
            text,nouns = self._correct(text)
            sent = self._analyze(text,nouns)
            
            if not sent:
                fails += 1
                log("Empty analysis for '%s' (at %s)" % ( text.encode('ascii','ignore') , self.source ) , level=Level.ERROR)
                continue
                
            _ids.append(_id)
            
            tags = opinion.pop('tags',None)
            if tags is None:
                items = [{
                    'word'   : token['form'],
                    'lemma'  : token['lemma'],
                    'tag'    : token['tag'],
                } for token in sent ]
            else:
                sent,tags = __fix_tags__( opinion['text'].split(' '), sent, tags ) # TO-DO Please improve me  
                items = [{
                    'word'   : token['form'],
                    'lemma'  : token['lemma'],
                    'tag'    : token['tag'],
                    'negated': False if tag == 'O' else None if tag == 'B-NEG' else True,
                } for token,tag in zip(sent,tags) ]              
            
            self._sents[ opinion['category'] ].append({
                '_id' : _id,
                'text': items
            })
    
       
    def __repr__(self):
        return "< %s.%s - %s (%s) >" % (self.__class__.__module__, self.__class__.__name__, self.source, self._lang)
        
        
    def __str__(self):
        return "%s(%s,%s)" % ( self.__class__.__name__, self.source , self._lang.upper() )        
        
    
    def categories(self,pattern=None):
        if not pattern:
            return self._sents.keys()
        return [ category for category in self._sents.keys() if re.match(pattern,category) ]
    
        
    def sents(self,category=None):
        if category is None:
            return sum( self._sents.values() , [] )
        elif category not in self.categories():
            raise ValueError('Expected key argument \'category\' to be in categories.')
        else:
            return self._sents[category]
            
    
    def data(self,mapping=None,**kwargs):
        def _gen(mapping):
            pattern = r"(%s)" % '|'.join(mapping.keys()) if mapping else None
            for category in self.categories( pattern=pattern ):
                for sent in self.sents(category=category):
                    item = { 
                        "_id":sent['_id'], 
                        'source':self.source,
                        'text':sent['text'], 
                        'category':category if mapping is None else mapping.get(category,None) 
                    } 
                    if kwargs:
                        item.update(kwargs)
                    yield item
        return Iterable( _gen(mapping) )
            
    
    def to_json(self,dirpath='./'):
        save( self._sents , "preproc_%s.json" % self.source , dirpath )
   
        
        
'''
-----------------------
      AUXILIARIES
-----------------------
'''        

def __equals__(item1,item2):
    item1 = re.sub(u"(\w)\\1+",u"\\1",item1)
    item2 = re.sub(u"(\w)\\1+",u"\\1",item2)
    item1 = no_accent(item1)
    item2 = no_accent(item2)
    return item1==item2 \
        or item1 in item2 \
        or item2 in item1 \
        or levenshtein_no_accent(item1,item2) < 3 \
        or (re.search("([^\s]?https?:\/\/\S+)", item1) is not None and item2 == 'enlace') \
        or (re.search("[\w\.-]+@[\w\.-]+\.[\w]+", item1) is not None and item2 == 'correo') \
                

def __fix_tags__(original,generated,tags):  
    genwords = [ tok['form'] for tok in generated ]
    i = j = 0 ; newsent = [] ; newtags = []
    try:
        while i < len(original) and j < len(generated):
            if __equals__( original[i].lower(), genwords[j].lower() ) or i+1 == len(original):
                newsent.append( generated[j] ) ; newtags.append( tags[i] )
                i+=1 ; j+=1
            else:
                if __equals__( original[i+1].lower(), generated[j]['form'].lower() ):    
                    i += 1
                elif i > 0 and tags[i] == 'B-NEG': # Do not repeat negator -- assign previous tag
                    newsent.append( generated[j] ) ; newtags.append( tags[i-1] )
                    j += 1
                else: # __equals__( original[i].lower(), genwords[j].lower() ):
                    newsent.append( generated[j] ) ; newtags.append( tags[i] )
                    j += 1
    except Exception as e:
        raw_input("\nSHIT")
        import pdb; pdb.set_trace()
        
    return newsent,newtags        
    