# -*- encoding: utf-8 -*-
import freeling 
import os
from enchant import DictWithPWL
from enchant.checker import SpellChecker
from difflib import get_close_matches, SequenceMatcher


DATA = "/usr/local/share/freeling/"
LANG="es"

assert os.path.getsize('../utilities/es-lat') > 0
my_dict = DictWithPWL('es', '../utilities/es-lat')
assert my_dict.provider.name == 'aspell'
chkr = SpellChecker(my_dict)


class Analyzer:

    def __init__(self):

        freeling.util_init_locale("default")

        # Create options set for maco analyzer
        op = freeling.maco_options(LANG)
        op.PunctuationFile  = DATA + "common/punct.dat"
        op.DictionaryFile   = DATA + LANG + "/es-ar/dicc.src"
        op.AffixFile        = DATA + LANG + "/afixos.dat"
        op.LocutionsFile    = DATA + LANG + "/locucions.dat"
        op.NPdataFile       = DATA + LANG + "/np.dat"
        op.QuantitiesFile   = DATA + LANG + "/quantities.dat" 
        op.ProbabilityFile  = DATA + LANG + "/probabilitats.dat" 

        # Create analyzers
        self.tk  = freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
        self.sp  = freeling.splitter(DATA+LANG+"/splitter.dat")
        self.mf  = freeling.maco(op)

        # create tagger and alternatives
        self.tg  = freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2)
        self.alts_ort = freeling.alternatives(DATA+LANG+"/alternatives-ort.dat")
        
        # known words
        self.wknown = []
        
        self.sid = self.sp.open_session()
        
        
    def __del__(self):
        self.sp.close_session(self.sid)
    

    def analyze(self,text):
        
        def no_accent(text):
            return text.replace(u'á',u'a').replace(u'é',u'e').replace(u'í',u'i').replace(u'ó',u'o').replace(u'ú',u'u').replace(u'ü',u'u')
        
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8') 
        
        # Check which words are correct
        self.mf.set_active_options(
            False, # User Map
            False,  # Number Detection 
            True,  # Punctuation Detection 
            False,  # Date Detection 
            True,  # Dictionary Search 
            True,  # Affix Analysis
            False, # Compound Analysis
            True,  # Retok Contractions
            False,  # Multiword Detection 
            False,  # NER                    <-- Required
            False,  # Quantities Detection
            False   # Probability Assignment <-- Required
        )
        ls = self.tk.tokenize( text )
        ls = self.sp.split(self.sid,ls,False)
        ls = self.mf.analyze(ls)
        ls = self.alts_ort.analyze(ls) 
        ack = []  
        for sentence in ls :
            for token in sentence.get_words() :
                word = token.get_form()
                for word in word.split('_'):
                    if token.found_in_dict(): 
                        ack.append( word )
        
        # Check which words are correct
        self.mf.set_active_options(
            False, # User Map
            False,  # Number Detection 
            True,  # Punctuation Detection 
            False,  # Date Detection 
            True,  # Dictionary Search 
            True,  # Affix Analysis
            False, # Compound Analysis
            True,  # Retok Contractions
            False,  # Multiword Detection 
            True,  # NER                    <-- Required
            False,  # Quantities Detection
            False   # Probability Assignment <-- Required
        )
        ls = self.tk.tokenize( text )
        ls = self.sp.split(self.sid,ls,False)
        ls = self.mf.analyze(ls)
        ls = self.alts_ort.analyze(ls) 
        nouns = []  
        for sentence in ls :
            for token in sentence.get_words() :
                word = token.get_form()
                for word in word.split('_'):
                    if token.found_in_dict(): 
                        nouns.append( word )
        nouns = list( set(nouns) - set(ack) )
                    
        # Replace those incorrect words and normalize correct ones 
        words = text.split(' ')
        for i in range( len(words) ):
            word = words[i]
            if not word: 
                continue
            if (word in ack) or chkr.check(word):
                word = word.lower()
            else:
                word_na = no_accent(word)
                sugg = { no_accent(s):s for s in chkr.suggest( word_na ) if ('-' not in s) }
                alts = get_close_matches( word_na , sugg.keys() , 5 , 0.75   )
                if   alts : corr = sugg[ alts[0] ].lower()
                elif sugg : corr = sugg.keys()[0].lower() if (word not in nouns) else word
                else : 
                    chkr.set_text(word)
                    for err in chkr:
                        corr = chkr.suggest( err.word ) 
                        err.replace( corr[0] if corr else err.word )
                    word = chkr.get_text()
                    corr = word.lower() if (word not in nouns) else word
#                 import pdb;pdb.set_trace()
                word = corr
            words[i] = word
        text = ' '.join(words)
            
        # Analyze result
        self.mf.set_active_options(
            False, # User Map
            False,  # Number Detection 
            True,  # Punctuation Detection 
            False,  # Date Detection 
            True,  # Dictionary Search 
            True,  # Affix Analysis
            False, # Compound Analysis
            True,  # Retok Contractions
            False,  # Multiword Detection 
            True,  # NER 
            False,  # Quantities Detection
            True   # Probability Assignment <-- Required
        )
        ls = self.tk.tokenize(text)
        ls = self.sp.split(self.sid,ls,False)
        ls = self.mf.analyze(ls)
        ls = self.tg.analyze(ls)
        sent = []
        for sentence in ls :
            for token in sentence.get_words() :
                sent.append({
                    "form"  : token.get_lc_form(),
                    "lemma" : token.get_lemma(), 
                    "tag"   : token.get_tag()
                })
        
        return sent


#--------------- EXAMPLE ---------------

if __name__ == "__main__":

    analiyzer = Analyzer()
    while True:
        text = raw_input('> ')
        if not text: break
        result =  analiyzer.analyze(text)
        print "INPUT :",text
        print "OUTPUT:",' '.join([tok['form'] for tok in result])
        for res in result: print res
#     #------------------------------------------------------
#     print "\n   With unkown words"
#     result =  analiyzer.analyze("Horrible Se cuelga. Tengo Nexus y Maria Soledad Garcia ttienne un Google que es buenisimo jajaja. Queres ir al 23 a haser ALGO o no quereis xq es mini jeje. Revis mi mail.")
#     for res in result: print res
#     #------------------------------------------------------
#     print "\n   Unfinished phrase"
#     print analiyzer.analyze("Esto es una prueba")
#     #------------------------------------------------------
#     print "\n   Complete phrase"
#     print analiyzer.analyze("Esto es una prueba.")
#     #------------------------------------------------------
#     print "\n   Exclamation phrase"
#     print analiyzer.analyze("Esto es una prueba!")
#     #------------------------------------------------------
#     print "\n   Question phrase"
#     print analiyzer.analyze("¿Será esto una prueba?")
#     #------------------------------------------------------
#     print "\n   Phrases with special characters"
#     print analiyzer.analyze("Mañana haré pruebas con pingüinos.")

