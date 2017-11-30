# -*- encoding: utf-8 -*-
'''
Module for reading multiple sources
@author: Nicolás Mechulam, Damián Salvia
'''
from cldas.utils.misc import EnumItems  

import glob, re
from collections import defaultdict

from cldas.utils import progress, save
from cldas.utils.logger import Log, Level
from cldas.utils.misc import Iterable


log = Log("./log")


class CorpusReader(object):
    '''
    Class for retrieving opinion and category from corporea source files
    '''

    def __init__(self, directory, filename, 
            op_pattern     = None, 
            wd_pattern     = None,
            path_pattern   = None,
            path_level     = 0,
            file_pattern   = None,
            scope_pattern  = None, 
            negexp_pattern = None, 
            start_from     = 0,
            decoding       = 'utf8',
            verbose = True,
        ):
        '''
        Constructor from source directory and extension pattern
        '''
        if not op_pattern:
            raise ValueError('Expected keyword argument \'op_pattern\'.')
        if not (path_pattern or file_pattern):
            raise ValueError('Expected keyword argument \'file_pattern\' or \'path_pattern\'.')
        if op_pattern and re.compile(op_pattern).groups > 1:
            raise ValueError("Only one group is admitted for \'op_pattern\' argument.")
        if wd_pattern and re.compile(wd_pattern).groups > 1:
            raise ValueError("Only one group is admitted for \'wd_pattern\' argument.")
        if path_pattern and re.compile(path_pattern).groups > 1: 
            raise ValueError("Only one group is admitted for \'path_pattern\' argument.")
        if path_pattern and path_level < 0:
            raise ValueError('Expected keyword argument \'path_level\' to be positive.')
        if file_pattern and re.compile(file_pattern).groups > 1:
            raise ValueError("Only one group is admitted for \'file_pattern\' argument.")
        if start_from < 0:
            raise ValueError('Expected keyword argument \'start_from\' to be positive.')
        
        def get_flags(pattern):
            if pattern is None:
                return None, 0
            tmp = re.sub(r"^/(.*?)/g$","\\1",pattern) # Check if DOTALL is required and clean it from pattern
            flags = re.DOTALL if tmp == pattern else 0
            pattern = tmp
            return pattern, flags 
        
        directory = directory.replace("\\","/")
        directory = directory if directory[-1] != "/" else directory[:-1]
        files = glob.glob(directory+'/'+filename)
        
        if not files:
            raise Exception('There are no files in \'%s\'.' % (directory+'/'+filename))
        
        self._directory   = directory
        self._files       = files
        self.source       = directory.split("/")[-1]
        self._decoding    = decoding
        
        self.filesid = []
        
        op_pattern,   op_flags   = get_flags(op_pattern)
        wd_pattern,   wd_flags   = get_flags(wd_pattern)
        file_pattern, file_flags = get_flags(file_pattern)
        
        self._op_pattern     = op_pattern    # Regex pattern for opinion
        self._op_flags       = op_flags      # Flags applied for opinion pattern
        self._wd_pattern     = wd_pattern    # Regex pattern for words of an opinion
        self._wd_flags       = wd_flags      # Flags applied for words pattern
        self._file_pattern   = file_pattern  # Regex pattern for category in file
        self._file_flags     = file_flags    # Flags applied for file pattern
        self._path_pattern   = path_pattern  # Regex pattern for category in path
        self._path_level     = path_level    # Number for category level in path
        self._scope_pattern  = scope_pattern
        self._negexp_pattern = negexp_pattern 
        self._start_from     = start_from    # Number for specifying the first line to be read 
        
        self._c2o = defaultdict(list)
        
        self._parse(verbose)  
        
    
    def _parse(self,verbose):
        
        revs = [] ; cats = []
        total = len(self._files)
        for idx,filename in enumerate(self._files):
            filename = filename.replace('\\','/')
            
            if verbose: progress("Parsing %s" % self.__str__(),total,idx)   
            
            if self._path_pattern is not None:
                pattern  = "{dir}/(?:.*?/){{{level}}}{cat}".format(dir=re.escape(self._directory), level=self._path_level, cat=self._path_pattern )
                category = re.findall(pattern, filename)
            
            content = open(filename,'r').read().decode(self._decoding,'replace').encode('utf8')
            
            revs = re.findall(self._op_pattern, content, self._op_flags)
            
            if self._scope_pattern is not None: # TODO Please improve me !!
                for idx,rev in enumerate(revs):
                    neg_scope = re.findall(self._scope_pattern, rev, re.DOTALL)
                    toks = [ word for word in re.findall(self._wd_pattern, rev) ]
                    scopes = [] ; negs = []
                    for scope in neg_scope:
                        scope_toks = [ word for word in re.findall(self._wd_pattern, scope) ]
                        scopes.append( scope_toks )
                        if self._negexp_pattern is not None:
                            expr  = re.findall(self._negexp_pattern, scope, re.DOTALL)
                            neg_toks = [ word for e in expr for word in re.findall(self._wd_pattern, e, re.DOTALL) ] 
                            if neg_toks: 
                                negs.append( neg_toks )
                            else: 
                                scopes.pop(-1)
                    bio = [] ; tag = "O"
                    for i in range( len(toks) ):
                        if not scopes: 
                            continue
                        size = len(scopes[0])
                        if toks[i:i+size] == scopes[0][:size]:
                            scopes[0].pop(0)
                            if not scopes[0]: scopes.pop(0)
                            if negs and toks[i] == negs[0][0]:
                                negs[0].pop(0)
                                if not negs[0]: negs.pop(0)
                                tag = "B-NEG"
                            else:
                                tag = "B-INV" if tag in ["O","B-NEG"] else "I-INV"
                        else:
                            tag = "O"
                        for tok in toks[i].split("_"): 
                            bio.append(tok+"/"+tag)
                    revs[idx] = ' '.join( bio )
                            
            elif self._wd_pattern is not None:
                revs = [ re.findall(self._wd_pattern, rev, self._wd_flags) for rev in revs ]
                revs = [ ' '.join([ wd for i,wd in enumerate(words) if wd != words[i-1] ]) for words in revs ]
            
            if self._path_pattern is not None:
                cats = category * len(revs)
            else:
                cats = re.findall(self._file_pattern, content, self._file_flags)
                
            if not revs:
                log("Nothing match in %s" % filename, level=Level.WARN)
            
            if len(revs) != len(cats):
                log("Difference match in %s : %i opinions : %i categories" % (filename,len(revs),len(cats)), level=Level.WARN)
                raise Exception("Difference match in %s : %i opinions : %i categories" % (filename,len(revs),len(cats)))
            
            for i in range( len(revs) )[ self._start_from: ]:
                self._add( revs[i] , cats[i] )
            del revs ; del cats
                            
        
    def __repr__(self):
        return "< %s.%s - %s >" % ( self.__class__.__module__, self.__class__.__name__, self._directory )
    
    
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__,self.source) 
        
    
    def _add(self,opinion,category):
        if not isinstance(opinion,unicode):
            opinion = unicode(opinion,'utf8')
        self._c2o[ category ].append( opinion )
    
    
    def categories(self,pattern=None):
        if not pattern:
            return self._c2o.keys()
        return [ category for category in self._c2o.keys() if re.match(pattern,category) ]
    
    
    def opinions(self,category=None):
        if category is None:
            return sum( self._c2o.values() , [] )
        elif category not in self.categories():
            return []
        return self._c2o[category]
        
    
    def data(self,mapping=None):
        def _gen(mapping):
            pattern = r"(%s)" % '|'.join(mapping.keys()) if mapping else None
            for category in self.categories( pattern=pattern ):
                for text in self.opinions( category=category ):
                    if not text: 
                        continue
                    words, tags = zip ( *re.findall( "(.+?)(?:\/(O|B-NEG|B-INV|I-INV))?(?:\s|$)", text ) )
                    item = { 
                        'text':' '.join( words ), 
                        'category':category if mapping is None else mapping.get(category,None) 
                    }
                    if self._scope_pattern is not None:
                        item.update({ 'tags':tags })
                    yield item
        return Iterable( _gen(mapping) )
    
    
    def to_json(self,dirpath='./'):
        save( self._c2o ,"retriv_%s" % self.source , dirpath )        
        