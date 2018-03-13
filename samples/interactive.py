# -*- encoding: utf-8 -*-
'''
Example of how to use interactive negation by command-line interface
@author: Nicolás Mechulam, Damián Salvia
'''
import sys
sys.path.append('../src')

import os
clean = 'cls' if os.name == 'nt' else 'clear'

from cldas.neg.model import NegScopeLSTM, NegScopeFFN
from cldas.utils.interactive import interactive_prediction, manual_tagging, interactive_correction
import cldas.db.crud as dp
from cldas.utils.file import load
import glob


def interactive_option():
	os.system(clean)
	print "SELECT INTERACTIVE MODE"
	print 0,". Exit"
	print 1,". Interactive text correction"
	print 2,". Manual negation tagging"
	print 3,". Interative negation prediction"
	return raw_input("> ")


def network_option(path='./neg/models'):
	os.system(clean)
	print "SELECT PRETRAINED MODEL"
	files = glob.glob(path+"/*.h5")
	for i,file in enumerate(files):
		print i+1, ".", file.replace(path+"/","")
	while True:
		op = raw_input("> ")
		if op.isdigit() and 1<=int(op)<=len(files): break
	op = int(op)
	file = files[op-1]
	params = load(file.replace(".h5",".json"))
	params.update({'verbose':0})
	return file, params


'''
---------------------------------------------
    Use interactive correction/negation
---------------------------------------------
'''

while True:
	op = interactive_option()
	if op == '0':
		break
	elif op == '1': 
		interactive_correction()
	elif op == '2': 
		manual_tagging(dp,tofile='./neg/manual/')
	elif op == '3':
		os.system(clean)
		file, params = network_option()
		if params.has_key('window_left') and params.has_key('window_right'):
			ann = NegScopeFFN(**params)
			ann.load_model(file)
			formatter = dp.get_ffn_dataset
		elif params.has_key('window'):
			ann = NegScopeLSTM(**params)
			ann.load_model(file)
			formatter = dp.get_lstm_dataset
		else:
			raw_input("Cannot find appropiate parameters.\nContinue...")
			continue
		interactive_prediction( ann , formatter, **params )
	else:
		raw_input('Invalid option. Try again.\nContinue...')


