# -*- coding: utf-8 -*-

def config_set_parsing():
    return [
        {
            'source'           :"../../corpus/corpus_apps_android",
            'path_pattern'     :"*/*.json",
            'review_pattern'   :"\"(.*?)\"[,(?:\\r\\n)]",
            'category_pattern' :"(neg|pos)/",
            'category_mapping' :{
                'neg': 20,
                'pos': 80
            },
            'category_location':"PATH",
            'category_position':None,
            'category_level'   :0,
            'start'            :0,
            'decoding'         :'unicode-escape'
        },
        {
            'source'            :"../../corpus/corpus_cine",
            'path_pattern'      :"*.xml",
            'review_pattern'    :"<body>(.*?)</body>",
            'category_pattern'  :"rank=\"([1-5])\"",
            'category_mapping'  :{
                '1': 0, 
                '2': 25, 
                '3': 50, 
                '4': 75, 
                '5': 100
            },
            'category_location' :"FILE",
            'category_position' :"BEFORE",
            'category_level'    :None,
            'start'             :0,
            'decoding'          :'cp1252'
        },
        {
            'source'            :"../../corpus/corpus_hoteles",
            'path_pattern'      :"*.xml",
            'review_pattern'    :"<coah:review>(.*?)</coah:review>",
            'category_pattern'  :"<coah:rank>([1-5])</coah:rank>",
            'category_mapping'  :{
                '1': 0, 
                '2': 25, 
                '3': 50, 
                '4': 75, 
                '5': 100
            },
            'category_location' :"FILE",
            'category_position' :"BEFORE",
            'category_level'    :None,
            'start'             :0,
            'decoding'          :'utf8'
        },
        {
            'source'            :"../../corpus/corpus_prensa_uy",
            'path_pattern'      :"*.csv",
            'review_pattern'    :"\#(.*(?!TRUE|FALSE)),[^ ]", # No considera el test.csv, el "\#" significa "no uses re.DOTALL" 
            'category_pattern'  :",(Neg|Neu|Pos)\\n",
            'category_mapping'  :{
                'Neg': 0, 
                'Neu': 50, 
                'Pos': 100
            },
            'category_location' :"FILE",
            'category_position' :"AFTER",
            'category_level'    :None,
            'start'             :0,
            'decoding'          :'utf8'
        },
        {
            'source'            :"../../corpus/corpus_tweets",
            'path_pattern'      :"*.tsv",
            'review_pattern'    :"(.*?)\\t.*?\\n",
            'category_pattern'  :"(\d\\t\d)\\t",
            'category_mapping'  :{
                '3\t1': 10, 
                '3\t2': 20, 
                '2\t4': 90, 
                '2\t2': 70, 
                '2\t3': 60, 
                '4\t2': 30,
                '2\t1': 80, 
                '5\t1': 40, 
                '1\t5': 50, 
                '1\t4': 30, 
                '4\t1': 50, 
                '1\t1': 40, 
                '1\t3': 60, 
                '1\t2': 70
            },
            'category_location' :"FILE",
            'category_position' :"BEFORE",
            'category_level'    :None,
            'start'             :1,
            'decoding'          :'utf8'
        },
#         {
#             'source'            :"../../corpus/corpus_variado_sfu", 
#             'path_pattern'      :"*/*.txt", 
#             'review_pattern'    :"(.*)\s",
#             'category_pattern'  :"(yes|no)_",
#             'category_mapping'  :{
#                 'no' : 20, 
#                 'yes': 80
#             },
#             'category_location' :"PATH",
#             'category_position' :None,
#             'category_level'    :1,
#             'start'             :0,
#             'decoding'          :'unicode-escape'
#         },
        {
            'source'            :"../../corpus/corpus_tweets_2",
            'path_pattern'      :"*.csv",
            'review_pattern'    :"\"(.*?)\",",
            'category_pattern'  :"(N|P|NEU|NONE)\\n",
            'category_mapping'  :{
                'N'   :0,
                'NEU' :50,
                'NONE':50,
                'P'   :100
            },
            'category_location' :"FILE",
            'category_position' :"AFTER",
            'category_level'    :None,
            'start'             :1,
            'decoding'          :'utf8'
        },
        {
            'source'            :"../../corpus/corpus_restaurantes",
            'path_pattern'      :"*/*.json",
            'review_pattern'    :"\"(.*?)\"[,(?:\\r\\n)]",
            'category_pattern'  :"(neg|pos)/",
            'category_mapping'  :{
                'neg': 20,
                'pos': 80
            }, 
            'category_location' :"PATH",
            'category_position' :None,
            'category_level'    :0,
            'start': 0,
            'decoding'          :'unicode-escape'
        }
] 
    
def config_set_neural_negation_tagger():
    # Activations: relu [max(0,x)], linear [x], tanh, softplus [ln(1+exp(x)], selu [x:x>0;aexp(x)-a:x<=0], sigmoid [1/(1+exp(-x))]
    # Optimizers:  adam, sgd, rmsprop
    # Monitors: None, val_binary_accuracy o val_precision
    return [
#         {
#             'wleft'         :3,
#             'wright'        :3,
#             'out_dims'      :[1200],
#             'activation'    :['relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :2,
#             'out_dims'      :[1200],
#             'activation'    :['relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :3,
#             'out_dims'      :[1300],
#             'activation'    :['relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2]
#         },
#         {
#             'wleft'         :2,
#             'wright'        :2,
#             'out_dims'      :[750,500],
#             'activation'    :['relu','relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :3,
#             'wright'        :3,
#             'out_dims'      :[1200,700],
#             'activation'    :['relu','relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :2,
#             'out_dims'      :[1200,700],
#             'activation'    :['relu','relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :3,
#             'out_dims'      :[1300,800],
#             'activation'    :['relu','relu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :2,
#             'wright'        :2,
#             'out_dims'      :[750,500],
#             'activation'    :['selu','selu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :3,
#             'wright'        :3,
#             'out_dims'      :[1200,700],
#             'activation'    :['selu','selu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :4,
#             'out_dims'      :[1500],
#             'activation'    :['selu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2]
#         },
#         {
#             'wleft'         :4,
#             'wright'        :4,
#             'out_dims'      :[1500,800],
#             'activation'    :['selu','selu','sigmoid'],
#             'loss'          :'binary_crossentropy',
#             'optimizer'     :'adam',
#             'early_monitor' :'val_binary_accuracy',
#             'drop_rate'     :[0.2,0.2]
#         },
    ]