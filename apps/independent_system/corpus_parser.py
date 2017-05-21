# -*- coding: utf-8 -*-

from corpus_parser_strategies import *
import json, io

#=====================================================================
class ParseCorpus:
	def __init__(self,cdir):
		self.revs = []
		self.dir  = cdir if cdir[-1] != "/" else cdir[:-1]
		self.name = cdir.split("/")[-1]
		self.alg  = globals()[self.name]

	def parse(self):
		self.revs = self.alg(self.dir)
		
	def save(self,dest='outputs/corpus'):
		cdir = "%s/%s.json" % (dest,self.name)
		with io.open(cdir, "w", encoding='utf8') as ofile:
			content = json.dumps(self.revs,indent=4,sort_keys=True,ensure_ascii=False)
			if not isinstance(content, unicode):
				content = unicode(content,'utf8')
			ofile.write(content)
		print "Result was saved in %s\n" % cdir


#=====================================================================
if __name__ == "__main__":
    parser = ParseCorpus("../../corpus/corpus_cine")
    parser.parse()
    parser.save()

    parser = ParseCorpus("../../corpus/corpus_hoteles")
    parser.parse()
    parser.save()

    parser = ParseCorpus("../../corpus/corpus_prensa_uy")
    parser.parse()
    parser.save()

    parser = ParseCorpus("../../corpus/corpus_tweets")
    parser.parse()
    parser.save()

    parser = ParseCorpus("../../corpus/corpus_variado_sfu")
    parser.parse()
    parser.save()

    parser = ParseCorpus("../../corpus/corpus_apps_android")
    parser.parse()
    parser.save()
