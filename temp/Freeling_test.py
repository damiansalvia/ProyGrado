#!/usr/bin/python
# -*- encoding: utf-8 -*-
import freeling
import sys

# ## ------------  output a parse tree ------------
# def printTree(ptree, depth):

#     node = ptree.begin();

#     print ''.rjust(depth*2);
#     info = node.get_info();
#     if (info.is_head()): 
#         print '+';

#     nch = node.num_children();
#     if (nch == 0) :
#         w = info.get_word();
#         print w.get_form() + ' ' + w.get_lemma() + ' ' + w.get_tag();

#     else :
#         print('{0}_['.format(info.get_label()));

#         for i in range(nch) :
#             child = node.nth_child_ref(i);
#             printTree(child, depth+1);

#         print ''.rjust(depth*2);
#         print ']';
        
#     print('');

# ## ------------  output a parse tree ------------
# def printDepTree(dtree, depth):

#     node = dtree.begin()

#     print ''.rjust(depth*2);

#     info = node.get_info();
#     link = info.get_link();
#     linfo = link.get_info();
#     print link.get_info().get_label() +'/'+ info.get_label()+ '/' ;

#     w = node.get_info().get_word();
#     print w.get_form() + ' ' + w.get_lemma() + ' ' + w.get_tag();

#     nch = node.num_children();
#     if (nch > 0) :
#         print(' [');

#         for i in range(nch) :
#             d = node.nth_child_ref(i);
#             if (not d.begin().get_info().is_chunk()) :
#                 printDepTree(d, depth+1);

#         ch = {};
#         for i in range(nch) :
#             d = node.nth_child_ref(i);
#             if (d.begin().get_info().is_chunk()) :
#                 ch[d.begin().get_info().get_chunk_ord()] = d;
 
#         for i in sorted(ch.keys()) :
#             printDepTree(ch[i], depth + 1);

#         print ''.rjust(depth*2);
#         print ']';

#     print '';



## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local";

DATA = FREELINGDIR+"/share/freeling/";
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
print "Input >"
lin=sys.stdin.readline();



# print  "Text language is: "+la.identify_language(lin,["es","ca","en","it"])+"\n" 

while (lin) :
        
    l = tk.tokenize(lin);
    ls = sp.split(sid,l,False);

    ls = mf.analyze(ls);
    ls = tg.analyze(ls);
    ls = sen.analyze(ls);
    ls = parser.analyze(ls);
    ls = dep.analyze(ls);

    ## output results
    for s in ls :
       ws = s.get_words();
       for w in ws :
          print w.get_form()+" "+w.get_lemma()+" "+w.get_tag()
       print "-----";

       # tr = s.get_parse_tree();
       # printTree(tr, 0);

       # dp = s.get_dep_tree();
       # printDepTree(dp, 0)

    lin=sys.stdin.readline();
    
# clean up       
sp.close_session(sid);
