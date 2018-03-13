# -*- encoding: utf-8 -*-
import sys
sys.path.append('../src')

import os
clean = 'cls' if os.name == 'nt' else 'clear'

import cldas.db.crud as dp
from cldas.neg.model import NegScopeLSTM, NegScopeFFN
from cldas.utils.metrics import *
from cldas.utils.misc import Iterable
from cldas.utils import title, Log, Level, save
import time, itertools, json, md5

log = Log('./log')

tagged = dp.get_tagged(tag_as=dp.TaggedType.MANUAL)

PATH = './neg/models'
FIXED = {
        'dimension':len(dp.get_null_embedding()),
        # 'verbose'  :0,
    }


def end_time(start_time,case=''):
    elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time()-start_time))
    print "\n","Elapsed:",elapsed,"\n"
    log( "[%s] Elapsed: %s" % (case,elapsed) , level=Level.DEBUG)
    return elapsed


def _md5(params):
    return md5.new(json.dumps(params)).hexdigest()


def eval_neg( arguments={}, params_lstm=None, params_ffn=None, iter=''):

    # FFN
    if params_ffn and (not arguments or arguments.get('ffn') != None):
        keys_ffn = params_ffn.keys()
        idx = 0
        for par in itertools.product(*params_ffn.values()):
            dict_par = dict( zip(keys_ffn,par) )
            dict_par.update(FIXED)
            if idx < arguments.get('ffn', 0):
                continue
            name = 'Neg_FNN_' + _md5(dict_par) 
            if not os.path.exists(PATH+'/'+name+".h5"):
                print name
                start_time = time.time()

                ann = NegScopeFFN( **dict_par )
                X, Y = dp.get_ffn_dataset( tagged, **dict_par )
                ann.fit( X, Y )
                
                elapsed = end_time(start_time,case='FFN')
                
                score = ann.get_scores( X,Y )
                dp.save_evaluation([dict({
                    'type'          : 'negation',
                    'ANN'           : 'FFN',
                    'name'          : name,
                    'score'         : dict(score),
                    'training_time' : elapsed,
                    'params'        : dict_par
                })])  

                ann.save_model(name, dirpath=PATH)
                save(dict_par,name,PATH)

                log( "Step fnn %d finished." % idx, level=Level.INFO)
            idx += 1

    ## LSTM
    if params_lstm and (not arguments or arguments.get('lstm') != None):
        keys_lstm = params_lstm.keys()
        idx = 0
        for par in itertools.product(*params_lstm.values()):
            dict_par = dict(zip(keys_lstm,par))
            dict_par.update(FIXED)
            if idx < arguments.get('lstm', 0):
                continue
            name = 'Neg_LSTM_' + _md5(dict_par) 
            if not os.path.exists(PATH+'/'+name+".h5"):
                print name
                start_time = time.time()

                ann = NegScopeLSTM( **dict_par )
                X, Y = dp.get_lstm_dataset( tagged, dict_par['window'] )
                ann.fit( X,Y )

                elapsed = end_time(start_time,case='LSTM')

                score = ann.get_scores( X,Y )
                dp.save_evaluation([dict({
                    'type'          : 'negation',
                    'ANN'           : 'LSTM',
                    'name'          : name,
                    'score'         : dict(score),
                    'training_time' : elapsed,
                    'params'        : dict_par
                })])  

                ann.save_model(name, dirpath=PATH)
                save(dict_par,name,PATH)
                
                log( "Step lstm %d - %s finished." % (idx,iter), level=Level.INFO)
            idx += 1

        return 'DONE'



'''
---------------------------------------------
      Evaluation parameters from args
---------------------------------------------
'''
def eval_default_parameters():
    ann = NegScopeFFN( 2,2,300 )
    X, Y = dp.get_ffn_dataset( tagged, 2,2 )
    ann.fit( X, Y )
    ann.save_model('default_FFN', dirpath=PATH)

    ann = NegScopeLSTM( 10,300 )
    X, Y = dp.get_lstm_dataset( tagged, 10 )
    ann.fit( X, Y )
    ann.save_model('default_LSTM', dirpath=PATH)



def eval_varying_window(arguments):
    print title('VARYING WINDOW SIZE')
    params_lstm = {
        'window'    :[5,10,15,20],
        'loss'      :['binary_crossentropy'],
        'optimizer' :['adam'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }
    params_ffn = {
        'window_left'  : [1,3],
        'window_right' : [1,3],
        'loss'         : ['binary_crossentropy'], 
        'optimizer'    : ['adam'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }
    eval_neg( arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='window' )



def eval_varying_optimizer(arguments):
    print title('VARYING OPTIMIZER')
    params_lstm = {
        'window'    :[10],
        'loss'      :['binary_crossentropy'],
        'optimizer' :['Nadam', 'RMSprop'],
        'layers'    :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }
    params_ffn = {
        'window_left'  : [2],
        'window_right' : [2],
        'loss'         : ['binary_crossentropy'], 
        'optimizer'    : ['Adamax', 'SGD'],
        'layers'       :[
            [
                {'units':750,  'activation': 'relu', 'dropout': 0.2 }
            ]
        ]
    }
    eval_neg( arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='optimizer' )



def eval_varying_layers(arguments):
    print title('VARYING LAYERS SHAPES')
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
        'window_left'  : [2],
        'window_right' : [2],
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
    eval_neg( arguments=arguments, params_lstm=params_lstm, params_ffn=params_ffn, iter='layers' )    


def run_level(arguments):
    os.system(clean)
    if arguments['start'] <= 0:
        eval_default_parameters()
    if arguments['start'] <= 1:  
        eval_varying_window(arguments)
    if arguments['start'] <= 2:  
        eval_varying_optimizer(arguments)
    if arguments['start'] <= 3:  
        eval_varying_layers(arguments)


'''
---------------------------------------------
              Main execution
---------------------------------------------
'''

if __name__== '__main__':

    len_arg = len(sys.argv)
    arguments = {}
    if len_arg == 1:
        arguments['ffn']   = 0
        arguments['lstm']  = 0
    else:
        if len_arg >= 3:
            if sys.argv[1] not in ['lstm', 'fnn', 'start'] or not sys.argv[2].isdigit():
                raise ValueError('Arguments must be "[ffn|lstm|start] [steps]"')
            arguments[sys.argv[1]] = int(sys.argv[2])
        if len_arg >= 5:
            if sys.argv[3] not in ['lstm', 'fnn', 'start'] or not sys.argv[4].isdigit():
                raise ValueError('Arguments must be "[ffn|lstm|start] [steps]"')
            arguments[sys.argv[3]] = int(sys.argv[4])
        if len_arg >= 7:
            if sys.argv[3] not in ['lstm', 'fnn', 'start'] or not sys.argv[4].isdigit():
                raise ValueError('Arguments must be "[ffn|lstm|start] [steps]"')
            arguments[sys.argv[3]] = int(sys.argv[4])
    if 'start' not in arguments.keys():
        arguments['start'] = 1

    run_level(arguments)





