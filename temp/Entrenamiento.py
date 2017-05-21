# -*- coding: utf-8 -*-
'''
Construcción de léxicos dinámicos para análisis de sentimiento
Facultad de Ingenieria, UdelaR, 2016

Proyecto de Grado

@author: Salvia, Damian
@author: Mechulam, Nicolas
'''

import os
import gensim
import logging
import glove
import re
from string import punctuation


def print_progress(current,total,bar_length=60):
    percent = float(current) / total
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    print "\r[{0}] {1}%".format(hashes + spaces, round(percent * 100,2)),


def pre_process(textline):
    textline = re.sub('<add>(.*?)</add>', u"\g<1>", textline)
    textline = re.sub('<doc>(.*?)</doc>', u"\g<1>", textline)
    textline = re.sub('<field name=\"articulo\">(.*?)</field>', u"\g<1>", textline) # Obtener texto
    textline = re.sub('<field .*?>.*?</field>', "", textline) # El resto no me importa 
    textline = re.sub('[{}]'.format(punctuation), "", textline)
    textline = re.sub('\n|\r', "", textline)
    textline = re.sub('\s+',' ',textline)
    textline = re.sub('<add>|<doc>|</doc>|</add>', "", textline)
    textline = textline.lower()
    return textline


class Corpus(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                line = pre_process(line)
                if line: 
                    yield line.split()
   
                
class Modelo(object):
    model = None
    
    def __init__(self, sentences, w2v=True):
        self.is_w2v     = w2v
        self.sentences = sentences
    
    def load(self,filepath):
        try: # Intenta cargar el archivo pickles
            with open(filepath, 'rb') as loadfile:
                self.model.load(loadfile)
        except:
            print "No se pudo cargar",filepath
    
    def fit(self, save_as=None, size=100, windows=5, threads=5, lrate=0.05, log=True):
        if self.is_w2v:
            if log: logging.basicConfig(
                format='%(asctime)s : %(levelname)s : %(message)s',  
                level=logging.INFO
            )
            self.model = gensim.models.Word2Vec(
                self.sentences,
                size=size,
                window=windows,
                alpha=lrate,
                workers=threads,
                min_count=None, # No ignorar palabras
                sg=1,
                hs=1,
                negative=0,
                cbow_mean=0
            )
        else:
            corpus = glove.Corpus()
            corpus.fit(
                self.sentences, 
                window=windows
            )
            self.model = glove.Glove(
                no_components=size, 
                learning_rate=lrate
            )
            self.model.fit(
                corpus.matrix, 
                epochs=5, 
                no_threads=threads, 
                verbose=log
            )
            self.model.add_dictionary(
                corpus.dictionary
            )
        if save_as:
            self.model.save(save_as)
    
    def most_similar(self,word,top=10):
        if self.is_w2v:
            return self.model.most_similar(positive=[word],topn=top)
        else:
            return self.model.most_similar(word,number=top)
        
    def save(self,filepath):
        bow = set(word for sentence in self.sentences for word in sentence)
        total = len(bow)
        with open(filepath,'w') as savefile:
            for i,word in enumerate(bow):
                vector = (' '.join(['%7.6f']*self[word].size)) % tuple(self[word])
                savefile.write(' '.join([word,vector,'\n']))
                print_progress(i,total)
    
    def __getitem__(self,word):
        if type(word) is not str: 
            raise "Indice debe ser palabra"
        if self.is_w2v:
            return self.model[word]
        else:
            idx = self.model.dictionary[word]
            return self.model.word_vectors[idx]
               


# Demo
if __name__ == '__main__':
    corpus = Corpus('./corpus prensa 2015/')
#     corpus = Corpus('./test/')
    
    size = 100
    
    print "\nUsing GloVe"
    filename = "CLDAS.GloVe.%i" % size
    model = Modelo(corpus,w2v=False)
#     model.fit()
    model.fit(save_as=filename+".model",size=size)
    print model['el']
    model.save(filename+'.txt')
    
    print "\nUsing Word2Vect"
    filename = "CLDAS.Word2Vec.%i" % size
    model = Modelo(corpus,w2v=True)
#     model.fit()
    model.fit(save_as=filename+".model",size=size)
    print model['el']
    model.save(filename+'.txt')
    
    
#     model.fit(save_as='test')
# #     model.load('prensa.pickles')
#     
#     print model.most_similar('mujer')    