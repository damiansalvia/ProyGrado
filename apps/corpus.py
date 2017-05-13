# -*- coding: utf-8 -*-

import ui 
import glob
import csv

def corpus(cdir,cfmt,revTag,polTag):
	files = glob.glob(cdir + '*.'+cfmt)
	total = len(files)
	for idx,file in enumerate(files):
		ui.progress("Reading corpus",total,idx)
		with open(file) as file:
			print str(file)
	name = cdir.split('/')[-2]

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Description of your program')
	parser.add_argument('-d','--dir', help='Corpus location directory', required=True)
	parser.add_argument('-f','--fmt', help='Corpus format file', required=True)
	parser.add_argument('-R','--rev-tag', help='Review corpus tag', required=True)
	parser.add_argument('-P','--pol-tag', help='Polarity corpus tag', required=True)
	args = parser.parse_args()
	print args