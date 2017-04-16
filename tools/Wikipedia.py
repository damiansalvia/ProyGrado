# -*- coding: utf-8 -*-

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

#f = open('/eswiki.0.3.glove.25.50.100.150.200/eswiki.0.3.vectors.100.txt','r')
def from_corpus(file):
	word2vec = {} #skip information on first line
	fin= open(file)    
	for line in fin:
		items = line.replace('\r','').replace('\n','').split(' ')
		if len(items) < 10: continue
		word = items[0]
		vect = np.array([float(i) for i in items[1:] if len(i) > 1])
		word2vec[word] = vect
	return word2vec

def get_pca(word2vect,dim):
	pca = PCA(n_components=dim)
	vect = np.array([list(value) for value in word2vect.values()])
	word = np.array([list(value) for value in word2vect.keys()])
	pca = pca.fit_transform(vect)	
	return word, pca

def plot_chart_2d(coords,labels):
	plt.plot(coords[:,0],coords[:,1], 'o', markersize=7, color='blue', alpha=0.5, label='class1')

	plt.xlabel('x_values')
	plt.ylabel('y_values')
	plt.xlim([-4,4])
	plt.ylim([-4,4])
	plt.legend()
	plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')

	plt.show()

def plot_chart_3d(points,labels):
	fig = plt.figure(figsize=(8,8))
	ax = fig.add_subplot(111, projection='3d')
	plt.rcParams['legend.fontsize'] = 10   
	x, y, z = points[:,0], points[:,1], points[:,2]
	ax.plot(x, y, z, 'o',markersize=8, color='blue', alpha=0.5, label=labels)

	plt.title('Samples for pca')
	ax.legend(loc='upper right')

	plt.show()

def plot_chart_3d_motion(points,labels):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection = '3d')

	plotlabels = []
	xs, ys, zs = np.split(points, 3, axis=1)
	sc = ax.scatter(xs,ys,zs)

	for txt, x, y, z in zip(labels, xs, ys, zs):
	    x2, y2, _ = proj3d.proj_transform(x,y,z, ax.get_proj())
	    label = plt.annotate(
	        txt, xy = (x2, y2), xytext = (-20, 20),
	        textcoords = 'offset points', ha = 'right', va = 'bottom',
	        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	        arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=0'))
	    plotlabels.append(label)
	# fig.canvas.mpl_connect('motion_notify_event', lambda event: update_position(event,fig,ax,zip(plotlabels, xs, ys, zs)))
	plt.show()


def update_position(e,fig,ax,labels_and_points):
    for label, x, y, z in labels_and_points:
        x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
        label.xy = x2,y2
        label.update_positions(fig.canvas.renderer)
    fig.canvas.draw()

def draw_words(dictionary, words, pca=False, alternate=True, arrows=True, x1=3, x2=3, y1=3, y2=3, title=''):
    # get vectors for given words from model
    vectors = [dictionary[word] for word in words]

    if pca:
        pca = PCA(n_components=2, whiten=True)
        vectors2d = pca.fit(vectors).transform(vectors)
    else:
        tsne = TSNE(n_components=2, random_state=0)
        vectors2d = tsne.fit_transform(vectors)

    # draw image
    plt.figure(figsize=(6,6))
    if pca:
        plt.axis([x1, x2, y1, y2])

    first = True # color alternation to divide given groups
    for point, word in zip(vectors2d , words):
        # plot points
        plt.scatter(point[0], point[1], c='r' if first else 'g')
        # plot word annotations
        plt.annotate(
            word, 
            xy = (point[0], point[1]),
            xytext = (-7, -6) if first else (7, -6),
            textcoords = 'offset points',
            ha = 'right' if first else 'left',
            va = 'bottom',
            size = "x-large"
        )
        first = not first if alternate else first

    # draw arrows
    if arrows:
        for i in xrange(0, len(words)-1, 2):
            a = vectors2d[i][0] + 0.04
            b = vectors2d[i][1]
            c = vectors2d[i+1][0] - 0.04
            d = vectors2d[i+1][1]
            plt.arrow(a, b, c-a, d-b,
                shape='full',
                lw=0.1,
                edgecolor='#bbbbbb',
                facecolor='#bbbbbb',
                length_includes_head=True,
                head_width=0.08,
                width=0.01
            )

    # draw diagram title
    if title:
        plt.title(title)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
	dictionary = from_corpus('./eswiki.0.3.glove.25.50.100.150.200/eswiki.0.3.vectors.100.txt')
	# l3d,v3d = Wikipedia.get_pca(a,3)
	# assert len(l3d)==len(v3d),"Labels & vectors diffier"
	# Wikipedia.plot_chart_3d(v3d,l3d)
	
	currency = ["uruguay","pesos","alemania","euro","japon","yen","rusia","rublo","eeuu","dolar"]
	capital  = ["atenas","grecia","berlin","alemania","ankara","turquia","estocolmo","suecia","hanoi","vietnam","lisboa","portugal","moscu","rusia","tokio","japan","washington","eeuu"]
	language = ["alemania","aleman","eeuu","ingles","francia","frances","grecia","griego","noruega","noruego","suecia","sueco","polonia","polaco","uruguay","latino"]
	continent = ["alemania","europa","eeuu","america","uruguay","sudamerica","japon","asia","egipto","africa","australia","oceania","noruega","eurasia"]
	opposites = ["hombre","mujer","rey","reina","leon","leona","perro","perra","feo","fea"]

	words = language
	draw_words(dictionary, words, True, True, True, -3, 3, -2, 1.7, r'$PCA\ Visualizando:\ Fruta$')