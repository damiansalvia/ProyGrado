# -*- coding: utf-8 -*-

import ui 
import glob, codecs
import csv, json
import xml.etree.ElementTree as xmlreader
magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
            <!ENTITY nbsp ' '>
            ]>''' 

def corpus(cdir,cfmt,revTag,polTag,enc):
	files = glob.glob("%s/*.%s" % (cdir,cfmt))
	total = len(files)
	reviews = []
	for idx,file in enumerate(files):
		ui.progress("Reading corpus",idx,total)
		# try: 
		with open(file) as fp:
			if cfmt == 'xml':
				content = fp.read().decode(enc).encode('utf8')
				root    = xmlreader.fromstring(content)

				print root.tag, root.attrib
				# if polTab in root.attrib:

				# if revTag in root.attrib:

				for child in root:
					print child.tag, child.attrib 
					for grandchild in child:
						print grandchild.tag, grandchild.attrib 
					# reviews.append({
					# 	'review' : xml.get(revTag), #.decode('utf-8') , 
					# 	'rank'   : xml.get(polTag) 
					# })
				# print "\n",root[0], root[1]
				# try:
				# 	revTag = root.get(revTag) 
				# 	polTag = root.get(polTag) 
				# except: pass
				# for elem in root:
				# 	revTag = elem.get(revTag) or elem.find(revTag)
				# 	polTag = elem.get(polTag) or elem.find(polTag) 
					# reviews.append({
					# 	'review' : xml.get(revTag), #.decode('utf-8') , 
					# 	'rank'   : xml.get(polTag) 
					# })
			elif cfmt == 'csv':
				content = csv.reader(fp)
				for row in content:
					reviews.append({
						'review' : row[int(revTag)], #.decode('utf-8') , 
						'rank'   : row[int(polTag)]
					})

			# elif cfmt == 'txt':

			# elif cfmt == 'json': 
		# except Exception as e:
			# log("error con el archivo: " + file + " - " + str(e), 'warning')
	ui.progress("Reading corpus",idx,total)
	name = cdir.split('/')[-1]
	with open("%s/%s.json" % (cdir,name), "w") as output:
		json.dump(reviews, output)
	

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Retrives <review,polarity> from a corpus')
	parser.add_argument('-d','--dir', help='Corpus location directory', required=True)
	parser.add_argument('-f','--fmt', help='Corpus format file', required=True)
	parser.add_argument('-R','--rev-tag', help='Review corpus tag', required=True)
	parser.add_argument('-P','--pol-tag', help='Polarity corpus tag', required=True)
	parser.add_argument('-E','--enc', help='Polarity corpus tag', required=True)
	args = parser.parse_args()
	print args.dir, args.fmt, args.rev_tag, args.pol_tag, args.enc
	corpus(args.dir,args.fmt,args.rev_tag,args.pol_tag,args.enc)