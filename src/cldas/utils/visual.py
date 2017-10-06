# -*- coding: utf-8 -*-
'''
Module for command-line visualization

@author: Nicolás Mechulam, Damian Salvia
'''

import os


tmp = os.popen('stty size', 'r').read().split()
width = int(tmp[1])-15 if tmp else 100


def progress(prompt, total, current, width=width, end=True):
    current += 1
    size_status = 2*len( str(total) ) + 3 
    bar_length = width-len(prompt)-size_status
    percent = float(current) / total
    hashes = '=' * int( round(percent * bar_length) )
    spaces = '.' * ( bar_length - len(hashes) - 1 )
    status = "(%i/%i)" % ( current , total )
    print "\r{0} {1} [{2}] {3}%".format( status , prompt , hashes + '>' + spaces , round(percent * 100,2) ),
    if current==total and end: print


def title(title,width=width):
    size = width - len(title) + 2
    size = size / 2 
    print "*"*size,title.upper(),"*"*size
