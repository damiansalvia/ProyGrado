# -*- coding: utf-8 -*-
'''
Module for manage application logging

@author: Nicolás Mecuchlám, Damián Salvia
'''

from time import gmtime, strftime
import inspect, os
from cldas.utils.misc import EnumItems


class Level(EnumItems):
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    WARN  = "WARN"
    INFO  = "INFO" 
    

class Log:
    
    def __init__(self,logdir,logname="clds.log"):
        logdir = logdir if logdir[-1] != "/" else logdir[:-1]
        if not os.path.isdir(logdir): os.makedirs(logdir)
        self.logpath = logdir+"/"+logname

    def __call__(self,message, level=Level.ERROR):
        with open(self.logpath, 'a') as log:
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            log.write( "\n%s : %s at %s > %s \n" % ( level.upper() , time , inspect.stack()[1][0].f_code.co_name , message ) )
