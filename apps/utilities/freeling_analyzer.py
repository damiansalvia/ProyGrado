# -*- encoding: utf-8 -*-
import freeling 

class Analyzer:

    def __init__(self):
        DATA = "/usr/local/share/freeling/";
        LANG="es";

        freeling.util_init_locale("default");

        # create language analyzer
        # la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

        # create options set for maco analyzer. Default values are Ok, except for data files.
        op= freeling.maco_options("es");
        op.set_data_files( 
            "", 
            DATA + "common/punct.dat",
            DATA + LANG + "/dicc.src",
            DATA + LANG + "/afixos.dat",
            "",
            DATA + LANG + "/locucions.dat", 
            DATA + LANG + "/np.dat",
            DATA + LANG + "/quantities.dat",
            DATA + LANG + "/probabilitats.dat"
        );

        # create analyzers
        self.tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
        self.sp=freeling.splitter(DATA+LANG+"/splitter.dat");
        self.sid=self.sp.open_session();
        self.mf=freeling.maco(op);

        # activate mmorpho odules to be used in next call
        self.mf.set_active_options(False, True, True, True,  # select which among created 
                              True, True, False, True,  # submodules are to be used. 
                              True, True, True, True ); # default: all created submodules are used

        # create tagger, sense anotator, and parsers
        self.tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
        self.sen=freeling.senses(DATA+LANG+"/senses.dat");
        
        # parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
        # self.dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());


    def analyze(self,text):
        sid =self.sp.open_session();
        if not isinstance(text, unicode):
            text = unicode(text, 'utf8')
        l  = self.tk.tokenize(text);
        ls = self.sp.split(self.sid,l,False);

        ls = self.mf.analyze(ls);
        ls = self.tg.analyze(ls);

        ## output results

        sent = []
        for s in ls :
            ws = s.get_words();
            for w in ws :
                sent.append({
                    "form"  : w.get_form(),
                    "lemma" : w.get_lemma(), 
                    "tag"   : w.get_tag()
                })

        self.sp.close_session(sid);
        return sent

#--------------- EXAMPLE ---------------

if __name__ == "__main__":

    analiyzer = Analyzer()
    #------------------------------------------------------
    print "\n   Unfinished phrase"
    print analiyzer.analyze("Esto es una prueba")
    #------------------------------------------------------
    print "\n   Complete phrase"
    print analiyzer.analyze("Esto es una prueba.")
    #------------------------------------------------------
    print "\n   Exclamation phrase"
    print analiyzer.analyze("Esto es una prueba!")
    #------------------------------------------------------
    print "\n   Question phrase"
    print analiyzer.analyze("¿Será esto una prueba?")
    #------------------------------------------------------
    print "\n   Phrases with special characters"
    print analiyzer.analyze("Mañana haré pruebas con pingüinos.")

