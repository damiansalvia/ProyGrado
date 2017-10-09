# -*- coding: utf-8 -*-

import sys
import time
sys.path.append('../utilities')

from utilities import *
import re, glob, io, json


log = Log("./log")


SUBSTITUTIONS = [
    # Eliminate contractions
    (u"(\w)'(\w)",u"\\1\\2"),
    (u"q'",u"q"),
    # Replace quotes variants by double quotes
    (u"`",u"\""),(u"´",u"\""),(u"\'",u"\""),
    (u"[\u201c\u201d]",u"\""),
    ("\xc2\x93",u"\""),("\xc2\x94",u"\""),
    (u'\u2026',u'...'),   
    # Replace multiple periods by one
    (u"(\.\s*)+",u"."),
    # Replace emojis by a special tag
    (u":\)",u" emoji_feliz "),(u"\(:",u" emoji_feliz "),(u"\sxD\s",u" emoji_feliz "),
    (u":\(",u" emoji_triste "),(u"\):",u" emoji_triste "),
    # Remove URIs with scheme http or https
    (u"(https?:\/\/\S+)",u""),
    # Remove repetitive characters except ll, rr, cc
    (u"([^lr])\\1+",u"\\1"),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"([0-9a-záéíóúñü\\\]?)([^0-9a-záéíóúñü_\\\\s]+)([0-9a-záéíóúñü\\\]?)",u"\\1 \\2 \\3"),
    (u"([^0-9a-záéíóúñü_\s])([^0-9a-záéíóúñü_\s])",u"\\1 \\2"),
    # Separate alphabetical from numerical 
    (u"([a-záéíóúñü])([0-9])",u"\\1 \\2"), 
    (u"([0-9])([a-záéíóúñü])",u"\\1 \\2"),
    # Remove redundant quote marks  -- replace, delete, undo
    (u"(\")([^\"]*?)(?(1)\")",u"&quote;\\2&quote; "),
    (u"[\"]",u""),
    (u"&quote;\s+&quote;",u""),
    (u"&quote;",u"\""),
    # Remove redundant parenthesis -- replace, delete, undo
    (u"(\()([^\(]*?)(?(1)\))",u"&lquo;\\2&rquo;"),
    (u"[\(\)]",u""),
    (u"&lquo;",u"("),(u"&rquo;",u") "), 
    # Replace all non-alphabetical or special symbols by a whitespace
    (u"[^0-9a-záéíóúñü_¿\?¡!\(\),\.:;\"\$/<>]",u" "),
    # Replace multiple non-alphabetical characters by one
#     (u'([¿\?¡!\(\),\.:;\"\$\/<>])(\\1\s*)+',u'\\1 '),
    # Replace multiple blank spaces by one
    (u"(\s){2,}",u" "),
    # Force dot ending
    (u"([^\.])\.\s*$",u"\\1 .")
]

def _correction(text):
    # Encode
    text = text.decode('utf8')
    if not isinstance(text,unicode):
        text = unicode(text,'utf8')
    for source,target in SUBSTITUTIONS:
        text = re.sub(source,target,text,flags=re.DOTALL|re.U|re.I)
#         print source,">>",text
    # Tags treatment (embedded and residual)
    pattern = u"<\s(.*?)\s.*?>(.*?)</\s\\1\s>" 
    while re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern,u"\\2",text,flags=re.DOTALL)
    text = re.sub(u"<.*?>",u"",text,flags=re.DOTALL)
    try:
        diff = text.count(u"(") - text.count(u")")
        while diff <> 0:
            if diff > 0 : 
                text = text[ text.index(u"(") ] ; diff -= 1
            if diff < 0 : 
                text = text[ text.index(u")") ] ; diff += 1
        if text.count(u"\"") % 2 == 1 : 
            text = text[ text.index(u"\"") ]
    except Exception as e:
        print str(e)
        import pdb; pdb.set_trace()
         
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
        tofile=None             # Save result in a tmp file
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
    
    # Normalize source directory
    source = source.replace("\\","/")
    source = source if source[-1] != "/" else source[:-1]
    
    # Create a name for the corpus
    corpus_name = source.split("/")[-1]
    
    # Create the resource file directory for glob reader
    files_dir = source+'/'+extension
    
    # Read the corpus from each file
    filenames = glob.glob(files_dir)
    if not filenames:
        raise Exception('Any corporea found in %s' % files_dir)
    revs , cats  = [] , []
    total = len(filenames)
    for idx, filename in enumerate(filenames):
        progress("Parsing %s" % corpus_name,total,idx)
        
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
        tmp = pattern.replace("\\#", "")
        flag = re.DOTALL if tmp == pattern else 0
        pattern = tmp
        regex = re.compile(pattern,flag)
        
        # Read the file content
        with open(filename,'r') as file:
            content = file.read()
            content = content.decode(decoding,'replace').encode('utf8')
               
        # Find targets
        if category_location == "PATH":
            revs_tmp = regex.findall(content)
            cats_tmp = cats_tmp*len(revs_tmp)
            revs += revs_tmp
            cats += cats_tmp
        elif category_location == "FILE":
            found = regex.findall(content)
            if not found:
                log("Nothing match in %s" % filename, level="warning")
                continue
            if category_position == "BEFORE":
                cats_tmp,revs_tmp = zip(*found)
            elif category_position == "AFTER":
                revs_tmp,cats_tmp = zip(*found)
            revs += list(revs_tmp)
            cats += list(cats_tmp)
            
        assert len(revs_tmp) == len(cats_tmp)
            
    assert len(revs) == len(cats)
    
    # Process the opinions for returning
    opinion_data , total = [] , len(revs)
    for idx in range(total)[start:]:
        progress("Generating %s" % corpus_name,total,idx)
        rev = revs[idx]
        cat = cats[idx]
        if rev:
            opinion_data.append({
                'idx'      : idx+1,
                'source'   : corpus_name,
                'text'     : _correction(rev), 
                'category' : category_mapping[cat] 
            })   
    if tofile: save(opinion_data,"from_%s" % corpus_name,tofile)
    return opinion_data

if __name__ == '__main__':
    while True:
        text = raw_input('> ')
        if not text: break
        result = _correction(text)
        print "INPUT:",text
        print "OUTPUT:",result
#     print _correction(u'Esto :( creo que ) eeees " una prueba! :) Usando ( corrrrrreccion ) de las ( palabras mal')
#     print _correction(u"Can't ad teams Cant ad brazilian soccer teams .")
#     print _correction(u"esta (es otra) prueba (con multiples) parentesis")
#     print _correction(u"tengo (: una aca ( esta es otra ) de  ( prueba :) con ( multiples ) ) parentesis giles")
#     print _correction(u"tengo \" una aca \" esta es otra \" de  \" prueba :\" con \" multiples \" \" parentesis giles")