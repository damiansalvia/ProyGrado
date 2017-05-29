# -*- encoding: utf-8 -*-

import freeling 

DATA = "/usr/local/share/freeling/";
LANG="es";

freeling.util_init_locale("default");

# create language analyzer
la=freeling.lang_ident(DATA+"common/lang_ident/ident.dat");

# create options set for maco analyzer. Default values are Ok, except for data files.
op= freeling.maco_options("es");
op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
                   DATA + LANG + "/probabilitats.dat");

# create analyzers
tk=freeling.tokenizer(DATA+LANG+"/tokenizer.dat");
sp=freeling.splitter(DATA+LANG+"/splitter.dat");
sid=sp.open_session();
mf=freeling.maco(op);


# activate mmorpho odules to be used in next call
mf.set_active_options(False, True, True, True,  # select which among created 
                      True, True, False, True,  # submodules are to be used. 
                      True, True, True, True ); # default: all created submodules are used

# create tagger, sense anotator, and parsers
tg=freeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
sen=freeling.senses(DATA+LANG+"/senses.dat");
parser= freeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat");
dep=freeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", parser.get_start_symbol());

# process input text
import sys

lin = True

while lin:

  lin = unicode(sys.stdin.readline(), 'utf8')
  #lin= u"Esto es una explicación." #.encode('utf-8') #.encode('iso-8859-1')
  #print  "Text language is: "+la.identify_language(lin,["es","ca","en","it"])+"\n" 
  l = tk.tokenize(lin);
  ls = sp.split(sid,l,False);

  ls = mf.analyze(ls);
  ls = tg.analyze(ls);

  ## output results

  for s in ls :
     ws = s.get_words();
     print "-----";
     sent = []
     for w in ws :
        print  w.get_form().encode('utf8') + " - ",
        print w.get_lemma().encode('utf8')  + " ",
        print  w.get_tag()
        sent.append(tuple( (w.get_form().encode('utf8'), w.get_lemma().encode('utf8'), w.get_tag()) ))

     print sent

     print "-----";

    
# clean up       
sp.close_session(sid);

# Spanish uses a number of non-ASCII characters, such as á, é, ñ, etc. These characters can come in different encodings. 
# To be able to correctly analyze text with these characters, Freeling analyzer should receive the input in ISO encoding.
# Thus, the input text needs an additional preprocessing stage to be converted into this encoding.
# Though this might look as a minor technical issue, guessing the original encoding becomes a significant problem when working with texts from arbitrary sources on the Web. We discuss encoding related issues in Section 4.2.

# http://acl2014.org/acl2014/P14-3/pdf/P14-3011.pdf
# pagina 80
