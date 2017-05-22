# -*- coding: utf-8 -*-

from corpus_parser_strategies import *
import json, io, string, ast

#=====================================================================

substitutions = [
    # Replace non-spanish characters with hipotetical correct character
    ("à","á"), ("è","é"), ("ì","í"), ("ò","ó"), ("ù","ú"),
    ("â","á"), ("ê","é"), ("î","í"), ("ô","ó"), ("û","ú"),
    ("À","Á"), ("È","É"), ("Ì","Í"), ("Ò","Ó"), ("ù","Ú"),
    ("ä","á"), ("ë","é"), ("ï","í"), ("ö","ó"),
    ("Ä","A"), ("Ë","E"), ("Ï","I"), ("Ö","O"),
    ("å","a"), ("ç","c"),
    # Replace every ocurrence of repetitive characters except {l,r,c,e} [cabaLLo, coRRer, aCCion, crEE]
    ("(?i)([abdf-km-qs-z])\\1+","\\1"),
    ("(?i)([lrce])\\1\\1+","\\1\\1"),
    ("(?i)([lrce])\\1(\W)","\\1\\2"),
    #Force every review (document) to end with a period
    ("(\w)(?:\.)?',","\\1 .\',"),
    # Separate alpabetical character from non-alphabegical character by a blank space
    ("(?i)([a-záéíóú]?)(\(|\)|\.|;|:|[^\wáéíóú\s\\\(?:{.*?}|\[.*?\])]+)([a-záéíóú]?)","\\1 \\2 \\3"),
    # Replace multiple blank spaces by one
    ("(\s){2,}"," "),
    # Adjust for eval
    ("\"","'"),
    ("\r?\n",""),
    ("\t"," "),
    ("}\s,\s{","},{"),
    ("(?i)'\s?review\s?'\s?:\s?'(.*?)'\s?,\s?'\s?rank\s?'\s?:\s?(\d+)","\"review\": \"\\1\",\"rank\": \\2"),
]

def correct(lst):
    content = json.dumps(lst)
    content = content.decode('string-escape')
    total = len(substitutions)
    # Substitute every rule
    for idx, (source,target) in enumerate(substitutions):
        progressive_bar("Preprocessing",total,idx)
        content = re.sub(source,target,content,flags=re.DOTALL)
    content = content.replace("\\", r"\\")
    # Retrieve result
    progressive_bar("Preprocessing",total,idx+1)
    ret = json.loads(content)
    assert len(ret) == len(lst)
    return ret

#=====================================================================
class ParseCorpus:
    def __init__(self,cdir):
        self.revs = []
        self.dir  = cdir if cdir[-1] != "/" else cdir[:-1]
        self.name = cdir.split("/")[-1]
        self.alg  = globals()[self.name]

    def parse(self):
        self.revs = self.alg(self.dir)
        self.revs = correct(self.revs)
     
    def get(self):
        return self.revs    
        
    def save(self,dest='outputs/corpus'):
        cdir = "%s/%s.json" % (dest,self.name)
        with io.open(cdir, "w", encoding='utf8') as ofile:
            content = json.dumps(self.revs,indent=4,sort_keys=True,ensure_ascii=False)
            if not isinstance(content, unicode):
                content = unicode(content,'utf8')
            ofile.write(content)
        print "Result was saved in %s\n" % cdir

#=====================================================================
if __name__ == "__main__":
    parser = ParseCorpus("../../corpus/corpus_cine")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()    
  
    parser = ParseCorpus("../../corpus/corpus_hoteles")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()
    
    parser = ParseCorpus("../../corpus/corpus_prensa_uy")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()
    
    parser = ParseCorpus("../../corpus/corpus_tweets")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()
   
    parser = ParseCorpus("../../corpus/corpus_variado_sfu")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()
   
    parser = ParseCorpus("../../corpus/corpus_apps_android")
    parser.parse()
    print "%i retrived" % len(parser.get())
    parser.save()