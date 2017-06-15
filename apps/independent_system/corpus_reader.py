# -*- coding: utf-8 -*-

import sys
import time
sys.path.append('../utilities') # To import 'utilities' modules

from printHelper import *
import re, glob, io, json
#####################################################################

SUBSTITUTIONS = [
    # Replace non-spanish characters with hipotetical correct character
    (u"à",u"á"), (u"è",u"é"), (u"ì",u"í"), (u"ò",u"ó"), (u"ù",u"ú"),
    (u"â",u"á"), (u"ê",u"é"), (u"î",u"í"), (u"ô",u"ó"), (u"û",u"ú"),
    (u"À",u"Á"), (u"È",u"É"), (u"Ì",u"Í"), (u"Ò",u"Ó"), (u"ù",u"Ú"),
    (u"ä",u"á"), (u"ë",u"é"), (u"ï",u"í"), (u"ö",u"ó"),
    (u"Ä",u"A"), (u"Ë",u"E"), (u"Ï",u"I"), (u"Ö",u"O"),
    (u"å",u"a"), (u"ç",u"c"),
    # Replace other non-spanish characters
    (u"`",u"\""),(u"´",u"\""),
    (u"\'",u"\""),
    # Replace every ocurrence of repetitive characters except {l,r,c,e} [cabaLLo, coRRer, aCCion, crEE]
    (u"(?i)([abdf-km-qs-z])\\1+",u"\\1"),
    (u"(?i)([lrce])\\1\\1+",u"\\1\\1"),
    (u"(?i)([lrce])\\1(\W)",u"\\1\\2"),
    # Separate alpabetical character from non-alphabegical character by a blank space
    (u"(?i)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)([^a-záéíóúñüÁÉÍÓÚÑÚ\\\\s]|(?:{.*?}|\[.*?\])]+)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)",u"\\1 \\2 \\3"),
    # Force every review (document) to end with a period
    (u"(.*)[^\.]",u"\\1 ."),
    # Replace all non-alphabetical symbols by a whitespace
    (u"(?i)[^0-9a-záéíóúñüÁÉÍÓÚÑÚ¿\?¡!\(\),\.:;\"\$/]",u" "),
    # Replace multiple blank spaces by one
    (u"(\s){2,}",u" ")
]

def correct(text):
    '''
    Apply simple pattern correction in the input text
    @text: Text for applying the correction. 
    '''
    for source,target in SUBSTITUTIONS:
        text = re.sub(source,target,text,flags=re.DOTALL)
    return text    

#####################################################################

class CorpusReader:
    
    def __init__(self,source,extension,review_pattern,category_pattern,category_location,
             category_position=None, category_level=None,start=0,ldir='./log',decoding='utf8'):
        '''
        Read any sentiment analysis corpus by matching the review/opinion and its category from each file.
        @source: Source directory where corpus files are located.
        @extension: Path pattern to the corpus file ending with its extension (e.g. /*/*/*.xml).
        @review_pattern: Pattern for matching a review.
        @category_pattern: Pattern for matching the category which the review belongs.
        @category_location: Indicates if the category_pattern applies for a FILE content or its PATH.
        @category_position: Indicates if the category_pattern is BEFORE or AFTER review_pattern. Apply for FILE location.
        @category_level: Indicates where the category_pattern should match in the path pattern (extension). Apply for PATH location. 
        @start: Indicates where should start reading the file. By default is 0 (begining). Useful when we want exclude a header in a .csv file (value 1).
        @ldir: Directory for the Log file.
        @decoding: Format for decoding the corpus file. By default "ut8", but it can be "cp1252", "unicode-escape", etc.
        '''    
        # Checking prerequisites
        if not source: 
            raise Exception("No corpus source directory found.")
        if not review_pattern: 
            raise Exception("No pattern for review found.")
        if not category_pattern: 
            raise Exception("No pattern for category found.")
        if not category_location in ["PATH","FILE"]: 
            raise Exception("No category location match.")
        if category_location == "FILE" and not category_position in ["BEFORE","AFTER"]:
            raise Exception("Category location is FILE but no category position found or match (BEFORE or AFTER of review)")
        if category_location == "PATH" and category_level == None:
            raise Exception("Category location is PATH but no category level found.")
        if re.compile(review_pattern).groups > 1:
            raise Exception("Only one group is admitted for review pattern.")
        if re.compile(category_pattern).groups > 1:
            raise Exception("Only one group is admitted for category pattern.")
        # Settings for Log
        if not os.path.isdir(ldir): 
            os.makedirs(ldir)
        self.log  = Log(ldir)
        # Normalize source directory
        source = source.replace("\\","/")
        source = source if source[-1] != "/" else source[:-1]
        # Create a name for the corpus
        self.name = source.split("/")[-1]
        # Create the resource file directory for glob reader
        files_dir = source+'/'+extension
        # Read the corpus from each file
        revs, cats = [], []
        for filename in glob.glob(files_dir):
            # Generate pattern
            filename = filename.replace('\\','/')
            if category_location == "PATH":
                pattern  = "%s/(?:.*?/){%i}%s"%(source.replace(".","\."),category_level,category_pattern)
                regex    = re.compile(pattern,re.DOTALL)
                cats_tmp = regex.findall(filename)
                pattern  = "%s"%review_pattern
            elif category_location == "FILE":
                if category_position == "BEFORE":
                    pattern = "%s.*?%s"%(category_pattern,review_pattern)
                elif category_position == "AFTER":
                    pattern = "%s.*?%s"%(review_pattern,category_pattern)
            # Compile pattern
            regex = re.compile(pattern,re.DOTALL)
            # Read the file content
            with open(filename,'r') as file:
                content = file.read()
                content = content.decode(decoding,'ignore')
            # Find targets
            if category_location == "PATH":
                revs_tmp = regex.findall(content)
                cats_tmp = cats_tmp*len(revs_tmp)
                revs += revs_tmp
                cats += cats_tmp
            elif category_location == "FILE":
                found = regex.findall(content)
                if not found:
                    continue
                if category_position == "BEFORE":
                    cats_tmp,revs_tmp = zip(*found)
                elif category_position == "AFTER":
                    revs_tmp,cats_tmp = zip(*found)
                revs += list(revs_tmp)
                cats += list(cats_tmp)
            assert len(revs_tmp) == len(cats_tmp)
        assert len(revs) == len(cats)
        # Process the input data
        self.opinions = []
        self.categories = []
        total = len(revs)
        for idx in range(total)[start:]:
            progressive_bar("Reading %s" % self.name,total,idx)
            rev = correct(revs[idx])
            cat = cats[idx]
            if rev:
                self.opinions.append(rev)
                self.categories.append(cat)
        progressive_bar("Reading %s" % self.name,total,idx+1)
        
    def get_categories(self):
        '''
        Return a vector which indicates the target values for each review. 
        '''
        return self.categories
    
    def get_opinions(self):
        '''
        Return a vector of each review. 
        '''
        return self.opinions
    
    def get_data(self,mapping=lambda x:x):
        '''
        Return a json style structure (list of dict) which contains every review with its category and an id.
        @mapping: Function that assigns a value for each category on the data. By default leaves as was matched in the corpus. 
        '''
        if not callable(mapping):
            raise Exception("Mapping must be a function")
        total = len(self.opinions)
        data = []
        for idx in range(total):                
            data.append({
                'id'       : idx+1,
                'corpus'   : self.name,
                'review'   : self.opinions[idx], 
                'category' : mapping(self.categories[idx]) 
            })
        return data
    
    def save_read(self,odir='outputs/corpus',mapping=lambda x:x):
        '''
        Save the data read in a json file.
        @odir: Target directory where the file will be saved.
        '''
        # Check output directory and concatenate the filename
        if not os.path.isdir(odir): 
            os.makedirs(odir)
        odir = "%s/%s.json" % (odir,self.name)
        # Get formatted data
        data = self.get_data(mapping)
        # Save it into a the file
        with io.open(odir,"w",encoding='utf8') as f:
            content = json.dumps(data,indent=4,ensure_ascii=False)
            if not isinstance(content, unicode):
                content = unicode(content,'utf8')
            f.write(content)
            
def Test():
    # Correct function test
    obtained = correct(u"1º Acto: Yo haciendo tareäs.\u0083 2º Acto: Yo estudiando. 3º Acto: Yo rècogiendo... ¡mi cuarto!.¿CÓMO SE LLAMA LA OBRA? `No tengo vidaaaa´ 😡")
    expected = u" 1 Acto : Yo haciendo tareás . 2 Acto : Yo estudiando . 3 Acto : Yo récogiendo . . . ¡ mi cuarto ! . ¿ CÓMO SE LLAMA LA OBRA ? \" No tengo vida \" ."
    assert expected == obtained
    
    # CorpusReader test
    corpus = CorpusReader(
        "../../corpus/corpus_apps_android",
        "*/*.json",
        review_pattern ="\"(.*?)\"[,(?:\\r\\n)]",
        category_pattern = "(.*?)/",
        category_location = "PATH",
        category_level=0,
        decoding='unicode-escape'
    )
    assert len(corpus.get_opinions()) == len(corpus.get_categories())
    fun = {'neg':0,'pos':100}
    assert sorted(set(data['category'] for data in corpus.get_data(mapping=lambda x:fun[x]))) == [0,100]
            
##############################
#          EXAMPLES          #
##############################        
if __name__=="__main__":
    
    start_time = time.time()
    
    Test()
    
#     corpus = CorpusReader(
#         "../../corpus/corpus_apps_android",
#         "*/*.json",
#         "\"(.*?)\"[,(?:\\r\\n)]",
#         "(.*?)/",
#         "PATH",
#         category_level=0,
#         decoding='unicode-escape'
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = sorted(list(set(corpus.get_categories())))
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),range(0,size*(len(cats)-1)+1,size/(len(cats)-1))))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:]
#           
#     corpus = CorpusReader(
#         "../../corpus/corpus_cine",
#         "*.xml",
#         "<body>(.*?)</body>",
#         "rank=\"(.*?)\"",
#         "FILE",
#         category_position="BEFORE"
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = sorted(list(set(corpus.get_categories())))
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),range(0,size*(len(cats)-1)+1,size/(len(cats)-1))))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:]
#           
#     corpus = CorpusReader(
#         "../../corpus/corpus_hoteles",
#         "*.xml",
#         "<coah:review>(.*?)</coah:review>",
#         "<coah:rank>(.*?)</coah:rank>",
#         "FILE",
#         category_position="BEFORE"
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = sorted(list(set(corpus.get_categories())))
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),range(0,size*(len(cats)-1)+1,size/(len(cats)-1))))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:]
#             
#     corpus = CorpusReader(
#         "../../corpus/corpus_prensa_uy",
#         "*.csv",
#         "\"(.*?)\",(?:TRUE|FALSE)", # No considera el test.csv
#         ",(.*?)\\n",
#         "FILE",
#         category_position="AFTER"
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = sorted(list(set(corpus.get_categories())))
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),range(0,size*(len(cats)-1)+1,size/(len(cats)-1))))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:]
#    
#     corpus = CorpusReader(
#         "../../corpus/corpus_tweets",
#         "*.tsv",
#         "(.*?)\\t.*?\\n",
#         "(.*?\\t.*?)\\t",
#         "FILE",
#         category_position="BEFORE",
#         start=1
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = list(set(corpus.get_categories()))
#     nums = [tuple(cat.split("\t")) for cat in cats]
#     nums = [int(pos)-int(neg)+5 for (pos,neg) in nums if pos in "1234567890"]
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),map(lambda x:10*x,nums)))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:] 
#    
#     corpus = CorpusReader(
#         "../../corpus/corpus_variado_sfu", 
#         "*/*.txt", 
#         "(.*)\s",
#         "(.*?)_",
#         "PATH",
#         category_level=1
#     )
#     corpus.save_read()
#     print "TOTAL",len(corpus.get_opinions())
#     cats = sorted(list(set(corpus.get_categories())))
#     print "CATEGORIES",cats
#     size = 100
#     fun = dict(zip(sorted(cats),range(0,size*(len(cats)-1)+1,size/(len(cats)-1))))
#     print "FUN",fun
#     data = corpus.get_data(mapping=lambda x:fun[x])
#     print "Ejemplo"
#     print "  id      :",data[0]['id']
#     print "  Category :",data[0]['category']
#     print "  Review   :",data[0]['review'][:30]+" (...) "+data[0]['review'][-30:]
    
    print '\nElapsed time: %.2f Sec' % (time.time() - start_time)
    