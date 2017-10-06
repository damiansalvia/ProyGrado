# -*- encoding: utf-8 -*-
import freeling 
import os
from enchant import DictWithPWL
from enchant.checker import SpellChecker
from difflib import get_close_matches


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

        # Create analyzers
        self.tk  = freeling.tokenizer(DATA+LANG+"/tokenizer.dat")
        self.sp  = freeling.splitter(DATA+LANG+"/splitter.dat")
        self.mf  = freeling.maco(op)

        # create tagger and alternatives
        self.tg  = freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2)
        self.alts_ort = freeling.alternatives(DATA+LANG+"/alternatives-ort.dat")
        self.alts_phon = freeling.alternatives(DATA+LANG+"/alternatives-phon.dat")
        
        self.sid = self.sp.open_session()
        
    def __del__(self):
        self.sp.close_session(self.sid)


    def analyze(self,text):
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8')
        
        # Correction from alternatives
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
            False   # Probability Assignment <-- Required
        )
        ls = self.tk.tokenize(text)
        ls = self.sp.split(self.sid,ls,False)
        ls = self.mf.analyze(ls)
        ls = self.alts_ort.analyze(ls)
#         ls = self.alts_phon.analyze(ls)
        unk = [] ; text = ""
        for sentence in ls :
            for token in sentence.get_words() :
                word  = token.get_form()
                alts  = token.get_alternatives()
                known = token.found_in_dict()
                fact = len(word) / ( word.count('_') + 1 )  
                for wd in word.split('_'):
                    wd = wd.lower() if len(wd) < 5 else wd
                    if not known:
                        unk.append( wd )
                    text += ' '+ wd
                
#                 if raw_input(token.get_lc_form()+' > ') == 'd':
#                     import pdb;pdb.set_trace()           
        if unk: # Do word correction
            chkr.set_text(text)
            for err in chkr:
                if not err.word in unk: # Avoid correct nouns
                    continue
                sugg = [ s for s in chkr.suggest(err.word) if '-' not in s ]
                alts = get_close_matches( err.word , sugg , 3 , 0.80 )
                if alts   : corr = alts[0]
                elif sugg : corr = sugg[0]
                else      : corr = err.word
                err.replace(corr)
            text = chkr.get_text()
            unk = []
        
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
                
#         self.sp.close_session(sid)
        return sent


#--------------- EXAMPLE ---------------

if __name__ == "__main__":

    analiyzer = Analyzer()
    while True:
        text = raw_input('> ')
        if not text: break
        result =  analiyzer.analyze(text)
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

