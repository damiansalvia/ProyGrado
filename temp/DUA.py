# -*- coding: utf-8 -*-
import nltk
import codecs
import math
import json
from utils import *
from utilities.arg_DUA import args

inputdir = args.input or 'ProyGrado/apps/outputs/'

def matrix_to_string(dict):
    # To visualize the distribution  matrix
    maxLen = len(max(dict, key=lambda k: len(k)))
    hBar = "-"*(maxLen + 12* 5) + "|\n"
    sDict = hBar 
    sDict += " "*maxLen + "|" + "     1      " + "     2      " + "     3      " + "     4      " + "     5     |\n"
    sDict += hBar

    for word,ranks in dict.items():
        string = word + " "*(maxLen - len(word)) + "|"
        for val in ranks:
            sVal = str(val)
            spaces = 11 - len(sVal) 
            string += " "*math.trunc(spaces/2.0) + sVal + " "*int(math.ceil(spaces/2.0)) + "|"
        sDict += string + '\n'

    sDict += hBar
    return sDict

def polarity(vector):
    # Resolve polarity value of a word through a vector
    # TODO -- Normalizar
    average = sum([x * (idx + 1)
                   for idx, x in enumerate(vector)]) / float(sum(vector))
    if average < 3:
        return '- ' + str(average)
    elif average > 4:
        return '+ ' + str(average)
    else:
        return '0 ' + str(average)

# MAIN
with codecs.open(inputdir + "matrix.json", "r", "utf-8") as f:
    dic = json.load(f)

words = [x.lower() for x in nltk.word_tokenize(args.frase) if is_valid_word(x)]
for word in words:
    if word in dic:
        print polarity(dic[word]) + ' > ' + word
    else:
        print '#               > ' + word
