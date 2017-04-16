# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser(
     prog='DUA',
     description='''DUA.py es un 
     script que se basa en el resultado de el script 
     hermano "Parser.py" para identificar la polaridad 
     de cada una de las palabras de una frase dada 
     teniendo en cuenta su contexto.''',
     epilog='''  ''')

parser.add_argument(
    "frase",
    help="Frase a analizar"
)

parser.add_argument(
    "-i", "--input",
    action="store",
    help="Elegir directorio de entrada"
)

args = parser.parse_args()
