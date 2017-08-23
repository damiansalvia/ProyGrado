# -*- coding: utf-8 -*-

from time import gmtime, strftime 
import inspect, math, json, os, io


tmp = os.popen('stty size', 'r').read().split()
width = int(tmp[1])-15 if tmp else 100


def save(data,name,path):    
    # Check output directory and concatenate the filename
    if not os.path.isdir(path): 
        os.makedirs(path)
    path = "%s/%s.json" % (path,name)
    
    # Save it into a the file
    with io.open(path,"w",encoding='utf8') as f:
        content = json.dumps(data,indent=4,ensure_ascii=False)
        if not isinstance(content, unicode):
            content = unicode(content,'utf8')
        f.write(content)
    print "Saved at",path


def progress(prompt, total, current, width=width):
    current += 1
    bar_length = width-len(prompt)
    percent = float(current) / total
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    print "\r{0} [{1}] {2}%".format(prompt, hashes + spaces, round(percent * 100,2)),
    if current==total: print


class FileLog:

    def __init__(self, fname, mode='w'):
        self.__write_queue = []
        self.__f = open(fname, mode)

    def write(self, s):
        self.__write_queue.insert(0, s)

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.__write_queue: 
            self.__f.writelines(self.__write_queue)
        self.__f.close()
        

class Log:
    
    def __init__(self,ldir,lname="log_general"):
        if not os.path.isdir(ldir): os.makedirs(ldir)
        self.log = FileLog(ldir+"/"+lname, 'wa')

    def __call__(self,message, level='error'):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.log.write( "%s : %s at %s > %s \n" % ( level.upper() , time , inspect.stack()[1][0].f_code.co_name.upper() , message ) )
        
    def __exit__(self):
        self.log.close()
