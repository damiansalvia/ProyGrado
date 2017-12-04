# -*- coding: utf-8 -*-
'''
Module for preliminar preprocess of corporea text

@author: Nicolás Mechulam, Damián Salvia
'''

import freeling, os, enchant, re, md5
from enchant.checker import SpellChecker
from difflib import get_close_matches
from collections import defaultdict, Counter

from cldas.utils import progress, save
from cldas.utils.misc import Iterable, Levinstein
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
        self.Vocabulary   = Levinstein()
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
    # Replace emojis by a special tag
    (u"<?[:;=8xX][-‑o\']?[\)\]3dDoOpP\*\}]|[\(\[cC\{][-‑o\*\']?[:;=8]>?",u"FELIZ"),
    (u">?[:;=][-‑o\']?[\(\[cC\{\\\/\|@_]|[\)\]dD\}\\\/\|@_][-‑o\']?[:;=8xX]<?",u"TRISTE"),
    # Remove URIs with scheme http or https
    (u"(https?:\/\/\S+)",u"LINK"),
    # Remove repetitive characters (except (ll)egar, pe(rr)o and a(cc)ion ) <-- will be corrected by aspell
    (u"([^lrc])\\1+",u"\\1"),
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
    # Force dot ending
    (u"([^\w\?!\)\"])$",u""), (u"([^\.])$",u"\\1 ."),
    # Replace multiple blank spaces by one
    (u"\s\s+",u" ")
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
        
        self.Checker.set_text( text )
        for err in self.Checker:
            word = err.word
            cand = self.Vocabulary.correction( word )
            sugg = self.Checker.suggest( word )
            alts = get_close_matches( word, sugg, 5, 0.90 )
            if word in nouns:
                corr = word
            elif alts and not re.search('[\s-]',alts[0]) and len(alts) <= 2:
                corr = alts[0].lower()
            elif sugg and ( re.search('[\xe1\xe9\xed\xf3\xfa\xfc]',sugg[0].lower()) or len(sugg)<=5 ):
                corr = sugg[0].lower()
            elif word in ack:
                corr = word.lower()
            else:
                corr = cand
            import pdb;pdb.set_trace()
            err.replace( corr )
        text = self.Checker.get_text()
                           
#         words = text.split(' ')
#         for i in range( len( words ) ):
#             word = words[i]
#             if not word: 
#                 continue
#             if (word in ack) or self.Checker.check( word ):
#                 word = word.lower()
#             else:
#                 word_na = self._no_accent( word )
#                 sugg = { self._no_accent(s):s for s in self.Checker.suggest( word_na ) if ('-' not in s) }
#                 alts = get_close_matches( word_na , sugg.keys() , 5 , 0.75   )
#                 if   alts : corr = sugg[ alts[0] ].lower()
#                 elif sugg : corr = sugg.keys()[0].lower() if (word not in nouns) else word
#                 else : 
#                     self.Checker.set_text( word )
#                     for err in self.Checker:
#                         corr = self.Checker.suggest( err.word ) 
#                         err.replace( corr[0] if corr else err.word )
#                     word = self.Checker.get_text()
#                     corr = word.lower() if (word not in nouns) else word
#                 word = corr
#             words[i] = word
#         text = ' '.join(words)
            
        return text



class _MorfoTokenizer(_SingletonSettings):
    '''
    Class for making text tokenizaion, lemmatization and POS-tagging
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
    
    
    def __init__(self, source, opinions, data=DATA, lang=LANG, pwl=PWL, verbose=True, *args, **kwargs):
        super(Preprocess, self).__init__(data, lang, pwl, *args, **kwargs)
        self.source = source
        self._lang   = lang
        self._sents  = defaultdict(list)
        self._fails  = []
         
        self._run(opinions,verbose)
        
        
    def _run(self, opinions, verbose):
        if not opinions:
            return
        
        vocabulary = Counter( word for opinion in opinions for word in re.findall(r'\w+',opinion['text'].lower()) )
        self.Vocabulary.set_vocabulary(vocabulary)
        
        _ids = []
        total = len( opinions ) ; fails = 0 
        for idx, opinion in enumerate(opinions):
            
            if verbose: progress("Preprocessing %s (Fails %05.2f%%)" %  ( self.source, 100.0*fails/total ), total, idx )  
                         
            _id = md5.new( "%s %s" % (str(opinion['category']),opinion['text'].encode('ascii', 'ignore')) ).hexdigest()
            
            if _id in _ids:
                log("Repeated opinion '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self.source ) , level=Level.ERROR)
                continue
            
            text = opinion['text']
            text = self._correct(text)
            sent = self._analyze(text)
            
            if not sent:
                fails += 1
                self._fails.append( "'%s'\n\n==>'%s'" % ( opinion['text'], text ) )
                log("Empty analysis for '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self.source ) , level=Level.ERROR)
                continue
                
            _ids.append(_id)
            
            tags  = opinion.get('tags',None)
            if tags is None:
                items = [{
                    'word'   : token['form'],
                    'lemma'  : token['lemma'],
                    'tag'    : token['tag'],
                } for token in sent ]
            else: # TO-DO Please improve me !!                
                try: items = self.__get_items_from_tags(tags,opinion,sent)
                except Exception as e:
                    self._fails.append( "'%s'\n\n==>'%s'" % ( ' '.join( wd+"/"+tag for wd,tag in zip(opinion['text'],tags) ), text ) ) 
                    log("BIO parsing fail for '%s' (at %s)" % ( opinion['text'].encode('ascii','ignore') , self.source ) , level=Level.ERROR)
                    fails += 1 
                    continue
            
            self._sents[ opinion['category'] ].append({
                '_id' : _id,
                'text': items
            })
    
    
    def __get_items_from_tags(self,tags,opinion,sent): # TO-DO Please improve me !! 
                
            def flat(text):
                return text.replace(u'\xe1','a').replace(u'\xe9','e').replace(u'\xed','i').replace(u'\xf3','o').replace(u'\xfa','u').replace(u'\xfc','u').replace(u'\xf1','n')
            
            bio = [ ( self._correct(wd)[:-1].strip(), tag ) for wd,tag in zip( opinion['text'].split(' '), tags ) ]
            i = 0 ; j = 0
            items = [] ; t1 = len(sent) ; t2 = len(bio)
            while i < t1 and j < t2:
                if sent[i]['form'] == bio[j][0]: # Are equels
                    last = "CASE 1"
                    items.append( ( sent[i], bio[j][1] ) )
                    i+=1 ; j+=1
                elif flat(sent[i]['form']) in flat(bio[j][0]): # Is substring of
                    last = "CASE 4"
                    while flat(sent[i]['form']) in flat(bio[j][0]):
                        items.append( ( sent[i], bio[j][1] ) )
                        i+=1
                    j+=1
                elif len(sent[i]['form'])==1 and bio[j][0]==u'':
                    items.append( ( sent[i], bio[j][1] ) )
                    i+=1 ; j+=1 
                elif len(sent[i]['form'])>1 and bio[j][0]==u'':
                    j+=1 
                else:
                    
                    j1 = j+1
                    while j1 < t2 and sent[i]['form'] != bio[j1][0]: # Look ahead if are equals
                        j1+=1 
                    if j1 < t2:
                        last = "CASE 5"    
                        j = j1
                        continue
                    
                    i1 = i+1
                    while i1 < t1 and sent[i1]['form'] != bio[j][0]: # Look ahead if are equals
                        i1+=1
                    if i1 < t1:
                        last = "CASE 4"
                        items.append( ( sent[i], bio[j][1] ) )
                        i = i1 
                        continue
                    
                    i1 = i+1 ; j1 = j+1
                    while i1 < t1 and j1 < t2 and sent[i1]['form'] != bio[j1][0]: # Look ahead if are equals
                        i1+=1 ; j1+=1 
                    if i1 < t1:
                        last = "CASE 5"    
                        items.append( ( sent[i], bio[j][1] ) )
                        i+=1 ; j+=1
                        continue
                    
                    raise Exception()
                
            items = [{
                'word'   : token['form'],
                'lemma'  : token['lemma'],
                'tag'    : token['tag'],
                'negated': False if tag == 'O' else None if tag == 'B-NEG' else True
            } for token,tag in items ]
            
            return items
    
       
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
    
    
    def failures(self):
        return self._fails
    
    
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
    