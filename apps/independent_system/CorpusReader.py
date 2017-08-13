# -*- coding: utf-8 -*-

import sys
import time
sys.path.append('../utilities') # To import 'utilities' modules

from printHelper import *
import re, glob, io, json



URL_PATTERN = u"""
    (?:(?:https?|ftp):\/\/)
    (?:\S+(?::\S*)?@)?
    (
        (?!10(?:\.\d{1,3}){3})
        (?!127(?:\.\d{1,3}){3})
        (?!169\.254(?:\.\d{1,3}){2})
        (?!192\.168(?:\.\d{1,3}){2})
        (?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})
        (?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])
        (?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}
        (?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))
    |
        (?:(?:[a-z0-9]+-?)*[a-z0-9]+)
        (?:\.(?:[a-z0-9]+-?)*[a-z0-9]+)*
        (?:\.(?:[a-z]{2,}))
    )
    (?::\d{2,5})?
    (?:\/[^\s]*)?
    """.replace(u"\n", u"").replace(u"\t", u"").replace(u" ", u"")


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
    # Replace every URL by its domain
#     (URL_PATTERN,u"\\1"),
    # Replace every occurrence of repetitive characters except {l,r,c,e} [cabaLLo, coRRer, aCCion, crEE]
    (u"(?i)([abdf-km-qs-z])\\1+",u"\\1"),
    (u"(?i)([lrce])\\1\\1+",u"\\1\\1"),
    (u"(?i)([lrce])\\1(\W)",u"\\1\\2"),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"(?i)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)([^a-záéíóúñüÁÉÍÓÚÑÚ\\\\s]|(?:{.*?}|\[.*?\])]+)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)",u"\\1 \\2 \\3"),
    # Force every review (document) to end with a period
    (u"(.*)[^\.]",u"\\1 ."),
    # Replace all non-alphabetical symbols by a whitespace
    (u"(?i)[^0-9a-záéíóúñüÁÉÍÓÚÑÚ¿\?¡!\(\),\.:;\"\$/]",u" "),
    # Replace multiple blank spaces by one
    (u"(\s){2,}",u" ")
]


def review_correction(
    # Apply simple pattern correction in the input text
        text # Text for applying the correction.
    ):
    for source,target in SUBSTITUTIONS:
        text = re.sub(source,target,text,flags=re.DOTALL)
    return text    

    
def from_corpus(
    # Read any sentiment analysis corpus by matching the review/opinion and its category from each file
        source,                 # Source directory where corpus files are located.
        extension,              # Path pattern to the corpus file ending with its extension (e.g. /*/*/*.xml).
        review_pattern,         # Pattern for matching a review. 
        category_pattern,       # Pattern for matching the category which the review belongs.
        category_mapping,       # Maps ever category value to predefined domain (e.g. 0-100).
        category_location,      # Indicates if the category_pattern applies for a FILE content or its PATH.
        category_position=None, # Indicates if the category_pattern is BEFORE or AFTER review_pattern. Apply for FILE location. 
        category_level=None,    # Indicates where the category_pattern should match in the path pattern (extension). Apply for PATH location.
        start=0,                # Indicates where should start reading the file. Useful for excluding a header in a .csv file (value 1).
        decoding='utf8',        # Format for decoding the corpus file. By default "ut8", but it can be "cp1252", "unicode-escape", etc.
        ldir='./log'            # Directory for the Log file.
    ):
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
    log = Log(ldir)
    
    # Normalize source directory
    source = source.replace("\\","/")
    source = source if source[-1] != "/" else source[:-1]
    
    # Create a name for the corpus
    corpus_name = source.split("/")[-1]
    
    # Create the resource file directory for glob reader
    files_dir = source+'/'+extension
    
    # Read the corpus from each file
    filenames = glob.glob(files_dir)
    revs , cats  = [] , []
    total = len(filenames)
    for idx, filename in enumerate(filenames):
        
        progressive_bar("Parsing %s" % corpus_name,total,idx)
        
        # Generate pattern
        filename = filename.replace('\\','/')
        if category_location == "PATH":
            pattern  = "%s/(?:.*?/){%i}%s" % ( source.replace(".","\."), category_level, category_pattern )
            regex    = re.compile(pattern,re.DOTALL)
            cats_tmp = regex.findall(filename)
            pattern  = "%s" % review_pattern
        elif category_location == "FILE":
            if category_position == "BEFORE":
                pattern = "%s.*?%s" % ( category_pattern , review_pattern )
            elif category_position == "AFTER":
                pattern = "%s.*?%s" % ( review_pattern , category_pattern )
                
        # Compile pattern
        regex = re.compile(pattern,re.DOTALL)
        
        # Read the file content
        with open(filename,'r') as file:
            content = file.read()
            content = content.decode(decoding,'ignore')
            has_tmp = len(content.split('\n'))
               
        # Find targets
        if category_location == "PATH":
            revs_tmp = regex.findall(content)
            cats_tmp = cats_tmp*len(revs_tmp)
            revs += revs_tmp
            cats += cats_tmp
        elif category_location == "FILE":
            found = regex.findall(content)
            if not found:
                print "Noting found in %s" % filename
                continue
            if category_position == "BEFORE":
                cats_tmp,revs_tmp = zip(*found)
            elif category_position == "AFTER":
                revs_tmp,cats_tmp = zip(*found)
            revs += list(revs_tmp)
            cats += list(cats_tmp)
            
        assert len(revs_tmp) == len(cats_tmp)
#         assert len(revs_tmp) == has_tmp 
            
    assert len(revs) == len(cats)
    progressive_bar("Parsing %s   " % corpus_name,total,idx+1)
    
    # Process the opinions for returning
    opinion_data , total = [] , len(revs)
    for idx in range(total)[start:]:
        progressive_bar("Generating %s" % corpus_name,total,idx)
        rev = revs[idx]
        if not isinstance(content, unicode): 
            rev = unicode(rev,'utf8') 
        cat = cats[idx]
        if rev:
            opinion_data.append({
                'idx'      : idx+1,
                'source'   : corpus_name,
                'review'   : review_correction(rev), 
                'category' : category_mapping[cat] 
            })
    progressive_bar("Generating %s" % corpus_name,total,idx+1)    
    return opinion_data



def test(cases):
    if 1 in cases:    
        corus , name = from_corpus(
            "../../corpus/corpus_apps_android",
            "*/*.json",
            "\"(.*?)\"[,(?:\\r\\n)]",
            "(neg|pos)/",
            {
                'neg': 0,
                'pos': 100
            },
            "PATH",
            category_level=0,
            decoding='unicode-escape'
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
    if 2 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_cine",
            "*.xml",
            "<body>(.*?)</body>",
            "rank=\"([1-5])\"",
            {
                '1': 0, 
                '2': 25, 
                '3': 50, 
                '4': 75, 
                '5': 100
            },
            "FILE",
            category_position="BEFORE"
        )   
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]   
    if 3 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_hoteles",
            "*.xml",
            "<coah:review>(.*?)</coah:review>",
            "<coah:rank>([1-5])</coah:rank>",
            {
                '1': 0, 
                '2': 25, 
                '3': 50, 
                '4': 75, 
                '5': 100
            },
            "FILE",
            category_position="BEFORE"
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
    if 4 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_prensa_uy",
            "*.csv",
            "(.*?),(?:TRUE|FALSE)", # No considera el test.csv
            ",(Neg|Neu|Pos)\\n",
            {
                'Neg': 0, 
                'Neu': 50, 
                'Pos': 100
            },
            "FILE",
            category_position="AFTER"
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
    if 5 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_tweets",
            "*.tsv",
            "(.*?)\\t.*?\\n",
            "(.*?\\t.*?)\\t",
            {
                '3\t1': 10, 
                '3\t2': 20, 
                '2\t4': 90, 
                '2\t2': 70, 
                '2\t3': 60, 
                '4\t2': 30,
                '2\t1': 80, 
                '5\t1': 40, 
                '1\t5': 50, 
                '1\t4': 30, 
                '4\t1': 50, 
                '1\t1': 40, 
                '1\t3': 60, 
                '1\t2': 70
            },
            "FILE",
            category_position="BEFORE",
            start=1
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
    if 6 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_variado_sfu", 
            "*/*.txt", 
            "(.*)\s",
            "(yes|no)_",
            {
                'no' : 0, 
                'yes': 100
            },
            "PATH",
            category_level=1
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
    if 7 in cases:
        corus , name = from_corpus(
            "../../corpus/corpus_tweets_2",
            "*.csv",
            "\"(.*?)\",",
            "(N|P|NEU)\\n",#"(.*?)\\n",
            {
                'N'  :0,
                'NEU':50,
                'P'  :100
            },
            "FILE",
            category_position="AFTER",
            start=1
        )
        print "total:",len(corpus)
        print corpus[:2]+corpus[-2:]
   
if __name__ == '__main__':
    cases = raw_input("Enter cases separated by a colon > ")
    cases = [int(case) for case in cases.split(",")]
    test(cases)