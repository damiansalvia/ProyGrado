# -*- coding: utf-8 -*-
import re
from subprocess import Popen, PIPE

class Aspell(object):
    def __init__(self,text):
        self.corrections = self._parse(text)
    def _parse(self,text,aspell='aspell'):
        p = Popen([aspell,'-a'], stdin=PIPE, stdout=PIPE) # '--personal','../utilities/.aspell.es.pws','--repl','.../utilities/.aspell.es.prepl'
        result = {}
        captured = p.communicate(text.encode('utf8'))[0]
        for line in captured.split('\n'):
            if not line.startswith('&'): 
                continue
            k, v = line.split(':')
            token = re.sub(r'&\s*(\w+).+',r'\1',k)
            word = sorted(
                [word.strip() for word in v.strip().split(',')], 
                key=lambda word:len((set(word)-set([' ']))&set(token)), 
                reverse=True
            )[0]
            result[token] = word        
        return result
    def suggestion(self, word):
        return unicode(self.corrections[word],'utf8')
    def words(self):    
        return self.corrections.keys()

if __name__=='__main__':
    
    while True:
        text = raw_input("> ")
        text = unicode(text)
        
        x = Aspell(text)
        print text
        for word in x.words():
            print word, '->', x.suggestion(word)