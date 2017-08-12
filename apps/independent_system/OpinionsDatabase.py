 # -*- coding: utf-8 -*-

import sys
sys.path.append('../utilities') # To import 'utilities' modules

from pymongo import MongoClient



db = MongoClient().ProyGrado


def get_opinion(id):
    return db.reviews.find_one({'_id':id})


def save_opinions(opinions, corpus):
    for op in opinions:
        op['source'] = corpus
    return db.reviews.insert_many(opinions)


def save_negations():
    return


def get_sample():
    pass


def get_tagged():
    return


def get_untagged():
    return


def save_result():
    return


def get_indepentent_lex():
    return