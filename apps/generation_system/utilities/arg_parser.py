# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(
    prog='Parser',
    description='''Parser.py es un 
    script que se encarga de analizar grandes 
    volumenes de texto de sentimientos (en particular reseñas)
    y recopilar información útil.''',
    epilog='''  ''')

parser.add_argument(
    "-j", "--json",
    action="store",
    help="Importar parametros de archivo JSON"
)

parser.add_argument(
    "-s", "--resumen",
    action="store_true",
    help="Usar la versión resumida del las reseñas"
)

parser.add_argument(
    "-l", "--limite",
    action="store",
    help="Limitar la cantidad de palabras aceptables por reseña",
    type=int
)

parser.add_argument(
    "-rn", "--renombrar",
    action="store_true",
    help="Se reemplazan los nombres de las peliculas por un unico token",
)

parser.add_argument(
    "-t", "--top",
    action="store",
    help="Numero maximo de elementos en estadisticas",
    type=int
)

parser.add_argument(
    "-i", "--input",
    action="store",
    help="Elegir directorio de entrada"
)

parser.add_argument(
    "-o", "--output",
    action="store",
    help="Elegir directorio de salida"
)

parser.add_argument(
    "-lg", "--log",
    action="store",
    help="Elegir directorio para logs"
)

args = parser.parse_args()
