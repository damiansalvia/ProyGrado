# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('../utilities')

from analyzer import Analyzer
from CorpusReader import review_correction

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
            try:
                return float(raw_value)
            except ValueError:
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

    config = {}   
    option = raw_input("Hiperparametros ('help' por ayuda) >").replace(' ','')
    while option:
        if option == 'help':
            print ('''
    Los siguientes hiperparametros son validao:

        metrics
        loss
        optimizer
        early_monitor
        early_min_delta
        early_patience
        early_mode

    Se debe escribir con el formato <hiperparametro> : <valor>
    Oprima 'Enter' para continuar.''')
        else:
            try:
                key, raw_value = option.split(':') 
                assert key and raw_value
                assert key in ['loss', 'optimizer', 'metrics', 'early_monitor', 
                    'early_min_delta', 'early_patience', 'early_mode']
                value = process_value(raw_value)
                config[key] = value
            except:
                print "invalid Option"
        option = raw_input(">").replace(' ','') 
    os.system('clear')
    print 
    new_layer = True
    layers = []
    layer_number = 1
    while new_layer:
        layer = {}
        print 'Capa oculta #' + str(layer_number)
        layer_number += 1
        option = raw_input("Parametros capa oculta ('help' por ayuda) > ").replace(' ','')
        while option:
            if option == 'help':
                print ('''
    Los siguientes parametros son validos:

        units              : <Int>, 
        activation         : <String>,
        dropout            : <Double>,
        bias               : <Boolean>,
        recurrent_dropout  : <Double>

    Se debe escribir con el formato <parametro> : <valor>
    Oprima 'Enter' para continuar.''')
            else:
                try:
                    key, raw_value = option.split(':') 
                    assert key and raw_value
                    assert key in ['units', 'activation', 'dropout', 'bias', 'recurrent_dropout']
                    value = process_value(raw_value)
                    layer[key] = value
                except:
                    print "invalid Option"
            option = raw_input(">").replace(' ','') 
        layers.append(layer)
        new_layer = raw_input('Desea agregar una nueva capa? [ Y / n ] > ').replace(' ','') in ['y','Y']
    config['hidden_leyers'] = layers
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

