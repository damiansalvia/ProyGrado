# -*- coding: utf-8 -*-
'''
Module for manage application logging

@author: Nicolás Mecuchlám, Damián Salvia
'''

from time import gmtime, strftime
import inspect, os

class Log:
    
    def __init__(self,logdir,logname="clds.log"):
        logdir = logdir if logdir[-1] != "/" else logdir[:-1]
        if not os.path.isdir(logdir): os.makedirs(logdir)
        self.logpath = logdir+"/"+logname

    def __call__(self,message, level='error'):
        with open(self.logpath, 'a') as log:
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            log.write( "\n%s : %s at %s > %s \n" % ( level.upper() , time , inspect.stack()[1][0].f_code.co_name.upper() , message ) )
