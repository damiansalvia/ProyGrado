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
from _collections import defaultdict
from utils import progress, Log, save


log = Log("./log")


class CorpusReader(object):
    '''
    Retrieves opinion and category from corporea source files
    '''

    def __init__(self, directory, extension, verbose=True, tofile=None, **kwargs):
        '''
        Constructor from source directory and extension pattern
        '''
        directory = directory.replace("\\","/")
        extension = '*.'+extension if extension.isalnum() else extension
        
        self._directory   = directory if directory[-1] != "/" else directory[:-1]
        self._files       = glob.glob(directory+'/'+extension)
        self._source = directory.split("/")[-1]
        
        self.filesid = []
        
        self._op_pattern    = None # Regex specifying the opinion mapping
        self._path_pattern  = None # Regex specifying the category mapping in path
        self._path_level    = 0    # Number specifying the category level in path
        self._file_pattern  = None # Regex specifying the category mapping in file
        self._file_position = None # Number specifying the category position in file 
        self._read_start    = None # Number specifying the first line to be read 
        
        if 'op_content' in kwargs:
            self._op_pattern = kwargs['op_content']
            del kwargs['op_content']
        else:
            raise ValueError('Expected keyword argument op_content.')
        
        if 'cat_path' in kwargs:
            _path_pattern = self._path_pattern = kwargs['cat_path']
            if re.compile(_path_pattern).groups > 1:
                raise ValueError("Only one group is admitted for opinion pattern.")
            self._path_pattern = _path_pattern
            del kwargs['cat_path']
            if 'cat_level' in kwargs:
                _path_level = kwargs['cat_level']
                if _path_level < 0:
                    raise ValueError("Category level must be greater or equal to zero.")
                self._path_level = _path_level
                del kwargs['cat_level']
        elif 'cat_file' in kwargs:
            _file_pattern = kwargs['cat_file']
            if re.compile(_file_pattern).groups > 1:
                raise ValueError("Only one group is admitted for opinion pattern.")
            self._file_pattern = _file_pattern 
            del kwargs['cat_file']
            if 'cat_position' in kwargs:
                position = kwargs['cat_position']
                if position not in Position:
                    raise ValueError('Expected cat_position be BEFORE (1) or AFTER (2).')
                self._file_position = position
                del kwargs['cat_position']
            else:
                raise ValueError('Expected keyword argument cat_position when cat_file.')                
        else:
            raise ValueError('Expected keyword argument cat_path or cat_file.')
        
        if 'start_line' in kwargs:
            self._read_start = kwargs['start_line']
            del kwargs['start_line']
        
        if 'cat_path' in kwargs or 'cat_file' in kwargs:
            raise ValueError('Specify exactly one of: cat_path, cat_file.')
        
        self._c2o = defaultdict(set)
        
        decoding = 'utf8'
        if 'decoding' in kwargs:
            decoding = kwargs['decoding']
            del kwargs['decoding']
        self._parse(decoding,verbose,tofile)  
        
    
    def _parse(self,decoding,verbose,tofile):    
        
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
                tmp      = "%s/(?:.*?/){%i}%s" % ( re.escape(self.directory), self._path_level, self._path_pattern )
                regex    = re.compile(tmp,re.DOTALL)
                category = regex.findall(filename)
                    
            regex = re.compile(pattern,flag)
            
            content = '\n'.join( [line.decode(decoding,'replace').encode('utf8') for line in open(filename,'r').readline()][self._read_start:] )
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
         
        if tofile: save( self._c2o ,"retriv_%s" % self._source , tofile )       
        
    def __repr__(self):
        return "< %s.%s in %s >" % (self.__class__.__module__, self.__class__.__name__, self._directory)
    
    
    def __str__(self):
        return self._source 
    
    
    def _add(self,opinion,category):
        self._c2o[category].add(opinion)
    
        
    def categories(self):
        return self._c2o.keys()
    
    def opinions(self,category=None):
        if category is None:
            return sum( self._c2o.values() , [] )
        else:
            return self._c2o[category]        
    

        