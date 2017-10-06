# -*- coding: utf-8 -*-
'''
Module for preprocessing corporea text

@author: Nicolás Mechulam, Damián Salvia
'''

import freeling, os, enchant, re
from enchant.checker import SpellChecker
from difflib import get_close_matches
from utils import progress, Log

log = Log("./log")


class _SingletonSettings:
    '''
    Singleton class with the required settings
    '''
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_SingletonSettings, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,DATA,LANG,PWL):
        
        custom_dict = enchant.DictWithPWL(LANG, PWL)
        
        freeling.util_init_locale("default")
        
        op = freeling.maco_options(LANG)
        op.set_data_files( 
            "", 
            DATA + "common/punct.dat",
            DATA + LANG + "/es-ar/dicc.src",
            DATA + LANG + "/afixos.dat",
            "",
            DATA + LANG + "/locucions.dat", 
            DATA + LANG + "/np.dat",
            DATA + LANG + "/quantities.dat",
            DATA + LANG + "/probabilitats.dat"
        )
        
        self.Checker      = SpellChecker(custom_dict)
        self.Tokenizer    = freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
        self.Splitter     = freeling.splitter(DATA+LANG+"/splitter.dat")
        self.Morfo        = freeling.maco(op)
        self.Tagger       = freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2)
        self.Ortographic  = freeling.alternatives(DATA+LANG+"/alternatives-ort.dat")
        
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
    ("\xc2\x93",u"\""),("\xc2\x94",u"\""),
    (u'\u2026',u'...'),
    # Eliminate multiple co-joined quotes
    (u"\"\s\*\"",u"\""),     
    # Replace multiple periods by one
    (u"(\.\s*)+",u"."),
    # Replace emojis by a special tag
    (u":\)",u" emoji_feliz "),(u"\(:",u" emoji_feliz "),(u"\sxD\s",u" emoji_feliz "),
    (u":\(",u" emoji_triste "),(u"\):",u" emoji_triste "),
    # Remove URIs with scheme http or https
    (u"(https?:\/\/\S+)",u""),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"([0-9a-záéíóúñü\\\]?)([^0-9a-záéíóúñü_\\\\s]+)([0-9a-záéíóúñü\\\]?)",u"\\1 \\2 \\3"),
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
    # Replace multiple blank spaces by one
    (u"(\s){2,}",u" ")
]    
    
class _SpellCorrector(_SingletonSettings):
    '''
    Makes text correction
    '''
    
    def _correct(self,text):
        
        text = text.decode('utf8')
        if not isinstance(text,unicode):
            text = unicode(text,'utf8')
            
        for source,target in SUBSTITUTIONS:
            text = re.sub(source,target,text,flags=re.DOTALL|re.U|re.I)
            
        pattern = u"<\s(.*?)\s.*?>(.*?)</\s\\1\s>" 
        while re.search(pattern, text, flags=re.DOTALL):
            text = re.sub(pattern,u"\\2",text,flags=re.DOTALL)
        text = re.sub(u"<.*?>",u"",text,flags=re.DOTALL)
        
        text += u" ." 
        text = re.sub(u"(\s+\.)*\s+\.$",u" .",text,flags=re.DOTALL)
        
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
            False   # Probability Assignment <-- Required
        )
        
        ls = self.Tokenizer.tokenize(text)
        ls = self.Splitter.split(self.SessionId,ls,False)
        ls = self.Morfo.analyze(ls)
        ls = self.Ortographic.analyze(ls)
        
        unk = [] ; text = ""
        for sentence in ls :
            for token in sentence.get_words() :
                word  = token.get_lc_form()
                known = token.found_in_dict()
                for wd in word.split('_'):
                    if not known:
                        unk.append( wd )
                    text += ' '+ wd
                           
        if unk: # Do word correction
            self.Checker.set_text(text)
            for err in self.Checker:
                sugg = [ s for s in self.Checker.suggest(err.word) if '-' not in s ]
                alts = get_close_matches( err.word , sugg , 3 , 0.80 )
                if alts   : corr = alts[0]
                elif sugg : corr = sugg[0]
                else      : corr = err.word
                if err.word in unk: # Avoid correct nouns
                    err.replace(corr)
            text = self.Checker.get_text()
            unk = []
            
        return text



class _MofoTokenizer(_SingletonSettings):
    '''
    Makes text tokenizaion, lemmatization and POS-tagging
    '''
    
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
        ls = self.Tokenizer.split(self.sid,ls,False)
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



class Itemize(_SpellCorrector,_MofoTokenizer):
    '''
    Itemize text from corporea by correction, tokenizaion, lemmatization and POS-tagging
    '''
    
    def __new__(cls, *args, **kwargs):
        return super(Itemize, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, DATA, LANG, PWL, *args, **kwargs):
        super(Itemize, self).__init__(DATA, LANG, PWL, *args, **kwargs)
        self._sents = []
    
        
    def itemize(self,text):
        text = self._correct(text)
        sent = self._analyze(text)
        
        if sent:        
            self._sents.append(sent)
        else:
            raise Exception("Empty analysis for '%s'" % text.encode('ascii','ignore') )
            log("Empty analysis for '%s'" % text.encode('ascii','ignore') )
    
        
    def result(self):
        return self._sents
