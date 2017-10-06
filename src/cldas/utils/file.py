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
    
    if not os.path.isdir(path): os.makedirs(path)
        
    suffix = "" if overwrite else strftime("%Y%m%d_%H-%M-%S", gmtime()) 
            
    path = "%s/%s%s.json" % (path,name,suffix)         
    
    with io.open(path,"w",encoding='utf8') as f:
        content = json.dumps(data,indent=4,ensure_ascii=False)
        if not isinstance(content, unicode):
            content = unicode(content,'utf8')
        f.write(content)
    print "Saved at",path
    