# -*- coding: utf-8 -*-

import glob
import csv

from printHelper import *
from utils import *

inputdir  =  'corpus/corpus_test/'
outputdir =  'apps/dictionaries/'
logdir    =  'apps/log/'

log = Log(logdir)
files = glob.glob(inputdir + '*.csv')
total = len(files)

reviews = []

def get_normalized_rank(rank):
    if rank == 'Pos':
        return 100
    elif rank == 'Neg':
        return 0
    else:
        return 50


for idx, file in enumerate(files):
    with open(file) as csv_file:
        # try:
        reader = csv.reader(csv_file)
        for row in reader:
            reviews.append({'subject': 'Undefined' , 'review': row[0].decode('utf-8') , 'rank': get_normalized_rank(row[2]) })

        # except Exception as e:
        #     log("error con el archivo: " + file + " " + str(e), 'warning' )
        #     continue

sys.stdout.write('\n')
sys.stdout.flush()

with codecs.open(outputdir + "reviews_prensa.json", "w", "utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False)

print '\nFIN'

