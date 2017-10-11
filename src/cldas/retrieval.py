# -*- encoding: utf-8 -*-
'''
Module for reading multiple sources
@author: Nicolás Mechulam, Damián Salvia
'''

class Enum:
    class __metaclass__(type):
        def __contains__(self,item):
            return item in self.__dict__.values()
    
class Position(Enum):
    BEFORE = 1
    AFTER  = 2    


import glob, re
from collections import defaultdict
from utils import progress, Log, save


log = Log("./log")


class CorpusReader(object):
    '''
    Retrieves opinion and category from corporea source files
    '''

    def __init__(self, directory, extension, 
            op_pattern    = None,
            path_pattern  = None,
            path_level    = 0,
            file_pattern  = None,
            file_position = None,
            start_from    = 0,
            decoding      = 'utf8',
            verbose = True,
        ):
        '''
        Constructor from source directory and extension pattern
        '''
        if not op_pattern and not (path_pattern or file_pattern):
            raise ValueError('Expected keyword argument op_pattern with file_pattern or path_pattern.')
        if re.compile(op_pattern).groups > 1:
            raise ValueError("Only one group is admitted for op_pattern argument.")
        if path_pattern and re.compile(path_pattern).groups > 1: 
            raise ValueError("Only one group is admitted for path_pattern argument.")
        if path_pattern and path_level < 0:
            raise ValueError('Expected keyword argument path_level to be positive.')
        if file_pattern and re.compile(file_pattern).groups > 1:
            raise ValueError("Only one group is admitted for file_pattern argument.")
        if file_pattern and (not file_position or file_position not in Position):
            raise ValueError('Expected keyword argument file_position in Position values when file_pattern.')
        if start_from < 0:
            raise ValueError('Expected keyword argument start_from to be positive.')
        
        directory = directory.replace("\\","/")
        extension = '*.'+extension if extension.isalnum() else extension
        
        self._directory   = directory if directory[-1] != "/" else directory[:-1]
        self._files       = glob.glob(directory+'/'+extension)
        self.source = directory.split("/")[-1]
        
        self.filesid = []
        
        self._op_pattern    = op_pattern    # Regex specifying the opinion mapping
        self._path_pattern  = path_pattern  # Regex specifying the category mapping in path
        self._path_level    = path_level    # Number specifying the category level in path
        self._file_pattern  = file_pattern  # Regex specifying the category mapping in file
        self._file_position = file_position # Number specifying the category position in file 
        self._start_from    = start_from    # Number specifying the first line to be read 
        
        self._c2o = defaultdict(list)
        
        self._parse(decoding,verbose)  
        
    
    def _parse(self,decoding,verbose):    
        
        pattern = None
        if self._path_pattern is not None:
            pattern  = self._op_pattern 
        elif self._file_position is Position.AFTER:
            pattern = self._op_pattern+".*?"+self._file_pattern
        elif self._file_position is Position.BEFORE:
            pattern = self._file_pattern+".*?"+self._op_pattern
        
        tmp = pattern.replace("\\#", "") # For checking if DOTALL is required and clean it from pattern
        flag = re.DOTALL if tmp == pattern else 0
        pattern = tmp 
        
        revs = [] ; cats = []
        total = len(self._files)
        for idx,filename in enumerate(self._files):
            filename = filename.replace('\\','/')
            
            if verbose: progress("Parsing %s" % self.__str__(),total,idx)   
            
            if self._path_pattern is not None:
                tmp      = "%s/(?:.*?/){%i}%s" % ( re.escape(self._directory), self._path_level, self._path_pattern )
                regex    = re.compile(tmp,re.DOTALL)
                category = regex.findall(filename)
                    
            regex = re.compile(pattern,flag)
            
            content = open(filename,'r').read().decode(decoding,'replace').encode('utf8')
            content = '\n'.join( [ line for line in content.split('\n') ][ self._start_from: ] )
            found = regex.findall(content)
            
            if not found:
                log("Nothing match in %s" % filename, level="warning")
                continue
            
            qty = len(found)
            
            if self._path_pattern is not None:
                revs,cats = found,category*qty
            elif self._file_position == Position.AFTER:
                revs,cats = zip(*found)
            elif self._file_position == Position.BEFORE:
                cats,revs = zip(*found)
                
            for i in range(qty):
                self._add( revs[i] , cats[i] )
            revs = [] ; cats = []
                
            assert len(revs) == len(cats)             
    
        
    def __repr__(self):
        return "< %s.%s in %s >" % (self.__class__.__module__, self.__class__.__name__, self._directory)
    
    
    def __str__(self):
        return "Retrieval of %s" % self.source 
    
    
    def _add(self,opinion,category):
        self._c2o[ category ].append( opinion )
    
        
    def categories(self):
        return self._c2o.keys()
    
    
    def opinions(self,category=None):
        if category is None:
            return sum( self._c2o.values() , [] )
        else:
            return self._c2o[category]
        
    
    def to_json(self,dirpath='./'):
        save( self._c2o ,"retriv_%s" % self.source , dirpath )        
    

        