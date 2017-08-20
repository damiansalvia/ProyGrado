# -*- coding: utf-8 -*-

import sys
import time
sys.path.append('../utilities')

from utilities import *
import re, glob, io, json



SUBSTITUTIONS = [
    # Replace non-spanish characters by the hipotetical correct character
    (u"à",u"á"), (u"è",u"é"), (u"ì",u"í"), (u"ò",u"ó"), (u"ù",u"ú"),
    (u"â",u"á"), (u"ê",u"é"), (u"î",u"í"), (u"ô",u"ó"), (u"û",u"ú"),
    (u"À",u"Á"), (u"È",u"É"), (u"Ì",u"Í"), (u"Ò",u"Ó"), (u"ù",u"Ú"),
    (u"ä",u"á"), (u"ë",u"é"), (u"ï",u"í"), (u"ö",u"ó"),
    (u"Ä",u"A"), (u"Ë",u"E"), (u"Ï",u"I"), (u"Ö",u"O"),
    (u"å",u"a"), (u"ç",u"c"),
    # Replace other non-spanish characters
    (u"`",u"\""),(u"´",u"\""),
    (u"\'",u"\""),
    # Replace every occurrence of repetitive characters except {l,r,c,e} [cabaLLo, coRRer, aCCion, crEE]
    (u"(?i)([^lrce])\\1+",u"\\1"),
    (u"(?i)([lrce])\\1\\1+",u"\\1\\1"),
    (u"(?i)([lrce])\\1(\W)",u"\\1\\2"),
    # Separate alphabetical character from non-alphabetical character by a blank space
    (u"(?i)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)([^a-záéíóúñüÁÉÍÓÚÑÚ\\\\s]|(?:{.*?}|\[.*?\])]+)([a-záéíóúñüÁÉÍÓÚÑÚ\\\]?)",u"\\1 \\2 \\3"),
    # Replace all non-alphabetical symbols by a whitespace
    (u"(?i)[^0-9a-záéíóúñüÁÉÍÓÚÑÚ¿\?¡!\(\),\.:;\"\$/]",u" "),
    # Replace multiple blank spaces by one
    (u"(\s){2,}",u" "),
    # Replace multiple periods by one
    (u"(\.\s*)+",u".")
]


def review_correction(
    # Apply simple pattern correction in the input text
        text # Text for applying the correction.
    ):
    if not isinstance(text,unicode):
        text = unicode(text,'utf8')
    text += u" ."
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
                print "\rNothing found in",filename
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
                'text'     : review_correction(rev), 
                'category' : category_mapping[cat] 
            })   
    return opinion_data
