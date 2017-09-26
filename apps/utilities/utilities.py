# -*- coding: utf-8 -*-

from time import gmtime, strftime
import inspect, math, json, os, io


tmp = os.popen('stty size', 'r').read().split()
width = int(tmp[1])-15 if tmp else 100


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


def progress(prompt, total, current, width=width, end=True):
    current += 1
    size_status = 2*len(str(total))+3 
    bar_length = width-len(prompt)-size_status
    percent = float(current) / total
    hashes = '=' * int(round(percent * bar_length))
    spaces = '.' * ( bar_length - len(hashes) - 1 )
    status = "(%i/%i)" % (current,total)
    print "\r{0} {1} [{2}] {3}%".format(status,prompt, hashes + '>' + spaces,round(percent * 100,2)),
    if current==total and end: print


def title(title,width=width):
    size = width - len(title) + 2
    size = size / 2 
    print "*"*size,title.upper(),"*"*size
        

class Log:
    
    def __init__(self,ldir,lname="log_general"):
        ldir = ldir if ldir[-1] != "/" else ldir[:-1]
        if not os.path.isdir(ldir): os.makedirs(ldir)
        self.log = open(ldir+"/"+lname, 'a')

    def __call__(self,message, level='error'):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.log.write( "\n%s : %s at %s > %s \n" % ( level.upper() , time , inspect.stack()[1][0].f_code.co_name.upper() , message ) )
        
    def __exit__(self):
        self.log.close()
