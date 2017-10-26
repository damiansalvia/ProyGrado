# -*- encoding: utf-8 -*-
import sys
sys.path.append('../src')

import cldas.db.crud as dp

from cldas.indeplex import *
from cldas.deplex import *
from cldas.utils import USEFUL_TAGS, load


pos = dp.get_opinions( cat_cond={"$gt":50} )
neg = dp.get_opinions( cat_cond={"$lt":50} )
lemmas = dp.get_lemmas()

li = load('./indeplex/indeplex_by_senti_tfidf_top150.json')

opinions = dp.get_opinions( source='corpus_apps_android' )

graph = MultiGraph( opinions, 'corpus_apps_android', filter_tags=USEFUL_TAGS )

ld = by_influence( graph, li, limit=2000)

graph.to_vis(ld,tofile="./visgraph")

