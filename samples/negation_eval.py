# -*- encoding: utf-8 -*-
import sys
sys.path.append('../src')

import cldas.db.crud as dp
from cldas.neg.model import NegScopeLSTM, NegScopeFFN
from cldas.utils.metrics import *
from cldas.utils.misc import Iterable
import time
import itertools
from cldas.utils.logger import Log, Level


log = Log('./log')

tagged = dp.get_tagged(dp.TaggedType.MANUAL)


def eval_negation( fixed, arguments={}, params_lstm=None, params_ffn=None, iter=''):
    path = './neg/models'

    def end_time(start_time):
        return time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))

    ######## Feed-Forward Neural Network #########  
    ## FFN

    if params_ffn and (not arguments or arguments.get('ffn') != None):
        keys_ffn = params_ffn.keys()
        idx = 0
        for par in itertools.product(*params_ffn.values()):
            dict_par = dict(zip(keys_ffn,par))
            if idx < arguments.get('ffn', 0):
                continue
            # try:
            start_time = time.time()
            
            name = "Neg_FFN_%d" % int(start_time) 
            ffn = NegScopeFFN( ** dict(zip(keys_ffn,par) + fixed.items()))
            # X_train, Y_train = dp.get_ffn_dataset( tagged, dict_par['window_left'], dict_par['window_right'] )
            # ffn.fit( X_train, Y_train )
            gen_train, gen_test = dp.get_ffn_dataset2( tagged, dict_par['window_left'], dict_par['window_right'] )
            ffn.fit2( gen_train, gen_XY_test=gen_test )

            elapsed = end_time(start_time)

            # score = ffn.get_scores( X_train, Y_train )
            score = ffn.get_scores2( gen_train )
            dp.save_evaluation([dict({
                'type'          : 'negation',
                'ANN'           : 'FFN',
                'name'          : name,
                'score'         : dict(score),
                'training_time' : elapsed,
                'params'        : dict_par
            })])  

            ffn.save_model(name, path)

            log( "Step fnn %d finished." % idx, level=Level.INFO)
            # except Exception as e:
            #     error = "Error while processing: %s \n Error : %s" % (str(dict_par), str(e))
            #     print error
            #     log( error , level=Level.ERROR)
            #     time.sleep(2) 
            idx += 1

    ## LSTM
    if params_lstm and (not arguments or arguments.get('lstm') != None):
        keys_lstm = params_lstm.keys()
        idx = 0
        for par in itertools.product(*params_lstm.values()):
            if idx < arguments.get('lstm', 0):
                continue
            try:
                start_time = time.time()

                name = "Neg_LSTM_%d" % int(start_time) 
                lstm = NegScopeLSTM( ** dict(zip(keys_lstm,par) + fixed.items()))
                # X_train, Y_train = dp.get_lstm_dataset( tagged, dict(zip(keys_lstm,par))['window'] )
                # lstm.fit( X_train, Y_train )
                gen_train, gen_test = dp.get_lstm_dataset2( tagged, dict(zip(keys_lstm,par))['window'] )
                lstm.fit2( gen_train, gen_XY_test=gen_test )

                elapsed = end_time(start_time)

                # score = lstm.get_scores( X_train, Y_train)
                score = lstm.get_scores2( gen_train )
                dp.save_evaluation([dict({
                    'type'          : 'negation',
                    'ANN'           : 'LSTM',
                    'name'          : name,
                    'score'         : dict(score),
                    'training_time' : elapsed,
                    'params'        : dict(zip(keys_lstm,par))
                })])  

                lstm.save_model(name, path)
                
                log( "Step lstm %d - %s finished." % (idx,iter), level=Level.INFO)
            except Exception as e:
                error = "Error while processing: %s \n Error : %s" % (str(dict(zip(keys_lstm,par))), str(e))
                print error
                log( error , level=Level.ERROR)
                time.sleep(2) 
            idx += 1

        return 'ok'




if __name__== '__main__':

    len_arg = len(sys.argv)
    arguments = {}
    if len_arg not in [1,3,5,6]:
        raise 'Invalid arguments'
    if len_arg >= 3:
        if sys.argv[1] not in ['lstm', 'fnn'] or not sys.argv[2].isdigit():
            raise 'Invalid arguments'
        arguments[sys.argv[1]] = int(sys.argv[2])
    if len_arg >= 5:
        if sys.argv[3] not in ['lstm', 'fnn'] or not sys.argv[4].isdigit():
            raise 'Invalid arguments'
        arguments[sys.argv[3]] = int(sys.argv[4])

    start_at = '---'


    prompt =  '\nStart From: \n'
    prompt += '(Empty for start at beggining)\n\n'
    prompt += '1 : Window\n'
    prompt += '2 : Optimizer \n'
    prompt += '3 : Loss \n'
    prompt += '4 : Layers \n'
    # prompt += '5 : All \n'
    prompt += '\n> '
    

    while (start_at and not start_at.isdigit()):
        start_at = raw_input(prompt)

    if start_at.isdigit():
        start_at = int(start_at)
    else:
        start_at = 0


    fixed = {
        'dimension':len(dp.get_null_embedding()),
        'verbose'  :0,
        'metrics'  :[binacc, precision, recall, fmeasure, mse, bce],
    }


    params_lstm = {
        'window'    :[5,10,15,20],
        'loss'      :['binary_crossentropy'],
        'optimizer' :[ 'adam'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    params_ffn = {
        'window_left'  : [1,5,10],
        'window_right' : [1,5,10],
        'loss'         : ['binary_crossentropy'], 
        'optimizer'    : ['adam'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    if start_at <= 1:
        print eval_negation( fixed, arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='window')


    params_lstm = {
        'window'    :[10],
        'loss'      :['binary_crossentropy'],
        'optimizer' :[ 'Nadam', 'RMSprop'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    params_ffn = {
        'window_left'  : [6],
        'window_right' : [6],
        'loss'         : ['binary_crossentropy'], 
        'optimizer'    : ['Adamax', 'SGD'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    if start_at <= 2:
        print eval_negation( fixed, arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='optimizer')


    params_lstm = {
        'window'    :[10],
        'loss'      :['mean_squared_error', 'poisson', 'cosine_proximity'],
        'optimizer' :[ 'adam'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    params_ffn = {
        'window_left'  : [6],
        'window_right' : [6],
        'loss'         : ['mean_squared_error', 'poisson', 'cosine_proximity'], 
        'optimizer'    : ['adam'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }

    if start_at <= 3:
        print eval_negation( fixed, arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='loss')

    params_lstm = {
        'window'    :[10],
        'loss'      :['binary_crossentropy', ],
        'optimizer' :[ 'adam'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ],


            [
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':1000, 'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':1500, 'activation': 'relu', 'dropout': 0.2 }
            ],

            
            [
                {'units':750, 'activation': 'selu', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'tanh', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'sigmoid', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'linear', 'dropout': 0.2 }
            ],


            [
                {'units':750, 'activation': 'relu', 'dropout': 0.0 }
            ],
            [
                {'units':750, 'activation': 'relu', 'dropout': 0.1 }
            ],
            [
                {'units':750, 'activation': 'relu', 'dropout': 0.5 }
            ],


            [
                {'units':1500,  'activation': 'relu', 'dropout': 0.2 },
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':2000,  'activation': 'relu', 'dropout': 0.2 },
                {'units':1000,  'activation': 'relu', 'dropout': 0.2 },
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ]

        ]
    }

    params_ffn = {
        'window_left'  : [6],
        'window_right' : [6],
        'loss'         : ['binary_crossentropy'], 
        'optimizer'    : ['adam'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ],


            [
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':1000, 'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':1500, 'activation': 'relu', 'dropout': 0.2 }
            ],

            
            [
                {'units':750, 'activation': 'selu', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'tanh', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'sigmoid', 'dropout': 0.2 }
            ],
            [
                {'units':750, 'activation': 'linear', 'dropout': 0.2 }
            ],


            [
                {'units':750, 'activation': 'relu', 'dropout': 0.0 }
            ],
            [
                {'units':750, 'activation': 'relu', 'dropout': 0.1 }
            ],
            [
                {'units':750, 'activation': 'relu', 'dropout': 0.5 }
            ],


            [
                {'units':1500,  'activation': 'relu', 'dropout': 0.2 },
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ],
            [
                {'units':2000,  'activation': 'relu', 'dropout': 0.2 },
                {'units':1000,  'activation': 'relu', 'dropout': 0.2 },
                {'units':500,  'activation': 'relu', 'dropout': 0.2 }
            ]

        ]
    }

    if start_at <= 4:
        print eval_negation( fixed, arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='layers')


    # params_lstm = {
    #     'window'    :[5,7,10,15,20],
    #     'loss'      :['binary_crossentropy', 'mean_squared_error', 'poisson'],
    #     'optimizer' :[ 'adam', 'RMSprop'],
    #     'layers'    :[
    #         [
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':750,  'activation': 'selu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':1200, 'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 },
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':1000, 'activation': 'relu', 'dropout': 0.2 },
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 },
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ]
    #     ]
    # }


    # params_ffn = {
    #     'window_left'  : [5,10,15],
    #     'window_right' : [5,10,15],
    #     'loss'         : ['binary_crossentropy', 'mean_squared_error', 'poisson'], 
    #     'optimizer'    : ['adam', 'adamax'],
    #     'layers'       :[
    #         [
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':750,  'activation': 'selu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':1200, 'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 },
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ],
    #         [
    #             {'units':1000, 'activation': 'relu', 'dropout': 0.2 },
    #             {'units':750,  'activation': 'relu', 'dropout': 0.2 },
    #             {'units':500,  'activation': 'relu', 'dropout': 0.2 }
    #         ]
    #     ]
    # }


    # if start_at <= 5:
    #     print eval_negation( fixed, arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='all')




