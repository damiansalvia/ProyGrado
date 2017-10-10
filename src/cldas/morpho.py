# -*- coding: utf-8 -*-
'''
Module for preprocessing corporea text

@author: Nicolás Mechulam, Damián Salvia
'''

import freeling, os, enchant, re, md5
from enchant.checker import SpellChecker
from difflib import get_close_matches
from utils import progress, Log, save
from pprint import _id
from _collections import defaultdict

log = Log("./log")


DATA = "/usr/local/share/freeling/"
LANG = "es"
PWL  = os.path.join( os.path.dirname(__file__) , "files/aspell-es-lat.dic" )


class _SingletonSettings(object):
    '''
    Singleton class with the required settings
    '''
    
    _instance = None
    
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_SingletonSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self,data,lang,pwl):
        
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
    (u"(\w)'(\w)",u"\\1\\2"),
    (u"q'",u"q"),
    # Replace quotes variants by double quotes
    (u"`",u"\""),(u"´",u"\""),(u"\'",u"\""),
    (u"[\u201c\u201d]",u"\""),
    (u'\u2026',u'...'),   
    # Replace multiple periods by one
    (u"(\.\s*)+",u"."),
    # Replace emojis by a special tag
    (u":\)",u" emoji_feliz "),(u"\(:",u" emoji_feliz "),(u"\sxD\s",u" emoji_feliz "),
    (u":\(",u" emoji_triste "),(u"\):",u" emoji_triste "),
    # Remove URIs with scheme http or https
    (u"(https?:\/\/\S+)",u""),
    # Remove repetitive characters (except (ll)egar, pe(rr)o and a(cc)ion ) <-- will be corrected by aspell
    (u"([^lrc])\\1+",u"\\1"),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"([0-9a-záéíóúñü\\\]?)([^0-9a-záéíóúñü_\\\\s]+)([0-9a-záéíóúñü\\\]?)",u"\\1 \\2 \\3"),
    (u"([^0-9a-záéíóúñü_\s])([^0-9a-záéíóúñü_\s])",u"\\1 \\2"),
    # Separate alphabetical from numerical 
    (u"([a-záéíóúñü])([0-9])",u"\\1 \\2"), 
    (u"([0-9])([a-záéíóúñü])",u"\\1 \\2"),
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
#     (u'([¿\?¡!\(\),\.:;\"\$\/<>])(\\1\s*)+',u'\\1 '), # Issue when nested quotes
    # Force dot ending
    (u"([^\w\?!\)\"])$",u""), (u"([^\.])$",u"\\1 ."),
    # Replace multiple blank spaces by one
    (u"\s\s+",u" ")
]
    
class _SpellCorrector(_SingletonSettings):
    '''
    Makes text correction
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(_SpellCorrector, cls).__new__(cls, *args, **kwargs)
    
    
    def _no_accent(self,text):
        return text.replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'ü',u'u')
    
    
    def _clean_unbalanced(self,text):
        diff = text.count(u"(") - text.count(u")")
        while diff <> 0:
            if diff > 0 :
                i = text.index(u"(") ; diff -= 1
            if diff < 0 : 
                i = text.index(u")") ; diff += 1
            text = text[:i]+text[i+1:]
        if text.count(u"¿") - text.count(u"?") <> 0: 
            text = re.sub(u"[\?¿]",u".",text)
        if text.count(u"¡") - text.count(u"!") <> 0: 
            text = re.sub(u"[!¡]",u".",text)
        if text.count(u"\"") % 2 == 1 :
            i = text.index(u"\"")
            text = text[:i] + text[i+1:]
        return text
    
    
    def _clean_tags(self,text):
        pattern = u"<\s(.*?)\s.*?>(.*?)</\s\\1\s>" 
        while re.search(pattern, text, flags=re.DOTALL):
            text = re.sub(pattern,u"\\2",text,flags=re.DOTALL)
        text = re.sub(u"<.*?>",u"",text,flags=re.DOTALL)
    
    def _correct(self,text):
        
        if not isinstance(text,unicode):
            text = unicode(text,'utf8')
            
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
            True,  # Retok Contractions
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
                for word in word.split('_'):
                    if token.found_in_dict(): 
                        ack.append( word )
        
        self.Morfo.set_active_options(
            False,  # User Map
            False,  # Number Detection 
            True,   # Punctuation Detection 
            False,  # Date Detection 
            True,   # Dictionary Search 
            True,   # Affix Analysis
            False,  # Compound Analysis
            True,   # Retok Contractions
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
                for word in word.split('_'):
                    if token.found_in_dict() and (word not in ack): 
                        nouns.append( word )
                           
        words = text.split(' ')
        for i in range( len( words ) ):
            word = words[i]
            if not word: 
                continue
            if (word in ack) or self.Checker.check( word ):
                word = word.lower()
            else:
                word_na = self._no_accent( word )
                sugg = { self._no_accent(s):s for s in self.Checker.suggest( word_na ) if ('-' not in s) }
                alts = get_close_matches( word_na , sugg.keys() , 5 , 0.75   )
                if   alts : corr = sugg[ alts[0] ].lower()
                elif sugg : corr = sugg.keys()[0].lower() if (word not in nouns) else word
                else : 
                    self.Checker.set_text( word )
                    for err in self.Checker:
                        corr = self.Checker.suggest( err.word ) 
                        err.replace( corr[0] if corr else err.word )
                    word = self.Checker.get_text()
                    corr = word.lower() if (word not in nouns) else word
                import pdb;pdb.set_trace()
                word = corr
            words[i] = word
        text = ' '.join(words)
            
        return text



class _MorfoTokenizer(_SingletonSettings):
    '''
    Makes text tokenizaion, lemmatization and POS-tagging
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(_MorfoTokenizer, cls).__new__(cls, *args, **kwargs)
    
    
    def _analyze(self,text):
        
        self.Morfo.set_active_options(
            False,  # User Map
            False,  # Number Detection 
            True,   # Punctuation Detection 
            False,  # Date Detection 
            True,   # Dictionary Search 
            True,   # Affix Analysis
            False,  # Compound Analysis
            True,   # Retok Contractions
            False,  # Multiword Detection 
            True,   # NER 
            False,  # Quantities Detection
            True    # Probability Assignment <-- Required
        )
        
        ls = self.Tokenizer.tokenize(text)
        ls = self.Splitter.split(self.SessionId,ls,False)
        ls = self.Morfo.analyze(ls)
        ls = self.Tagger.analyze(ls)
        
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
    
    
    def __init__(self, source, data=DATA, lang=LANG, pwl=PWL, *args, **kwargs):
        super(Preprocess, self).__init__(data, lang, pwl, *args, **kwargs)
        self._source = source
        self._lang   = lang
        self._sents  = defaultdict(list)
        
        
    def __repr__(self):
        return "< %s.%s in %s (%s) >" % (self.__class__.__module__, self.__class__.__name__, self._source, self._lang)
        
        
    def __str__(self):
        return "%s in %s" % ( self._source , self._lang.upper() ) 
        
        
    def run(self, opinions, verbose=True, tofile=None):
        if not opinions:
            raise ValueError('Nothing to itemize')
        
        _ids = []
        total = len( list ( opinions ) ) ; fails = 0 
        for idx, opinion in enumerate(opinions):
            if verbose: progress("Preprocessing %s (Fails %05.2f%%)" %  ( self._source, 100.0*fails/total ), total, idx )  
                         
            _id = md5.new(str(opinion['category']) + opinion['text'].encode('ascii', 'ignore')).hexdigest()
            
            if _id in _ids:
                log("Repeated opinion '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self._source ) )
                continue
                
            _ids.append(_id)
            
            text = opinion['text']
            text = self._correct(text)
            sent = self._analyze(text)
            
            if not sent:
                fails += 1
                log("Empty analysis for '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self._source ) )
                continue
            
            self._sents[ opinion['category'] ].append({
                '_id' : _id,
                'text':[{
                    'word'  : token['form'],
                    'lemma' : token['lemma'],
                    'tag'   : token['tag']
                } for token in sent ]
            })
            
            if idx % 500 == 0 and tofile: # partial dump
                save( self._sents , "preproc_%s" % self._source , tofile )
            
        if tofile: save( self._sents , "preproc_%s.json" % self._source , tofile )
        
    
    def categories(self):
        return self._sents.keys()
    
        
    def sents(self,category=None):
        if category is None:
            return sum( self._sents.values() , [] )
        else:
            return self._sents[category]
            
