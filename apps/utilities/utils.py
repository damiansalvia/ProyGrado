# -*- coding: utf-8 -*-
import re
import codecs
import json

file_pattern = re.compile(r"^<review.*review>$", re.MULTILINE | re.DOTALL)
word_pattern = re.compile(ur'[áéíóúÁÉÍÓÚa-zA-Z]+|\<Film\>$', re.UNICODE)


def is_valid_file(data):
    # return true if the file is valid
    return True if re.match(file_pattern, data) else False


def is_valid_word(word):
    # return true if the word is valid
    try:
        return True if re.match(word_pattern, word) else False
    except:
        return False


def load(json_file):
    with codecs.open(json_file, "r", "utf-8") as f:
        dic = json.load(f)
        return (dic.get('input', None), 
            dic.get('output', None), 
            dic.get('log', None), 
            dic.get('max_acceptable_length', None), 
            dic.get('top', None), 
            dic.get('summarize', None), 
            dic.get('rename', None))
