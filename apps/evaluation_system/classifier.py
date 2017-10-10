


class Classifier:

    def __init__(self, lexicon):
        self.lexicon = lexicon

    def __call__(self, review):
        sentiment = 0
        for w in review['text']:
            inv = -1 if w['neggated'] else 1
            sentiment += self.lexicon.get(w['lemma'],0) * inv 
        return sentiment

lexicon = {
    'gusta': 5,
    'porqueria': -1,
    'diverido': 4
}

review1 = {'text': [
    {
        'lemma': 'esto',
        'neggated': False
    },
    {
        'lemma': 'no',
        'neggated': False
    },
    {
        'lemma': 'me',
        'neggated': True
    },
    {
        'lemma': 'gusta',
        'neggated': True
    },
    {
        'lemma': '.',
        'neggated': False
    }
]}


review2 = {'text': [
    {
        'lemma': 'esto',
        'neggated': False
    },
    {
        'lemma': 'no',
        'neggated': False
    },
    {
        'lemma': 'me',
        'neggated': True
    },
    {
        'lemma': 'gusta',
        'neggated': True
    },
    {
        'lemma': ',',
        'neggated': False
    }, 
    {
        'lemma': 'es',
        'neggated': False
    },
    {
        'lemma': 'una',
        'neggated': False
    },
    {
        'lemma': 'porqueria',
        'neggated': False
    },
    {
        'lemma': '.',
        'neggated': False
    },
    {
        'lemma': 'al',
        'neggated': False
    },
        {
        'lemma': 'menos',
        'neggated': False
    },
    {
        'lemma': 'es',
        'neggated': False
    },
    {
        'lemma': 'diverido',
        'neggated': False
    },
    {
        'lemma': '.',
        'neggated': False
    }
]}

classifier = Classifier(lexicon)
print 'review1: {}'.format(classifier(review1))
print 'review2: {}'.format(classifier(review2))