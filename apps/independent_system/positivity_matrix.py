import DataProvider as db
import numpy as np


SOURCE = 'corpus_apps_android'

output_dir = 'outputs/tmp/'

def get_vectors(text, window_left=2, window_right=2):
    vectors = []
    for idx, word in enumerate(text):
        vec = []
        for i in range(window_left + window_right + 1):
            if window_left != i:
                vec.append(get_entry(text, idx - window_left + i))
            else:
                target = get_entry(text, idx - window_left + i)
        vectors.append((target,vec))
    return vectors  

def get_entry(text, idx):
    if  0 <= idx < len(text) :
        return (text[idx]['lemma'], text[idx].get('negated',False)) 
    else:
        return None

def get_matrices(source):
    vocabulary = [ elem['_id'] for elem in db.get_soruce_vocabulary(SOURCE)]

    vocabulary_size = len(vocabulary)
    pos_matrix = np.zeros((vocabulary_size,vocabulary_size))
    neg_matrix = np.zeros((vocabulary_size,vocabulary_size))
    opinions = db.get_opinions(SOURCE)
    for idx, op in enumerate(opinions):
        cat = op['category']
        vectors = get_vectors(op['text']) 
        for v in vectors:
            target = v[0]
            context = v[1]
            target_cat = 100 - cat if target[1] else cat
            for w in context:
                if w:
                    if target_cat > 50:
                        pos_matrix[vocabulary.index(target[0])][vocabulary.index(w[0])] += target_cat - 50
                    else:
                        neg_matrix[vocabulary.index(target[0])][vocabulary.index(w[0])] += 50 - target_cat



    return pos_matrix, neg_matrix

#=====================================================================================================
if __name__ == "__main__":

    pos_matrix, neg_matrix = get_matrices(SOURCE)
    np.save(output_dir + 'pos_matrix', pos_matrix)
    np.save(output_dir + 'neg_matrix', neg_matrix)

    inner_product = {}
    norm_rest = {}

    for idx in range(vocabulary_size):
        inner_product[idx] = np.inner(pos_matrix, neg_matrix)
        norm_rest[idx] = np.linalg.norm(pos_matrix[idx]) - np.linalg.norm(neg_matrix[idx])

