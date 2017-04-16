# -*- coding: utf-8 -*-
from collections import defaultdict

import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d


def print_progress(current,total,bar_length=60):
	percent = float(current) / total
	hashes = '#' * int(round(percent * bar_length))
	spaces = ' ' * (bar_length - len(hashes))
	print "\r[{0}] {1}%".format(hashes + spaces, round(percent * 100,2)),

def get_contexts(corpus,swords,n=5):
	# Obtener texto del corpus
	f = open(corpus,'r')
	text = f.read().encode('utf-8')
	f.close()
	# Obtener contextos de palabras fuente
	words = text.split() # TODO - Mejorar c/pre-procesamiento
	total = len(words)
	contexts = defaultdict(lambda:[])
	for i,word in enumerate (words):
		if word in swords: 
			inf,sup = max(0,i-n),min(i+n+1,total) 
			lhs = ' '.join( words[inf:i  ] )
			rhs = ' '.join( words[i+1:sup] )
			contexts[word].append(' '.join([lhs,word,rhs]))
		# Print progress
		print_progress(i+1,total)
	return contexts

def get_vectors(dim=25):
	filename = './eswiki.0.3.glove.25.50.100.150.200/eswiki.0.3.vectors.%i.txt' % dim
	assert dim in [25,50,100,150,200]
	word2vec = {} 
	for line in open(filename,'r'):
		items = line.replace('\r','').replace('\n','').split(' ')
		if len(items) < 10: continue
		word = items[0].encode('utf-8')
		vect = np.array([float(i) for i in items[1:] if len(i) > 1])
		word2vec[word] = vect
	return word2vec

def draw_words(word2vect, words, pca=False, arrows=True, title=''):
	vectors = [word2vect[word] for word in words]
	
	# Discernir entre PCA o TSE
	if pca:
		pca = PCA(n_components=2, whiten=True)
		vectors2d = pca.fit(vectors).transform(vectors)
	else:
		tsne = TSNE(n_components=2, random_state=0)
		vectors2d = tsne.fit_transform(vectors)
	
	# Dibujar grafico
	plt.figure(figsize=(6,6))
	
	first = True # Alternar colores para dividir grupos
	for point, word in zip(vectors2d , words):
		# Plotear puntos
		plt.scatter(point[0], point[1], c='r' if first else 'g')
		# Plotear palabras
		plt.annotate(
		    word, 
		    xy = (point[0], point[1]),
		    xytext = (-7, -6) if first else (7, -6),
		    textcoords = 'offset points',
		    ha = 'right' if first else 'left',
		    va = 'bottom',
		    size = "x-large"
		)
		first = not first
	
	# Dibujar flechas
	if arrows:
		for i in xrange(0, len(words)-1, 2):
			a = vectors2d[i][0] 
			b = vectors2d[i][1] 
			c = vectors2d[i+1][0] 
			d = vectors2d[i+1][1] 
			plt.arrow(a, b, c-a, d-b,
			    shape='full',
			    lw=0.01,
			    edgecolor='#bbbbbb',
			    facecolor='#bbbbbb',
 			    length_includes_head=True,
			    head_width=0.06,
			    overhang=0.3,
			    width=0.01
			)
	
	# Dibujar titulo
	if title: plt.title(title)
	
	# Dibujar puntos con sus relaciones
	plt.tight_layout()
	plt.show()

def distance(pt_1, pt_2):
	return np.linalg.norm(pt_1-pt_2)

def distPosNeg(word, pos, neg, word2vec):
	tot_pos = sum([distance(word,word2vec[w]) for w in pos])
	tot_neg = sum([distance(word,word2vec[w]) for w in neg])
	return (tot_neg/len(neg) - tot_pos/len(pos)) * -1 # TODO - El "-1"?

def NPosNegLike(n,word2vec,pos,neg):
	orden = sorted(word2vec.keys(), key = lambda (x): distPosNeg(word2vec[x], pos, neg, word2vec))
	return orden[:n], orden[-n:]


if __name__ == '__main__':
	dim = 200
	word2vect = get_vectors(dim=dim)
	print "#Vectores:\n",len(word2vect)
	
	n = 10
	positivas = [
	    "largo",
	    "muchos",
	    "alto",
	    "grueso",
	    "profundo",
	    "pesado",
	    "enorme",
	    "gran",
	    "lindo"
	]	
	negativas = [
	    "poco",
	    "bajo",
	    "fino",
	    "superficial",
	    "liviano",
	    "feo"
	]
	poslike,neglike = NPosNegLike(n, word2vect, positivas, negativas)
	print "Positive-Like:\n",poslike
	print "Negative-Like:\n",neglike
	
# 	WORDS = {
# 		'Currency' : [
# 			"uruguay","pesos",
# 			"alemania","euro",
# 			"japon","yen",
# 			"rusia","rublo",
# 			"eeuu","dolar"
# 		],
# 		'Capital' : [
# 			"atenas","grecia",
# 			"berlin","alemania",
# 			"ankara","turquia",
# 			"estocolmo","suecia",
# 			"hanoi","vietnam",
# 			"lisboa","portugal",
# 			"moscu","rusia",
# 			"tokio","japan",
# 			"washington","eeuu"
# 		],
# 		'Languages' : [
# 			"alemania","aleman",
# 			"eeuu","ingles",
# 			"francia","frances",
# 			"grecia","griego",
# 			"noruega","noruego",
# 			"suecia","sueco",
# 			"polonia","polaco",
# 			"uruguay","latino" # TODO - Problema de condificacion
# 		],
# 		'Opposites' : [
# 			"hombre","mujer",
# 			"rey","reina",
# 			"leon","leona",
# 			"perro","perra"
# 		]
# 	}
# 	option,pca = 'Languages',True
# 	draw_words(
# 		word2vect, 
# 		WORDS[option], 
# 		pca=pca, 
# 		arrows=True, 
# 		title=r'%s - %s - %i dim' % (
# 			option,
# 			'PCA' if pca else 'TSE',
# 			dim
# 		)
# 	)
	
# 	words = ['gran','enorme','largo','muchos','alto']
# 	w = get_contexts('./corpus wikipedia/wikicorpus.es.plain.all.txt',words)
# 	print len(w)
# 	for k,v in w.items():
# 		print k,":",v
	