# -*- coding: utf-8 -*-
'''
Module for managing temporal resources

@author: Nicolás Mechulam, Damián Salvia
'''

from time import gmtime, strftime
import os, io, json



def save(data,name,path,overwrite=True):
    
    if not data:
        print "Nothing to be saved" 
        return    
    
    path = path.replace("\\", "/")
    
    if not os.path.isdir(path): os.makedirs(path)
        
    suffix = "" if overwrite else strftime("%Y%m%d_%H-%M-%S", gmtime()) 
            
    path = "%s/%s%s.json" % (path,name,suffix)         
    
    with io.open(path,"w",encoding='utf8') as fp:
        content = json.dumps(data,indent=4,ensure_ascii=False)
        if not isinstance(content, unicode):
            content = unicode(content,'utf8')
        fp.write(content)
    print "Saved at",path
    
    
    
def load(abspath):
    
    abspath = abspath.replace("\\", "/")
    
    if not abspath or not os.path.exists(abspath) or abspath.split('.')[-1] <> 'json':
        print "Nothing to be load from",abspath
        return 
    
    with io.open(abspath,"r",encoding='utf8') as fp:
        content = json.load(fp,'utf8')
        
    return content
    
    
    