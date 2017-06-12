# -*- coding: utf-8 -*-

import math
import os
from time import gmtime, strftime
import inspect

tmp = os.popen('stty size', 'r').read().split()
width = int(tmp[1])-15 if tmp else 100

def matrix_to_string(dict):
    # To visualize the distribution  matrix
    max_len = len(max(dict, key=lambda k: len(k)))
    h_bar = "-" * (max_len + 12 * 5) + "|\n"
    dict_s = h_bar
    dict_s += " " * max_len + "|" + "     1      " + "     2      " + \
        "     3      " + "     4      " + "     5     |\n"
    dict_s += h_bar
    coutn_dict = len(dict)
    for idx, (word, ranks) in enumerate(dict.items()):
        string = word + " " * (max_len - len(word)) + "|"
        for val in ranks:
            s_val = str(val)
            spaces = 11 - len(s_val)
            string += " " * \
                math.trunc(spaces / 2.0) + s_val + " " * \
                int(math.ceil(spaces / 2.0)) + "|"
        dict_s += string + '\n'
        progressive_bar("Generating matrix: ", coutn_dict, idx)
    dict_s += h_bar
    return dict_s


def progressive_bar(prompt, total, current, width=width):
    bar_length = width-len(prompt)
    percent = float(current) / total
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    print "\r{0} [{1}] {2}%".format(prompt,hashes + spaces, round(percent * 100,2)),
    if current==total: print

class Log:
    def __init__(self,ldir):
        if not os.path.isdir(ldir): os.makedirs(ldir)
        self.log = open(ldir + "/error_log", 'w')

    def __call__(self,error, level='error'):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.log.write( level.upper() + ':' + time + ' > ' + error + '\n' + 'at:' \
            +  inspect.stack()[1][0].f_code.co_name + '\n' )
