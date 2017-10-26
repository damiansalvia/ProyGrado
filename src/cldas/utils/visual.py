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
    total_size = len( str(total) )
    size_status = 2*total_size + 3 
    bar_length = width-len(prompt)-size_status
    percent = float(current) / total
    hashes = '=' * int( round(percent * bar_length) )
    spaces = '.' * ( bar_length - len(hashes) - 1 )
    status = "(%*i/%i)" % ( total_size, current , total )
    print "\r{0} {1} [{2}] {3:{4}}%".format( status , prompt , hashes + '>' + spaces , round(percent * 100,2), 5 ),
    if current==total and end: print


def title(title,width=width):
    size = width - len(title) + 2
    size = size / 2 ; rest = size % 2 
    print "*"*size,title.upper(),"*"*(size+rest)

class RGBGradiant:
    def __init__(self, max_positive, max_negative, rgb_pos, rgb_neg, rgb_neu):
        self.positive_dif = (
            (rgb_pos[0] - rgb_neu[0]) / (max_positive * 1.0), 
            (rgb_pos[1] - rgb_neu[1]) / (max_positive * 1.0), 
            (rgb_pos[2] - rgb_neu[2]) / (max_positive * 1.0)
        )
        self.negative_dif = (
            (rgb_neu[0] - rgb_neg[0]) / (max_negative * 1.0), 
            (rgb_neu[1] - rgb_neg[1]) / (max_negative * 1.0), 
            (rgb_neu[2] - rgb_neg[2]) / (max_negative * 1.0)
        )
        self.max_positive = max_positive
        self.max_negative = max_negative

        self.rgb_pos = rgb_pos
        self.rgb_neu = rgb_neu
        self.rgb_neg = rgb_neg

    def __call__(self, value):
        if value > 0:
            if value > self.max_positive:
                return self.rgb_pos
            return ( 
                round(self.rgb_neu[0] + value * self.positive_dif[0]), 
                round(self.rgb_neu[1] + value * self.positive_dif[1]), 
                round(self.rgb_neu[2] + value * self.positive_dif[2]) 
            )
        else: 
            if value < self.max_negative:
                return self.rgb_neg
            return ( 
                round(self.rgb_neu[0] - value * self.negative_dif[0]), 
                round(self.rgb_neu[1] - value * self.negative_dif[1]), 
                round(self.rgb_neu[2] - value * self.negative_dif[2]) 
            )