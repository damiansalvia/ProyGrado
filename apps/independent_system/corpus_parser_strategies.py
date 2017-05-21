# -*- coding: utf-8 -*-

from printHelper import *
import glob
import csv, json
import xml.etree.ElementTree as xmlreader

magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
            <!ENTITY nbsp ' '>
            <!ENTITY lsquo '‘'><!ENTITY rsquo '’'><!ENTITY ldquo '“'><!ENTITY rdquo '”'>
            <!ENTITY ndash '–'><!ENTITY mdash '—'>
            <!ENTITY Prime '´´'><!ENTITY prime '´'>
            <!ENTITY hellip '…'><!ENTITY middot '·'>
            <!ENTITY agrave 'à'><!ENTITY egrave 'è'><!ENTITY igrave 'ì'><!ENTITY ograve 'ò'><!ENTITY ugrave 'ù'>
            <!ENTITY Agrave 'À'><!ENTITY Egrave 'È'><!ENTITY Igrave 'Ì'><!ENTITY Ograve 'Ò'><!ENTITY Ugrave 'Ù'>
            <!ENTITY acute 'á'><!ENTITY ecute 'é'><!ENTITY icute 'í'><!ENTITY ocute 'ó'><!ENTITY ucute 'ú'>
            <!ENTITY Acute 'Á'><!ENTITY Ecute 'É'><!ENTITY Icute 'Í'><!ENTITY Ocute 'Ó'><!ENTITY Ucute 'Ú'>
            <!ENTITY uuml 'ä'><!ENTITY uuml 'ë'><!ENTITY iuml 'ï'><!ENTITY ouml 'ö'><!ENTITY uuml 'ü'>
            <!ENTITY aring 'å'>
            <!ENTITY szlig 'ß'>
            <!ENTITY euro '€'>
            <!ENTITY laquo '«'><!ENTITY raquo '»'>
            <!ENTITY ccedil 'ç'><!ENTITY Ccedil 'Ç'>
            ]>''' 

log = Log('../../apps/log/')

'''
############################### TEMPLATE ###############################
def <nombre_directorio_corpus>(cdir):
	name  = "Corpus: <NOMBRE_CORPUS>, Author: <nombre_autor>"
	val   = {'<cat1>':<val1>,'<cat2>':<val2>,...}
	items = <mechanism to get all items of the corpus in a list>
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:	
			<business logic to get review and polarity from an corpus item>	
			<sometime in the code must appear the following sentence>
			revs.append({
				'review': rev, 
				'rank'  : val[rank] 
			})	
		except Exception as e:
			log(str(e) + "\n" + content)
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs
'''

#=====================================================================

def corpus_cine(cdir):
	name  = "Corpus: MUCHOCINE, Author: Ivan Sainz-Pardo"
	val   = {'1':0,'2':25,'3':50,'4':75,'5':100}
	items = glob.glob(cdir + '/*.xml')
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:	
			with open(item) as fp:
				content = fp.read().decode('cp1252').encode('utf8')
			item = xmlreader.fromstring(magic+content)
			rank = item.attrib['rank']
			for child in item:
				if child.tag == 'body' and child.text is not None:
					rev = child.text
					revs.append({
						'review': rev, 
						'rank'  : val[rank] 
					})	
		except Exception as e:
			log(str(e) + "\n" + str(item))
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs

#=====================================================================

def corpus_hoteles(cdir):
	name  = "Corpus: COAH, Author: Molina Gonzalez"
	val   = {'1':0,'2':25,'3':50,'4':75,'5':100}
	with open(glob.glob(cdir + '/*.xml')[0]) as fp:
		content = fp.read()
	items = xmlreader.fromstring(content)
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:
			for elem in item:
				if elem.tag == '{http://sinai.ujaen.es/coah}rank':
					rank = elem.text
				if elem.tag == '{http://sinai.ujaen.es/coah}review':
					rev = elem.text
					revs.append({
						'review': rev, 
						'rank'  : val[rank] 
					})
		except Exception as e:
			log(str(e) + "\n" + str(item))
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs

#=====================================================================

def corpus_prensa_uy(cdir):
	name  = "Corpus: CORPUS PRENSA, Author: Estudiantes FIng"
	val   = {'NEG':0,'NEU':50,'POS':100}
	with open(cdir + '/train.csv') as csv_file:
		content = list(csv.reader(csv_file))
		columns = {'rev':0,'rank':2}
	items = content
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:
			rev  = item[columns['rev']]
			rank = item[columns['rank']]
			revs.append({
				'review': rev, 
				'rank'  : val[rank.upper()] 
			})	
		except Exception as e:
			log(str(e) + "\n" + str(item))
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs

#=====================================================================

def corpus_tweets(cdir):
	name  = "Corpus: SPANISH TWITTER, Author: David Villares"
	# val   = {'NEG':0,'NEU':50,'POS':100}
	with open(glob.glob(cdir + '/*.tsv')[0]) as tsv_file:
		content = list(csv.DictReader(tsv_file, delimiter='\t'))
	items = content
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:	
			rev  = item['Comment (All)']
			rank = (int(item['mean pos']) - int(item['mean neg']) + 5)*10
			revs.append({
				'review': rev, 
				'rank'  : rank 
			})	
		except Exception as e:
			log(str(e) + "\n" + item['Comment (All)'])
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs

#=====================================================================

def corpus_variado_sfu(cdir):
	name  = "Corpus: SFU VARIADO, Author: J.Brooke, M. Taboada"
	val   = {'NEG':0,'POS':100}
	items = glob.glob(cdir + '/*/*.txt')
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:	
			fname = item.replace('\\','/').split('/')[-1]
			if fname[:2] == 'no':
				rank = 'NEG'
			else:
				rank = 'POS'
			with open(item) as f:
				rev = f.read().decode('latin-1')
			revs.append({
				'review': rev, 
				'rank'  : val[rank] 
			})	
		except Exception as e:
			log(str(e) + "\n" + content)
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs

#=====================================================================

def corpus_apps_android(cdir):
	name  = "Corpus: ANDROIDAPPS-REVIEW-DATASET, Author: ldubiau"
	val   = {'NEG':0,'POS':100}
	paths = glob.glob(cdir + '/*/*.json')
	items = [(rev,path) for path in paths for rev in json.load(open(path))]
	total = len(items)
	revs  = []
	fails = 0
	for idx,item in enumerate(items):
		progressive_bar(name,total,idx)
		try:
			rank  = item[1].replace('\\','/').split('/')[-2].upper()
			rev   = item[0]
			revs.append({
				'review': rev, 
				'rank'  : val[rank] 
			})	
		except Exception as e:
			log(str(e) + "\n" + content)
			fails += 1
			continue
	progressive_bar(name,idx+1,total)
	print "\n%i of %i items have failed" % (fails,total)
	return revs
