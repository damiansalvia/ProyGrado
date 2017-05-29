# -*- coding: utf-8 -*-

from corpus_parser_strategies import *
import json, io, string, ast, time

import sys # Para ver UTF8 en consola
reload(sys)
sys.setdefaultencoding('utf-8')

import os

#=====================================================================

alphabet = "abcdefghijklmnñopqrstuvwxyzáéíóúü¿?¡!(),.:;'"


substitutions = [
    # Replace non-spanish characters with hipotetical correct character
    (u"à","á"), (u"è","é"), (u"ì","í"), (u"ò","ó"), (u"ù","ú"),
    (u"â","á"), (u"ê","é"), (u"î","í"), (u"ô","ó"), (u"û","ú"),
    (u"À","Á"), (u"È","É"), (u"Ì","Í"), (u"Ò","Ó"), (u"ù","Ú"),
    (u"ä","á"), (u"ë","é"), (u"ï","í"), (u"ö","ó"),
    (u"Ä","A"), (u"Ë","E"), (u"Ï","I"), (u"Ö","O"),
    (u"å","a"), (u"ç","c"),
    # Replace other non-spanish characters
    (u"`","\""),(u"´","\""),
    (u"\'","\""),
    # Replace every ocurrence of repetitive characters except {l,r,c,e} [cabaLLo, coRRer, aCCion, crEE]
    (u"(?i)([abdf-km-qs-z])\\1+","\\1"),
    (u"(?i)([lrce])\\1\\1+","\\1\\1"),
    (u"(?i)([lrce])\\1(\W)","\\1\\2"),
    # Force every review (document) to end with a period
    (u"(\w)(?:\.)?',","\\1 .\',"),
    # Separate alpabetical character from non-alphabegical character by a blank space
    (u"(?i)([a-záéíóúñ]?)([^\wáéíóúñ\s]|(?:{.*?}|\[.*?\])]+)([a-záéíóúñ]?)","\\1 \\2 \\3"),
#     (r" \\ u","\u"),
    # Replace multiple blank spaces by one
    (u"(\s){2,}"," "),
    # Adjust for eval
    (u"\"","'"),
    (u"\r?\n",""),
    (u"\t"," "),
    (u"}\s,\s{","},{"),
    (u"(?i)'\s?review\s?'\s?:\s?'(.*?)'\s?,\s?'\s?rank\s?'\s?:\s?(\d+)","\"review\": \"\\1\",\"rank\": \\2"),
]

def correct(lst):
    content = json.dumps(lst)
    content = content.decode('unicode-escape')
    total = len(substitutions)
    # Substitute every rule
    for idx, (source,target) in enumerate(substitutions):
        progressive_bar("Preprocessing",total,idx)
        content = re.sub(source,target,content,flags=re.DOTALL)
    content = content.replace("\\", r"\\")
    # Retrieve result
    progressive_bar("Preprocessing",total,idx+1)
    ret = json.loads(content.encode('utf8'))
    assert len(ret) == len(lst)
    return ret

#=====================================================================
class CorpusParser:
    
    def __init__(self,input_dir,ldir='./'):
        if not os.path.isdir(ldir): os.makedirs(ldir)
        self.log  = Log(ldir)
        self.res  = []
        input_dir = input_dir.replace("\\","/")
        self.dir  = input_dir if input_dir[-1] != "/" else input_dir[:-1]
        self.name = input_dir.split("/")[-1]
        self.alg  = globals()[self.name]

    def parse(self):
        self.res = self.alg(self.dir,self.log)
        self.res = correct(self.res)
        return self.res
    
    def get_parsed(self):
        return self.res
        
    def save(self,output_dir='outputs/corpus'):
        if not os.path.isdir(output_dir): os.makedirs(output_dir)
        cdir = "%s/%s.json" % (output_dir,self.name)
        with io.open(cdir,"w",encoding='utf8') as ofile:
            content = json.dumps(self.res,indent=4,ensure_ascii=False)
            if not isinstance(content, unicode):
                content = unicode(content,'utf8')
            ofile.write(content)
        print "Result was saved in %s\n" % cdir

#=====================================================================
if __name__ == "__main__":
    
    start_time = time.time()
    
    test = [{"review":u"Eeesto ès +++++prûebä \\ddde estrés `usando´ ''aquellos casos \" *********borde``a procesar´´","rank":10}]
    ret = correct(test)
    print ret
    print ret[0]['review']#.decode('utf8')
    
    parser = CorpusParser("../../corpus/corpus_cine")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()    
           
    parser = CorpusParser("../../corpus/corpus_hoteles")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()
          
    parser = CorpusParser("../../corpus/corpus_prensa_uy")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()
        
    parser = CorpusParser("../../corpus/corpus_tweets")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()
       
    parser = CorpusParser("../../corpus/corpus_variado_sfu")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()
         
    parser = CorpusParser("../../corpus/corpus_apps_android")
    parser.parse()
    res = parser.get_parsed()
    print "%i retrived" % len(res), type(res[0]['review'])
    parser.save()
    
    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
