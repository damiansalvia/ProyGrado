# -*- encoding: utf-8 -*-
import sys
sys.path.append('../src')

import cldas.db.crud as dp

from cldas.evaluator import evaluate
from cldas.indeplex import *
from cldas.deplex import *
from cldas.utils import USEFUL_TAGS, load




'''
---------------------------------------------
              Evaluation stage              
---------------------------------------------
'''
# start_time = time.time()

# for dep in dependent_lexicons:
#     testing_corpus = dp.get_opinions(ids=eval_ids, source=dep.get('source'))
#     score = evaluate(dep.get('lexicon'), testing_corpus)
result = {
    'type'   : 'depnedent',
    'li'     :'sentiTFIDF',
    'source' : 'TEST',
    'score'  : {'score1':1, 'score2':2}
}
import pdb; pdb.set_trace()  # breakpoint 2c6825fe //
result_id = dp.save_result(result)

# end_time(start_time)





# pos = dp.get_opinions( cat_cond={"$gt":50} )
# neg = dp.get_opinions( cat_cond={"$lt":50} )
# lemmas = dp.get_lemmas()

# li = load('./indeplex/indeplex_by_senti_tfidf_top150.json')

# opinions = dp.get_opinions( source='corpus_apps_android' )

# graph = MultiGraph( opinions, 'corpus_apps_android', filter_tags=USEFUL_TAGS )

# ld = by_influence( graph, li, limit=2000)

# graph.to_vis(ld,tofile="./visgraph")

