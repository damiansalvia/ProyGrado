# -*- coding: utf-8 -*-

import time
import nltk
import codecs
import json
import collections

from printHelper import *
from utils import *
from utilities.arg_parser import args

magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
            <!ENTITY nbsp ' '>
            ]>''' 

inputdir = None
outputdir = None
logdir  = None
max_acceptable_length = None
top= None
summarize = None
rename = None
lematize = False

if args.json:
    inputdir, outputdir, logdir , max_acceptable_length, top, summarize, rename = load(
        args.json)

inputdir  = args.input or inputdir or 'apps/dictionaries/'
outputdir = args.output or outputdir or  'apps/outputs/'
logdir    = args.log or logdir or 'apps/log/'

max_acceptable_length = args.limite or max_acceptable_length or 300000
top = args.top or top or 3
summarize = args.resumen or summarize or False
rename = args.renombrar or rename or False


def replace_film_name(text, film):
    # replace every occurrence of the name of the film with a particular token
    # (may not be a good idea)
    return text.replace(film, "<Film>")


def add_word_to_dic(occurrences, word, rank):
    if not occurrences.get(word):
        occurrences[word] = [0, 0, 0, 0, 0]
    occurrences[word][rank - 1] += 1


def is_length_acceptable(text, statistics):
	try:
	    length = len(nltk.word_tokenize(text))
	    statistics['average_review'] += length
	    statistics['largest_review'] = max(statistics['largest_review'], length)
	    statistics['shortest_review'] = min(statistics['shortest_review'], length) if statistics[
	        'shortest_review'] > 0 else length
	    if len(nltk.word_tokenize(text)) < max_acceptable_length:
	        return True
	    return False
	except Exception as e:
		log(str(e))
		return False


def get_tokens(review):
    if lematize:
        return nltk.word_tokenize(review)
    else:
        return nltk.word_tokenize(review)


# Main

log = Log(logdir)
start_time = time.time()
statistics = {
    'corpus_length': 0,
    'largest_review': 0,
    'shortest_review': 0,
    'average_review': 0,
    'top_frecuent_words': [],
    'top_positive': [],
    'top_negative': [],
}

occurrences = {}

with codecs.open(inputdir + "reviews.json", "r", "utf-8") as f:
    reviews = json.load(f)

statistics['corpus_length'] = len(reviews)
for idx, rev in enumerate(reviews):
    subject  = rev['subject']
    review  = rev['review']
    rank  = rev['rank']
    if rename:
        review = replace_film_name(review, subject)
    if is_length_acceptable(review, statistics):
        [add_word_to_dic(occurrences, x.lower(), rank) for
         x in get_tokens(review) if is_valid_word(x)]
    progressive_bar("Reading reviews:    ", statistics['corpus_length'], idx)
sys.stdout.write('\n')
sys.stdout.flush()

dictOccurrences = collections.OrderedDict(sorted(occurrences.items()))

with codecs.open(outputdir + "matrix.txt", "w", "utf-8") as f:
    f.write(matrix_to_string(dictOccurrences))

with codecs.open(outputdir + "matrix.json", "w", "utf-8") as f:
    json.dump(dictOccurrences, f, ensure_ascii=False)


def abs_polarity(vector):
    # Resolve polarity value of a word through a vector
    # TODO -- Normalizar
    average = sum([x * (idx + 1)
                   for idx, x in enumerate(vector)]) / float(sum(vector))
    if average < 2:
        return '- ' + str(average)
    elif average > 3:
        return '+ ' + str(average)
    else:
        return '0 ' + str(average)

polarities = dict([(x, abs_polarity(dictOccurrences[x]))
                   for x in dictOccurrences])

with codecs.open(outputdir + "absolute_polarities.json", "w", "utf-8") as f:
    json.dump(polarities, f, ensure_ascii=False)

# Si se quieren solo las palabras.
#statistics['top_frecuent_words'] = sorted(d, key= lambda x: sum(d[x]))[:2]

statistics['average_review'] /= statistics['corpus_length']

statistics['top_frecuent_words'] = sorted(
    dictOccurrences.items(), key=lambda x: sum(x[1]))[::-1][:top]
polaritySorted = sorted(dictOccurrences.items(), key=lambda v: sum(
    [x * (idx - 1.5) for idx, x in enumerate(v[1])]) / float(sum(v[1])))
statistics['top_positive'] = polaritySorted[::-1][:top]
statistics['top_negative'] = polaritySorted[:top]

with codecs.open(outputdir + "statistics.json", "w", "utf-8") as f:
    json.dump(statistics, f, ensure_ascii=False)


sys.stdout.write('Elapsed time: %.2f Sec' % (time.time() - start_time))
sys.stdout.write('\n')
sys.stdout.flush()
