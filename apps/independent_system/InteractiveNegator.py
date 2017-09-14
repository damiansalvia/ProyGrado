# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../utilities')

from analyzer import Analyzer
from CorpusReader import review_correction
an = Analyzer()
import DataProvider as dp
import NegationTagger


def new_model():
    option = raw_input("\nCreate new model or load saved model [ new / load ] > ").replace(' ','')
    while True:
        if option == 'new':
            return True
        elif option == 'load':
            return False
        option = raw_input("\nCreate new model or load data [ new / load ] > ").replace(' ','')


def get_window():
    window_str = raw_input("Indique la ventana del modelo guardado: ").replace(' ','')
    while not window_str.isdigit():
        window_str = raw_input("La ventana debe ser un digito: ").replace(' ','')
    return (int(window_str))

def get_params(window="dual"):
    def process_value(raw_value):
        if raw_value.startswith('[') and raw_value.endswith(']'):
            return [process_value(val) for val in raw_value[1:-1].split(',') ]
        elif raw_value.isdigit():
            return int(raw_value)
        else:
            return raw_value

    os.system('clear')

    if window == 'dual':
        wleft_str = raw_input("\nVentana izquierda: ").replace(' ','')
        while not wleft_str.isdigit():
            wleft_str = raw_input("La ventana debe ser un digito: ").replace(' ','')
        wleft= (int(wleft_str))

        wright_str = raw_input("Ventana Derecha: ").replace(' ','')
        while not wright_str.isdigit():
            wright_str = raw_input("La ventana debe ser un digito: ").replace(' ','')
        wright= (int(wright_str))
    else: 
        wleft_str = raw_input("\nVentana: ").replace(' ','')
        while not wleft_str.isdigit():
            wleft_str = raw_input("La ventana debe ser un digito: ").replace(' ','')
        wleft= (int(wleft_str))

    option = raw_input("\nOpciones ('help' por ayuda) >").replace(' ','')
    config = {}   
    while option:
        if option == 'help':
            print ('''
            Las siguiente opciones son validas:

                out_dims
                activation
                loss
                optimizer
                metrics
                early_monitor
                early_min_delta
                early_patience
                early_mode
                drop_rate

            Se debe escribir con el formato <option> : <value>
            Oprima enter para continuar.''')
        else:
            try:
                key, raw_value = option.split(':') 
                assert key and raw_value
                assert key in ['out_dims', 'activation', 'loss', 'optimizer', 'metrics', 'early_monitor', 
                    'early_min_delta', 'early_patience', 'early_mode']
                value = process_value(raw_value)
                config[key] = value
            except:
                print "invalid Option"
        option = raw_input(">").replace(' ','') 
        os.system('clear')
    if window == 'dual':
        return wleft, wright, config
    else:
        return wleft, config

def start_evaluator(predict_function):
    an = Analyzer()
    raw_input("\nPRESS ENTER TO CONTINUE")
    os.system('clear')
    sentence = raw_input("\nEscriba una frase a analizar o 'exit' para salir > ")
    while sentence != 'exit':
        try:
            sentence = review_correction(sentence)
            analized_sentence = [ item['form'] for item in an.analyze(sentence) ]
            Y = predict_function(analized_sentence)
            print '\nRESULTADO:'        
            print ' '.join(["%s" % ("\033[91m"+wd+"\033[0m" if tg else wd) for wd,tg in \
            zip([text for text in analized_sentence], Y ) ])  
        except:
            print '-- Ocurrio un error --'

        sentence = raw_input("\nEscriba una opinion a analizar o exit para salir > ")

if __name__ == '__main__':

    wleft, wright, config = get_params()
    ANN = NegationTagger.NeuralNegationTagger(wleft,wright,**config)
    ANN.fit_tagged( testing_fraction=0.20 , verbose=1 )
    an = Analyzer()
    raw_input("\nPRESS ENTER TO CONTINUE")
    os.system('clear')
    sentence = raw_input("\nEscriba una frase a analizar o 'exit' para salir > ")
    while sentence != 'exit':
        try:
            result = []
            sentence = review_correction(sentence)
            analized_sentence = an.analyze(sentence)
            analized_sentence = [ {'word': item['form']} for item in analized_sentence ]
            for X in dp.get_text_embeddings( analized_sentence,wleft , wright  )[0]:
                X = X.reshape((1, -1))
                Y = ANN.model.predict( X )
                Y = ( round(Y) == 1 )
                result.append( Y ) 
            print '\nRESULTADO:'        
            print ' '.join(["%s" % ("\033[91m"+wd+"\033[0m" if tg else wd) for wd,tg in \
            zip([text['word'] for text in analized_sentence], result) ])  
        except Exception as e:
            print '-- Ocurrio un error --'

        sentence = raw_input("\n\nEscriba una opinion a analizar o exit para salir > ")
