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

corpus = [{
    "_id" : "16b287a5b69aed48c0ed71890b739eb0",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFS000",
            "word" : "vez",
            "negated" : False
        }, 
        {
            "lemma" : "más",
            "tag" : "RG",
            "word" : "más",
            "negated" : False
        }, 
        {
            "lemma" : "difícil",
            "tag" : "AQ0CS00",
            "word" : "difícil",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "pantalla",
            "tag" : "NCFS000",
            "word" : "pantalla",
            "negated" : False
        }, 
        {
            "lemma" : "2",
            "tag" : "RG",
            "word" : "2",
            "negated" : False
        }, 
        {
            "lemma" : "7",
            "tag" : "AQ0CS00",
            "word" : "7",
            "negated" : True
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "puf",
            "tag" : "NCMS000",
            "word" : "puf",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "tela",
            "tag" : "NCFS000",
            "word" : "tela",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "56a8760e149fd8a57bfe34a703cea899",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "ami",
            "tag" : "NCMS000",
            "word" : "ami",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "fascinar",
            "tag" : "VMIP3S0",
            "word" : "fascina",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "siempre",
            "tag" : "RG",
            "word" : "siempre",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMII3S0",
            "word" : "jugaba",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "comprar",
            "tag" : "VMIS3P0",
            "word" : "compraron",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "tableta",
            "tag" : "NCFS000",
            "word" : "tableta",
            "negated" : False
        }, 
        {
            "lemma" : "decir",
            "tag" : "VMIS1S0",
            "word" : "dije",
            "negated" : False
        }, 
        {
            "lemma" : "ya",
            "tag" : "RG",
            "word" : "ya",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMIP1S0",
            "word" : "descargo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "candy",
            "tag" : "NCMS000",
            "word" : "candy",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "totalmente",
            "tag" : "RG",
            "word" : "totalmente",
            "negated" : False
        }, 
        {
            "lemma" : "súper",
            "tag" : "AQ0CN00",
            "word" : "súper",
            "negated" : False
        }, 
        {
            "lemma" : "hiper",
            "tag" : "AQ0CN00",
            "word" : "hiper",
            "negated" : False
        }, 
        {
            "lemma" : "mega",
            "tag" : "AQ0CN00",
            "word" : "mega",
            "negated" : False
        }, 
        {
            "lemma" : "recontra",
            "tag" : "NCCS000",
            "word" : "recontra",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "felicitar",
            "tag" : "VMIP1S0",
            "word" : "felicito",
            "negated" : False
        }, 
        {
            "lemma" : "beso",
            "tag" : "NCMP000",
            "word" : "besos",
            "negated" : False
        }, 
        {
            "lemma" : "chau",
            "tag" : "I",
            "word" : "chau",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "e163c6e24e9e48e61ecd979e69fa92d2",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "wau",
            "tag" : "NCCS000",
            "word" : "wau",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "PI0MP00",
            "word" : "todos",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : True
        }, 
        {
            "lemma" : "ninguno",
            "tag" : "DI0MS0",
            "word" : "ningún",
            "negated" : True
        }, 
        {
            "lemma" : "problema",
            "tag" : "NCMS000",
            "word" : "problema",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "PR00000",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : True
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "acabar",
            "tag" : "VMIP3P0",
            "word" : "acaban",
            "negated" : True
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : True
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "porque",
            "tag" : "CS",
            "word" : "porque",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMG0000",
            "word" : "teniendo",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "samsung",
            "tag" : "NCMS000",
            "word" : "samsung",
            "negated" : False
        }, 
        {
            "lemma" : "galaxia",
            "tag" : "NCFS000",
            "word" : "galaxia",
            "negated" : False
        }, 
        {
            "lemma" : "2",
            "tag" : "AQ0CS00",
            "word" : "2",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "llegar",
            "tag" : "VMIP3P0",
            "word" : "llegan",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "corto",
            "tag" : "AQ0MS00",
            "word" : "corto",
            "negated" : False
        }, 
        {
            "lemma" : "tiempo",
            "tag" : "NCMS000",
            "word" : "tiempo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "enseriar",
            "tag" : "VMIP1S0",
            "word" : "enserio",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : True
        }, 
        {
            "lemma" : "lento",
            "tag" : "AQ0MS00",
            "word" : "lento",
            "negated" : True
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "638ab17c557f083a7c1123c74d02e8a4",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMIP3P0",
            "word" : "gustan",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "RG",
            "word" : "mucho",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "caramelo",
            "tag" : "NCMP000",
            "word" : "caramelos",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "personaje",
            "tag" : "NCMP000",
            "word" : "personajes",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "musicar",
            "tag" : "VMIP3S0",
            "word" : "musica",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "fondo",
            "tag" : "NCMS000",
            "word" : "fondo",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP3S0",
            "word" : "tiene",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "NCMS000",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "cincar",
            "tag" : "VMIP1S0",
            "word" : "cinco",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "porque",
            "tag" : "CS",
            "word" : "porque",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIC3S0",
            "word" : "jugaría",
            "negated" : True
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MS0",
            "word" : "todo",
            "negated" : True
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : True
        }, 
        {
            "lemma" : "rato",
            "tag" : "NCMS000",
            "word" : "rato",
            "negated" : True
        }, 
        {
            "lemma" : "asta",
            "tag" : "NCFS000",
            "word" : "asta",
            "negated" : True
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "aburrir",
            "tag" : "VMSI3S0",
            "word" : "aburriera",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIC3S0",
            "word" : "jugaría",
            "negated" : True
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "7f125e468d7948c0583baa5d4e38a846",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "genial",
            "tag" : "AQ0CS00",
            "word" : "genial",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "aunque",
            "tag" : "CC",
            "word" : "aunque",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "diferencia",
            "tag" : "NCFP000",
            "word" : "diferencias",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIP2S0",
            "word" : "juegas",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "través",
            "tag" : "NCMS000",
            "word" : "través",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "androide",
            "tag" : "NCMS000",
            "word" : "androide",
            "negated" : False
        }, 
        {
            "lemma" : "o",
            "tag" : "CC",
            "word" : "o",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "través",
            "tag" : "NCMS000",
            "word" : "través",
            "negated" : False
        }, 
        {
            "lemma" : "d",
            "tag" : "NCFS000",
            "word" : "d",
            "negated" : False
        }, 
        {
            "lemma" : "htc",
            "tag" : "NC00000",
            "word" : "htc",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "deber",
            "tag" : "VMIC3S0",
            "word" : "debería",
            "negated" : True
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSN0000",
            "word" : "ser",
            "negated" : True
        }, 
        {
            "lemma" : "asi",
            "tag" : "NCMS000",
            "word" : "asi",
            "negated" : True
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "mismo",
            "tag" : "AQ0MS00",
            "word" : "mismo",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "52d3ddd60e0afe5ba6547c48c89b74cb",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "actualizar",
            "tag" : "VMSP3P0",
            "word" : "actualicen",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ir",
            "tag" : "VMIP1S0",
            "word" : "voy",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "adelantar",
            "tag" : "VMP00SF",
            "word" : "adelantada",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMP000",
            "word" : "niveles",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "móvil",
            "tag" : "NCMS000",
            "word" : "móvil",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP2S0",
            "word" : "tienes",
            "negated" : False
        }, 
        {
            "lemma" : "amigo",
            "tag" : "NCMP000",
            "word" : "amigos",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : "k",
            "tag" : "NCFS000",
            "word" : "k",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMSP3P0",
            "word" : "jueguen",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : True
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3P0",
            "word" : "son",
            "negated" : True
        }, 
        {
            "lemma" : "problema",
            "tag" : "NCMS000",
            "word" : "problema",
            "negated" : True
        }, 
        {
            "lemma" : "deber",
            "tag" : "VMIC3P0",
            "word" : "deberían",
            "negated" : True
        }, 
        {
            "lemma" : "regalar",
            "tag" : "VMN0000",
            "word" : "regalar",
            "negated" : True
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : True
        }, 
        {
            "lemma" : "botar",
            "tag" : "VMSP2S0",
            "word" : "botés",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "254ec3d375940b52e1298768c4d62175",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "poner",
            "tag" : "VMIP3S0",
            "word" : "pone",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "pantalla",
            "tag" : "NCFS000",
            "word" : "pantalla",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "contraste",
            "tag" : "NCMS000",
            "word" : "contraste",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : True
        }, 
        {
            "lemma" : "quitar",
            "tag" : "VMIP3S0",
            "word" : "quita",
            "negated" : True
        }, 
        {
            "lemma" : "hasta",
            "tag" : "SP",
            "word" : "hasta",
            "negated" : True
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "apagar",
            "tag" : "VMIP3S0",
            "word" : "apaga",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "prendar",
            "tag" : "VMIP1S0",
            "word" : "prendo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP1S0",
            "word" : "tengo",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "galaxy",
            "tag" : "NCFS000",
            "word" : "galaxy",
            "negated" : False
        }, 
        {
            "lemma" : "notar",
            "tag" : "VMSP3S0",
            "word" : "note",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "versión",
            "tag" : "NCFS000",
            "word" : "versión",
            "negated" : False
        }, 
        {
            "lemma" : "engarberad",
            "tag" : "NCFS000",
            "word" : "engarberad",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "6d913592c31327d9f0839558ae6c49fb",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : True
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : True
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP3S0",
            "word" : "puede",
            "negated" : True
        }, 
        {
            "lemma" : "parar",
            "tag" : "VMN0000",
            "word" : "parar",
            "negated" : True
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : True
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : True
        }, 
        {
            "lemma" : "lamentablemente",
            "tag" : "RG",
            "word" : "lamentablemente",
            "negated" : True
        }, 
        {
            "lemma" : "carajo",
            "tag" : "NCMS000",
            "word" : "carajo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMM03P0",
            "word" : "descarguen",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "PP3CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "valer",
            "tag" : "VMIP3S0",
            "word" : "vale",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "pena",
            "tag" : "NCFS000",
            "word" : "pena",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQSMS00",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "ca82c7f70acf63c7f8639997e42a49f1",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "(",
            "tag" : "Fpa",
            "word" : "(",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : ")",
            "tag" : "Fpt",
            "word" : ")",
            "negated" : False
        }, 
        {
            "lemma" : "pues",
            "tag" : "CS",
            "word" : "pues",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "metro",
            "tag" : "NCMN000",
            "word" : "m",
            "negated" : False
        }, 
        {
            "lemma" : "par",
            "tag" : "NCMS000",
            "word" : "par",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "DD0MS0",
            "word" : "ese",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "interesante",
            "tag" : "AQ0CS00",
            "word" : "interesante",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "ay",
            "tag" : "I",
            "word" : "ay",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMP000",
            "word" : "niveles",
            "negated" : False
        }, 
        {
            "lemma" : "k",
            "tag" : "NCFS000",
            "word" : "k",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "pasa",
            "tag" : "NCFP000",
            "word" : "pasas",
            "negated" : False
        }, 
        {
            "lemma" : "fácilmente",
            "tag" : "RG",
            "word" : "fácilmente",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "otro",
            "tag" : "DI0MP0",
            "word" : "otros",
            "negated" : False
        }, 
        {
            "lemma" : "k",
            "tag" : "NCFS000",
            "word" : "k",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "batallar",
            "tag" : "VMIP2S0",
            "word" : "batallas",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "RG",
            "word" : "mucho",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "pesar",
            "tag" : "VMN0000",
            "word" : "pesar",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "PI0MS00",
            "word" : "todo",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "recomendar",
            "tag" : "VMIP1S0",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},
{
    "_id" : "2c0b8623f28b2baeed36dcaa5fdcd4d8",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "verdad",
            "tag" : "NCFS000",
            "word" : "verdad",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "padre",
            "tag" : "NCMS000",
            "word" : "padre",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "mayoría",
            "tag" : "NCFS000",
            "word" : "mayoría",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CPS",
            "word" : "mis",
            "negated" : False
        }, 
        {
            "lemma" : "familiar",
            "tag" : "NCMP000",
            "word" : "familiares",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIP3S0",
            "word" : "juega",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "solo",
            "tag" : "AQ0MS00",
            "word" : "solo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "desesperar",
            "tag" : "VMIP1S0",
            "word" : "desespero",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : False
        }, 
        {
            "lemma" : "pasar",
            "tag" : "VMN0000",
            "word" : "pasar",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : "pronto",
            "tag" : "RG",
            "word" : "pronto",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "luego",
            "tag" : "RG",
            "word" : "luego",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMN0000",
            "word" : "dar",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "ff5ad5f1d5f245631bb7c860376f6866",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "entretenido",
            "tag" : "NCMS000",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "aunque",
            "tag" : "CC",
            "word" : "aunque",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMP000",
            "word" : "niveles",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "su",
            "tag" : "DP3CSN",
            "word" : "su",
            "negated" : False
        }, 
        {
            "lemma" : "dificultad",
            "tag" : "NCFS000",
            "word" : "dificultad",
            "negated" : False
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMIP3S0",
            "word" : "hace",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "perder",
            "tag" : "VMSP2S0",
            "word" : "pierdas",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "DI0FP0",
            "word" : "muchas",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMSP2S0",
            "word" : "tengas",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "repetir",
            "tag" : "VMN0000",
            "word" : "repetir",
            "negated" : False
        }, 
        {
            "lemma" : "varios",
            "tag" : "DI0FP0",
            "word" : "varias",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFP000",
            "word" : "veces",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "dba6cbe6091c32382096ed33f7e93e64",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "pantalla",
            "tag" : "NCFS000",
            "word" : "pantalla",
            "negated" : False
        }, 
        {
            "lemma" : "negro",
            "tag" : "AQ0FS00",
            "word" : "negra",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "mal",
            "tag" : "RG",
            "word" : "mal",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "pantalla",
            "tag" : "NCFS000",
            "word" : "pantalla",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "poner",
            "tag" : "VMIP3S0",
            "word" : "pone",
            "negated" : False
        }, 
        {
            "lemma" : "negro",
            "tag" : "AQ0FS00",
            "word" : "negra",
            "negated" : False
        }, 
        {
            "lemma" : "luego",
            "tag" : "RG",
            "word" : "luego",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "actualización",
            "tag" : "NCFS000",
            "word" : "actualización",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "esperar",
            "tag" : "VMIP1S0",
            "word" : "espero",
            "negated" : False
        }, 
        {
            "lemma" : "corregir",
            "tag" : "VMSP3P0",
            "word" : "corrijan",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "desagradable",
            "tag" : "AQ0CS00",
            "word" : "desagradable",
            "negated" : False
        }, 
        {
            "lemma" : "situación",
            "tag" : "NCFS000",
            "word" : "situación",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "más",
            "tag" : "RG",
            "word" : "más",
            "negated" : False
        }, 
        {
            "lemma" : "pronto",
            "tag" : "RG",
            "word" : "pronto",
            "negated" : False
        }, 
        {
            "lemma" : "posible",
            "tag" : "AQ0CS00",
            "word" : "posible",
            "negated" : False
        }, 
        {
            "lemma" : "antes",
            "tag" : "RG",
            "word" : "antes",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "seguir",
            "tag" : "VMSP3S0",
            "word" : "siga",
            "negated" : False
        }, 
        {
            "lemma" : "calificar",
            "tag" : "VMG0000",
            "word" : "calificando",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFS000",
            "word" : "estrella",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "ahora",
            "tag" : "RG",
            "word" : "ahora",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "cerrar",
            "tag" : "VMIP3S0",
            "word" : "cierra",
            "negated" : False
        }, 
        {
            "lemma" : "forzosamente",
            "tag" : "RG",
            "word" : "forzosamente",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "57652460f91bfeff810db64220b5bbef",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "altamente",
            "tag" : "RG",
            "word" : "altamente",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "cuidado",
            "tag" : "NCMS000",
            "word" : "cuidado",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "solo",
            "tag" : "AQ0MS00",
            "word" : "solo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "metro",
            "tag" : "NCMN000",
            "word" : "m",
            "negated" : False
        }, 
        {
            "lemma" : "estanco",
            "tag" : "AQ0MS00",
            "word" : "estanco",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "rato",
            "tag" : "NCMS000",
            "word" : "rato",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "determinar",
            "tag" : "VMP00PM",
            "word" : "determinados",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMP000",
            "word" : "niveles",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP1S0",
            "word" : "tengo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "estar",
            "tag" : "VAN0000",
            "word" : "estar",
            "negated" : False
        }, 
        {
            "lemma" : "pedir",
            "tag" : "VMG0000",
            "word" : "pidiendo",
            "negated" : False
        }, 
        {
            "lemma" : "ayuda",
            "tag" : "NCFS000",
            "word" : "ayuda",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CPS",
            "word" : "mis",
            "negated" : False
        }, 
        {
            "lemma" : "amigo",
            "tag" : "NCMP000",
            "word" : "amigos",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "pues",
            "tag" : "CS",
            "word" : "pues",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD0FS00",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "trato",
            "tag" : "NCMS000",
            "word" : "trato",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSN0000",
            "word" : "ser",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "1",
            "tag" : "AO0MS00",
            "word" : "primer",
            "negated" : False
        }, 
        {
            "lemma" : "lugar",
            "tag" : "NCMS000",
            "word" : "lugar",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "nunca",
            "tag" : "RG",
            "word" : "nunca",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "aburrir",
            "tag" : "VMIP2S0",
            "word" : "aburres",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "501670f2fb01bc50d0c9a6da2bfec7c9",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "funcionar",
            "tag" : "VMIP3S0",
            "word" : "funciona",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "serio",
            "tag" : "AQ0FS00",
            "word" : "seria",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "RG",
            "word" : "mucho",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "útil",
            "tag" : "AQ0CS00",
            "word" : "útil",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "PR00000",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "pedir",
            "tag" : "VMIP1P0",
            "word" : "pedimos",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSSP1S0",
            "word" : "sea",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "lista",
            "tag" : "NCFS000",
            "word" : "lista",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "contacto",
            "tag" : "NCMP000",
            "word" : "contactos",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIP3P0",
            "word" : "juegan",
            "negated" : False
        }, 
        {
            "lemma" : "candy",
            "tag" : "NCMS000",
            "word" : "candy",
            "negated" : False
        }, 
        {
            "lemma" : "cursar",
            "tag" : "VMM02P0",
            "word" : "cursad",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : True
        }, 
        {
            "lemma" : "cualquiera",
            "tag" : "PI0CS00",
            "word" : "cualquiera",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "perder",
            "tag" : "VMP00SF",
            "word" : "perdida",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "tiempo",
            "tag" : "NCMS000",
            "word" : "tiempo",
            "negated" : False
        }, 
        {
            "lemma" : "buscar",
            "tag" : "VMN0000",
            "word" : "buscar",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "PI0MS00",
            "word" : "uno",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : True
        }, 
        {
            "lemma" : "uno",
            "tag" : "PI0MS00",
            "word" : "uno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "478dd913baa594de4d32bc83dc23ee1d",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entre",
            "tag" : "SP",
            "word" : "entre",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "diseñar",
            "tag" : "VMP00SM",
            "word" : "diseñado",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMSP3P0",
            "word" : "den",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "posibilidad",
            "tag" : "NCFS000",
            "word" : "posibilidad",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMN0000",
            "word" : "dar",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "cosa",
            "tag" : "NCFP000",
            "word" : "cosas",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "amigo",
            "tag" : "NCMP000",
            "word" : "amigos",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMN0000",
            "word" : "poder",
            "negated" : False
        }, 
        {
            "lemma" : "recibir",
            "tag" : "VMN0000",
            "word" : "recibir",
            "negated" : False
        }, 
        {
            "lemma" : "ayuda",
            "tag" : "NCFP000",
            "word" : "ayudas",
            "negated" : False
        }, 
        {
            "lemma" : "también",
            "tag" : "RG",
            "word" : "también",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "8e42d97b01ff91aaeb154e3ceaa68219",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "fáunico",
            "tag" : "AQ0FS00",
            "word" : "fáunica",
            "negated" : False
        }, 
        {
            "lemma" : "re",
            "tag" : "NCMS000",
            "word" : "re",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "funcionar",
            "tag" : "VMIP3S0",
            "word" : "funciona",
            "negated" : False
        }, 
        {
            "lemma" : "re",
            "tag" : "NCMS000",
            "word" : "re",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "galaxy",
            "tag" : "NCFS000",
            "word" : "galaxy",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : False
        }, 
        {
            "lemma" : "avance",
            "tag" : "NCMS000",
            "word" : "avance",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "llegar",
            "tag" : "VMSP3S0",
            "word" : "llegue",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : "1",
            "tag" : "AQ0CS00",
            "word" : "1",
            "negated" : False
        }, 
        {
            "lemma" : "9",
            "tag" : "NCMS000",
            "word" : "9",
            "negated" : False
        }, 
        {
            "lemma" : "sin",
            "tag" : "SP",
            "word" : "sin",
            "negated" : False
        }, 
        {
            "lemma" : "ninguno",
            "tag" : "DI0MS0",
            "word" : "ningún",
            "negated" : False
        }, 
        {
            "lemma" : "problema",
            "tag" : "NCMS000",
            "word" : "problema",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "5188bedf647e44827df078e43bdae94e",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "lindo",
            "tag" : "AQ0MS00",
            "word" : "lindo",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "último",
            "tag" : "AO0FS00",
            "word" : "última",
            "negated" : False
        }, 
        {
            "lemma" : "actualización",
            "tag" : "NCFS000",
            "word" : "actualización",
            "negated" : False
        }, 
        {
            "lemma" : "dejar",
            "tag" : "VMIS3S0",
            "word" : "dejó",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "aplicación",
            "tag" : "NCFS000",
            "word" : "aplicación",
            "negated" : False
        }, 
        {
            "lemma" : "sin",
            "tag" : "SP",
            "word" : "sin",
            "negated" : False
        }, 
        {
            "lemma" : "uso",
            "tag" : "NCMS000",
            "word" : "uso",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : True
        }, 
        {
            "lemma" : "permitir",
            "tag" : "VMIP3S0",
            "word" : "permite",
            "negated" : True
        }, 
        {
            "lemma" : "entrar",
            "tag" : "VMN0000",
            "word" : "entrar",
            "negated" : True
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : True
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : True
        }, 
        {
            "lemma" : "candy",
            "tag" : "NCMS000",
            "word" : "candy",
            "negated" : True
        }, 
        {
            "lemma" : "cursar",
            "tag" : "VMM02P0",
            "word" : "cursad",
            "negated" : True
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFS000",
            "word" : "saga",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "favor",
            "tag" : "NCMS000",
            "word" : "favor",
            "negated" : False
        }, 
        {
            "lemma" : "verificar",
            "tag" : "VMSP3P0",
            "word" : "verifiquen",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD00S00",
            "word" : "esto",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "gracia",
            "tag" : "NCFP000",
            "word" : "gracias",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "quedar",
            "tag" : "VMIS3S0",
            "word" : "quedó",
            "negated" : False
        }, 
        {
            "lemma" : "inactivo",
            "tag" : "AQ0MS00",
            "word" : "inactivo",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "samsung",
            "tag" : "NCMS000",
            "word" : "samsung",
            "negated" : False
        }, 
        {
            "lemma" : "galayo",
            "tag" : "NCMS000",
            "word" : "galayo",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "ecd0d215ca4fc797bbd467a036472033",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "genial",
            "tag" : "AQ0CS00",
            "word" : "genial",
            "negated" : False
        }, 
        {
            "lemma" : "usar",
            "tag" : "VMM03S0",
            "word" : "use",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MPA0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : "ami",
            "tag" : "NCMS000",
            "word" : "ami",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "funcionar",
            "tag" : "VMIP3S0",
            "word" : "funciona",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adicto",
            "tag" : "AQ0MS00",
            "word" : "adicto",
            "negated" : False
        }, 
        {
            "lemma" : "mí",
            "tag" : "PP1CSO0",
            "word" : "mí",
            "negated" : False
        }, 
        {
            "lemma" : "familia",
            "tag" : "NCFS000",
            "word" : "familia",
            "negated" : False
        }, 
        {
            "lemma" : "i",
            "tag" : "NCFS000",
            "word" : "i",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMIP1P0",
            "word" : "jugamos",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MP0",
            "word" : "todos",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "día",
            "tag" : "NCMP000",
            "word" : "días",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP1S0",
            "word" : "tengo",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "tableta",
            "tag" : "NCFS000",
            "word" : "tableta",
            "negated" : False
        }, 
        {
            "lemma" : "len",
            "tag" : "AQ0CS00",
            "word" : "len",
            "negated" : False
        }, 
        {
            "lemma" : "ovo",
            "tag" : "NCMS000",
            "word" : "ovo",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "1",
            "tag" : "NCMS000",
            "word" : "1",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "e",
            "negated" : False
        }, 
        {
            "lemma" : "2",
            "tag" : "NCMS000",
            "word" : "2",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "funcionar",
            "tag" : "VMIP3S0",
            "word" : "funciona",
            "negated" : False
        }, 
        {
            "lemma" : "genial",
            "tag" : "AQ0CS00",
            "word" : "genial",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "i",
            "tag" : "NCFS000",
            "word" : "i",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMSP2S0",
            "word" : "tengas",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMP000",
            "word" : "juegos",
            "negated" : True
        }, 
        {
            "lemma" : "genial",
            "tag" : "AQ0CP00",
            "word" : "geniales",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "577959076cabce83f25a0a498bfd1167",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQSMS00",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "ayudar",
            "tag" : "VMIP3S0",
            "word" : "ayuda",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "sacar",
            "tag" : "VMN0000",
            "word" : "sacar",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "tristeza",
            "tag" : "NCFS000",
            "word" : "tristeza",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "estrés",
            "tag" : "NCMS000",
            "word" : "estrés",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQSMS00",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "ayudar",
            "tag" : "VMIP3S0",
            "word" : "ayuda",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "sacar",
            "tag" : "VMN0000",
            "word" : "sacar",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "tristeza",
            "tag" : "NCFS000",
            "word" : "tristeza",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "estrés",
            "tag" : "NCMS000",
            "word" : "estrés",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : True
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : True
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP3P0",
            "word" : "tienen",
            "negated" : True
        }, 
        {
            "lemma" : "bajar",
            "tag" : "VMM03P0",
            "word" : "bajen",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "solo",
            "tag" : "RG",
            "word" : "solo",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP1S0",
            "word" : "tengo",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "problema",
            "tag" : "NCMS000",
            "word" : "problema",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "acautelar",
            "tag" : "VMG0000",
            "word" : "acautelando",
            "negated" : False
        }, 
        {
            "lemma" : "nos",
            "tag" : "PP1CP00",
            "word" : "nos",
            "negated" : False
        }, 
        {
            "lemma" : "nuevo",
            "tag" : "AQ0FP00",
            "word" : "nuevas",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : False
        }, 
        {
            "lemma" : "conectar",
            "tag" : "VMN0000",
            "word" : "conectar",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "faz",
            "tag" : "NCFP000",
            "word" : "faces",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "k",
            "tag" : "NCFS000",
            "word" : "k",
            "negated" : False
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMIP1S0",
            "word" : "hago",
            "negated" : False
        }, 
        {
            "lemma" : "ayudar",
            "tag" : "VMM03P0",
            "word" : "ayuden",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "carajo",
            "tag" : "NCMS000",
            "word" : "carajo",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "78a6f388000f1d69015c2edd06b29798",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "único",
            "tag" : "AQ0MS00",
            "word" : "único",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFP000",
            "word" : "veces",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "congelar",
            "tag" : "VMIP3S0",
            "word" : "congela",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "general",
            "tag" : "AQ0CS00",
            "word" : "general",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD0FS00",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "huevar",
            "tag" : "VMSF1S0",
            "word" : "huevare",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "fiar",
            "tag" : "VMN0000",
            "word" : "fiar",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "héroe",
            "tag" : "NCMP000",
            "word" : "héroes",
            "negated" : False
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFS000",
            "word" : "saga",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "seguro",
            "tag" : "AQ0MS00",
            "word" : "seguro",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIF3S0",
            "word" : "será",
            "negated" : False
        }, 
        {
            "lemma" : "tan",
            "tag" : "RG",
            "word" : "tan",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "como",
            "tag" : "CS",
            "word" : "como",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "petar",
            "tag" : "VMIS3S0",
            "word" : "petó",
            "negated" : False
        }, 
        {
            "lemma" : "resumir",
            "tag" : "VMIP3S0",
            "word" : "resume",
            "negated" : False
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFS000",
            "word" : "saga",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "desarrollador",
            "tag" : "NCMS000",
            "word" : "desarrollador",
            "negated" : False
        }, 
        {
            "lemma" : "siempre",
            "tag" : "RG",
            "word" : "siempre",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3P0",
            "word" : "son",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MP00",
            "word" : "buenos",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMP000",
            "word" : "juegos",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "gracia",
            "tag" : "NCFP000",
            "word" : "gracias",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "4d675633207cf1487a2cc30f47272964",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "aun",
            "tag" : "RG",
            "word" : "aun",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "cantidad",
            "tag" : "NCFS000",
            "word" : "cantidad",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFS000",
            "word" : "vida",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "poco",
            "tag" : "DI0FS0",
            "word" : "poca",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "parecer",
            "tag" : "VMN0000",
            "word" : "parecer",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "porque",
            "tag" : "CS",
            "word" : "porque",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "nos",
            "tag" : "PP1CP00",
            "word" : "nos",
            "negated" : True
        }, 
        {
            "lemma" : "permitir",
            "tag" : "VMIP3S0",
            "word" : "permite",
            "negated" : False
        }, 
        {
            "lemma" : "pasar",
            "tag" : "VMN0000",
            "word" : "pasar",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MS0",
            "word" : "todo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "día",
            "tag" : "NCMS000",
            "word" : "día",
            "negated" : False
        }, 
        {
            "lemma" : "pegar",
            "tag" : "VMP00PM",
            "word" : "pegados",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMG0000",
            "word" : "jugando",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : True
        }, 
        {
            "lemma" : "enviciar",
            "tag" : "VMIP3P0",
            "word" : "envician",
            "negated" : True
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "dc01db08ec7bb3b6e51ec78b1964a0ca",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encasta",
            "tag" : "NCFS000",
            "word" : "encasta",
            "negated" : False
        }, 
        {
            "lemma" : "quien",
            "tag" : "PR0CS00",
            "word" : "quien",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD0MS00",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "leer",
            "tag" : "VMG0000",
            "word" : "leyendo",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD00S00",
            "word" : "esto",
            "negated" : False
        }, 
        {
            "lemma" : "seguir",
            "tag" : "VMSP3S0",
            "word" : "siga",
            "negated" : False
        }, 
        {
            "lemma" : "leer",
            "tag" : "VMG0000",
            "word" : "leyendo",
            "negated" : False
        }, 
        {
            "lemma" : "poner",
            "tag" : "VMSP3P0",
            "word" : "pongan",
            "negated" : False
        }, 
        {
            "lemma" : "youtube",
            "tag" : "NP00000",
            "word" : "youtube",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "doler",
            "tag" : "VMIP3P0",
            "word" : "duelen",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "buscar",
            "tag" : "VMN0000",
            "word" : "buscar",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "escribir",
            "tag" : "VMSP3P0",
            "word" : "escriban",
            "negated" : False
        }, 
        {
            "lemma" : ":",
            "tag" : "Fd",
            "word" : ":",
            "negated" : False
        }, 
        {
            "lemma" : "desliñar",
            "tag" : "VMIP1S0",
            "word" : "desliño",
            "negated" : False
        }, 
        {
            "lemma" : "cubrir",
            "tag" : "VMIP3S0",
            "word" : "cubre",
            "negated" : False
        }, 
        {
            "lemma" : "world",
            "tag" : "NP00000",
            "word" : "world",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "último",
            "tag" : "AO0MS00",
            "word" : "último",
            "negated" : False
        }, 
        {
            "lemma" : "disfrutar",
            "tag" : "VMSP3P0",
            "word" : "disfruten",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "después",
            "tag" : "RG",
            "word" : "después",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMN0000",
            "word" : "haber",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMN0000",
            "word" : "descargar",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "b11f9f240ef89589eeb41a410362fbbe",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "mejor",
            "tag" : "AQ0CS00",
            "word" : "mejor",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ver",
            "tag" : "VMIS1S0",
            "word" : "vi",
            "negated" : False
        }, 
        {
            "lemma" : "hasta",
            "tag" : "SP",
            "word" : "hasta",
            "negated" : False
        }, 
        {
            "lemma" : "ahora",
            "tag" : "RG",
            "word" : "ahora",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "par",
            "tag" : "NCMS000",
            "word" : "par",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "PI0MS00",
            "word" : "uno",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "mejor",
            "tag" : "AQ0CP00",
            "word" : "mejores",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMP000",
            "word" : "juegos",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MS0",
            "word" : "todo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "capaz",
            "tag" : "AQ0CS00",
            "word" : "capaz",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "también",
            "tag" : "RG",
            "word" : "también",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "mundo",
            "tag" : "NCMS000",
            "word" : "mundo",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "P01CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : True
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : True
        }, 
        {
            "lemma" : "buenísimo",
            "tag" : "NCMS000",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "recomendar",
            "tag" : "VMIP1S0",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "bb3881ddf0e07c7271ae2ebb713c8947",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "bañar",
            "tag" : "VMIP3P0",
            "word" : "bañan",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : "9",
            "tag" : "AQ0CS00",
            "word" : "9",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "desestresante",
            "tag" : "AQ0CS00",
            "word" : "desestresante",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0FS00",
            "word" : "buena",
            "negated" : False
        }, 
        {
            "lemma" : "terapia",
            "tag" : "NCFS000",
            "word" : "terapia",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "desconectar",
            "tag" : "VMN0000",
            "word" : "desconectar",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0FS00",
            "word" : "buena",
            "negated" : False
        }, 
        {
            "lemma" : "medicina",
            "tag" : "NCFS000",
            "word" : "medicina",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "estresados",
            "tag" : "VMP00PM",
            "word" : "estresados",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "92f371a93e87a88b53a49f72dbba56cf",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMIP3S0",
            "word" : "gusta",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "RG",
            "word" : "mucho",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MS0",
            "word" : "todo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "día",
            "tag" : "NCMS000",
            "word" : "día",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : True
        }, 
        {
            "lemma" : "aburrir",
            "tag" : "VMIP3S0",
            "word" : "aburre",
            "negated" : True
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : True
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP1S0",
            "word" : "doy",
            "negated" : True
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : True
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : True
        }, 
        {
            "lemma" : "amojar",
            "tag" : "VMM02S0",
            "word" : "amoja",
            "negated" : True
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3FSA0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "37b512bf65067254bd1bc9e93776c075",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "verdad",
            "tag" : "NCFS000",
            "word" : "verdad",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "tenia",
            "tag" : "NCFS000",
            "word" : "tenia",
            "negated" : False
        }, 
        {
            "lemma" : "duda",
            "tag" : "NCFP000",
            "word" : "dudas",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "bajar",
            "tag" : "VMN0000",
            "word" : "bajar",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "igual",
            "tag" : "AQ0CS00",
            "word" : "igual",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "caso",
            "tag" : "NCMS000",
            "word" : "caso",
            "negated" : False
        }, 
        {
            "lemma" : "mejor",
            "tag" : "AQ0CS00",
            "word" : "mejor",
            "negated" : False
        }, 
        {
            "lemma" : "aqui",
            "tag" : "VMIS1S0",
            "word" : "aqui",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "notar",
            "tag" : "VMM03S0",
            "word" : "note",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "tildar",
            "tag" : "VMIP3S0",
            "word" : "tilda",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "celar",
            "tag" : "VMIS3S0",
            "word" : "celó",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : False
        }, 
        {
            "lemma" : "3",
            "tag" : "AQ0CS00",
            "word" : "3",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "andar",
            "tag" : "VMIP3S0",
            "word" : "anda",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "maravilla",
            "tag" : "NCFS000",
            "word" : "maravilla",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "opinión",
            "tag" : "NCFP000",
            "word" : "opiniones",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "decir",
            "tag" : "VMIP3P0",
            "word" : "dicen",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "comprar",
            "tag" : "VMN0000",
            "word" : "comprar",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "botar",
            "tag" : "VMSP2S0",
            "word" : "botés",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "si",
            "tag" : "CS",
            "word" : "si",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "comprar",
            "tag" : "VMN0000",
            "word" : "comprar",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MPA0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "como",
            "tag" : "CS",
            "word" : "como",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "x",
            "tag" : "NCFS000",
            "word" : "x",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP1S0",
            "word" : "doy",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "4fe5b92df102a9b9a04cefaf09b4f153",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMIP3S0",
            "word" : "gusta",
            "negated" : False
        }, 
        {
            "lemma" : "muo",
            "tag" : "AQ0MS00",
            "word" : "muo",
            "negated" : False
        }, 
        {
            "lemma" : "o",
            "tag" : "NCFP000",
            "word" : "os",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3FSA0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMSP2P0",
            "word" : "descarguéis",
            "negated" : False
        }, 
        {
            "lemma" : "muí",
            "tag" : "RG",
            "word" : "muí",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMM02S0",
            "word" : "encantá",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "único",
            "tag" : "AQ0MS00",
            "word" : "único",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "acabar",
            "tag" : "VMIP3S0",
            "word" : "acaba",
            "negated" : False
        }, 
        {
            "lemma" : "mí",
            "tag" : "PP1CSO0",
            "word" : "mí",
            "negated" : False
        }, 
        {
            "lemma" : "pronto",
            "tag" : "RG",
            "word" : "pronto",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : True
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "9086e67835254afdd4677ab3555adf68",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "horrible",
            "tag" : "AQ0CS00",
            "word" : "horrible",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "peor",
            "tag" : "AQ0CS00",
            "word" : "peor",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "PD0FS00",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "aburrir",
            "tag" : "VMP00SM",
            "word" : "aburrido",
            "negated" : False
        }, 
        {
            "lemma" : "además",
            "tag" : "RG",
            "word" : "además",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3FSA0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "musicar",
            "tag" : "VMIP3S0",
            "word" : "musica",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "feo",
            "tag" : "AQ0FS00",
            "word" : "fea",
            "negated" : True
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMSP3P0",
            "word" : "descarguen",
            "negated" : True
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : True
        }, 
        {
            "lemma" : "decepcionar",
            "tag" : "VMSI3P0",
            "word" : "decepcionaran",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "5abb7a939f32f0ec3e70f21466a30c42",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP3S0",
            "word" : "da",
            "negated" : False
        }, 
        {
            "lemma" : "gana",
            "tag" : "NCFP000",
            "word" : "ganas",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "hora",
            "tag" : "NCFP000",
            "word" : "horas",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "correr",
            "tag" : "VMIP3S0",
            "word" : "corre",
            "negated" : False
        }, 
        {
            "lemma" : "sin",
            "tag" : "SP",
            "word" : "sin",
            "negated" : False
        }, 
        {
            "lemma" : "ninguno",
            "tag" : "DI0MS0",
            "word" : "ningún",
            "negated" : False
        }, 
        {
            "lemma" : "problema",
            "tag" : "NCMS000",
            "word" : "problema",
            "negated" : True
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "samsung",
            "tag" : "NCMS000",
            "word" : "samsung",
            "negated" : False
        }, 
        {
            "lemma" : "galayo",
            "tag" : "NCMS000",
            "word" : "galayo",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : False
        }, 
        {
            "lemma" : "4",
            "tag" : "AQ0CS00",
            "word" : "4",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "cd5aadf8e9a3d2694cc4b444fbc8e2e3",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "genial",
            "tag" : "AQ0CS00",
            "word" : "genial",
            "negated" : False
        }, 
        {
            "lemma" : "pasar",
            "tag" : "VMIP3S0",
            "word" : "pasa",
            "negated" : False
        }, 
        {
            "lemma" : "tiempo",
            "tag" : "NCMS000",
            "word" : "tiempo",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "PI0MS00",
            "word" : "uno",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CPS",
            "word" : "mis",
            "negated" : False
        }, 
        {
            "lemma" : "favorito",
            "tag" : "NCMP000",
            "word" : "favoritos",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "igual",
            "tag" : "AQ0CS00",
            "word" : "igual",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "petar",
            "tag" : "VMIS3S0",
            "word" : "petó",
            "negated" : False
        }, 
        {
            "lemma" : "resumir",
            "tag" : "VMIP3S0",
            "word" : "resume",
            "negated" : False
        }, 
        {
            "lemma" : "creer",
            "tag" : "VMIP1S0",
            "word" : "creo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "deber",
            "tag" : "VMIC3P0",
            "word" : "deberían",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMN0000",
            "word" : "tener",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFP000",
            "word" : "sagas",
            "negated" : False
        }, 
        {
            "lemma" : "como",
            "tag" : "CS",
            "word" : "como",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FP0",
            "word" : "estas",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "0771980df4d59050e61bd5077e78195f",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMIP3S0",
            "word" : "gusta",
            "negated" : False
        }, 
        {
            "lemma" : "solo",
            "tag" : "RG",
            "word" : "solo",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMIC3S0",
            "word" : "gustaría",
            "negated" : False
        }, 
        {
            "lemma" : "adquirir",
            "tag" : "VMN0000",
            "word" : "adquirir",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "movimiento",
            "tag" : "NCMP000",
            "word" : "movimientos",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "otro",
            "tag" : "DI0FS0",
            "word" : "otra",
            "negated" : False
        }, 
        {
            "lemma" : "firma",
            "tag" : "NCFS000",
            "word" : "firma",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSSP3P0",
            "word" : "sean",
            "negated" : True
        }, 
        {
            "lemma" : "comprar",
            "tag" : "VMP00PM",
            "word" : "comprados",
            "negated" : True
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : True
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : True
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : True
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "bf86598543e3facabdf7177541b8d040",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "increíble",
            "tag" : "AQ0CS00",
            "word" : "increíble",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : True
        }, 
        {
            "lemma" : "dejar",
            "tag" : "VMN0000",
            "word" : "dejar",
            "negated" : True
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : True
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "extremadamente",
            "tag" : "RG",
            "word" : "extremadamente",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "etapa",
            "tag" : "NCFS000",
            "word" : "etapa",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "desafío",
            "tag" : "NCMS000",
            "word" : "desafío",
            "negated" : False
        }, 
        {
            "lemma" : "diferente",
            "tag" : "AQ0CS00",
            "word" : "diferente",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : True
        }, 
        {
            "lemma" : "aburrar",
            "tag" : "VMIP1S0",
            "word" : "aburro",
            "negated" : False
        }, 
        {
            "lemma" : "nunca",
            "tag" : "RG",
            "word" : "nunca",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "8eacb5665ff56f33efc5cb1c3cd1aa08",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "cuando",
            "tag" : "CS",
            "word" : "cuando",
            "negated" : False
        }, 
        {
            "lemma" : "papar",
            "tag" : "VMIP3S0",
            "word" : "papa",
            "negated" : False
        }, 
        {
            "lemma" : "petar",
            "tag" : "VMN0000",
            "word" : "petar",
            "negated" : False
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFS000",
            "word" : "saga",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "deber",
            "tag" : "VMIC3P0",
            "word" : "deberían",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMN0000",
            "word" : "hacer",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "tienda",
            "tag" : "NCFS000",
            "word" : "tienda",
            "negated" : False
        }, 
        {
            "lemma" : "donde",
            "tag" : "PR00000",
            "word" : "donde",
            "negated" : False
        }, 
        {
            "lemma" : "canje",
            "tag" : "NCMP000",
            "word" : "canjes",
            "negated" : False
        }, 
        {
            "lemma" : "punto",
            "tag" : "NCMP000",
            "word" : "puntos",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "ejemplo",
            "tag" : "NCMS000",
            "word" : "ejemplo",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "0",
            "tag" : "NCMS000",
            "word" : "0",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "0",
            "tag" : "NCMS000",
            "word" : "0",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "punto",
            "tag" : "NCMP000",
            "word" : "puntos",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "cambiar",
            "tag" : "VMSP2S0",
            "word" : "cambies",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "bomba",
            "tag" : "NCFS000",
            "word" : "bomba",
            "negated" : True
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : True
        }, 
        {
            "lemma" : "color",
            "tag" : "NCMS000",
            "word" : "color",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "a19cf9beda0cb845dd206449df402a03",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "fabuloso",
            "tag" : "AQ0MS00",
            "word" : "fabuloso",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "valorar",
            "tag" : "VMP00SM",
            "word" : "valorado",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "sorpresa",
            "tag" : "NCFP000",
            "word" : "sorpresas",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "encontrar",
            "tag" : "VMIP2S0",
            "word" : "encontrás",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "PI0MS00",
            "word" : "uno",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "episodio",
            "tag" : "NCMP000",
            "word" : "episodios",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "recomendar",
            "tag" : "VMIP1S0",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "28bb6973d56e0cb38189fa80cf9b2541",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "precaución",
            "tag" : "NCFS000",
            "word" : "precaución",
            "negated" : False
        }, 
        {
            "lemma" : ":",
            "tag" : "Fd",
            "word" : ":",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "básico",
            "tag" : "AQ0MS00",
            "word" : "básico",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "hasta",
            "tag" : "SP",
            "word" : "hasta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "momento",
            "tag" : "NCMS000",
            "word" : "momento",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : False
        }, 
        {
            "lemma" : "4",
            "tag" : "AQ0CS00",
            "word" : "4",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VAIP1S0",
            "word" : "he",
            "negated" : True
        }, 
        {
            "lemma" : "sufrir",
            "tag" : "VMP00SM",
            "word" : "sufrido",
            "negated" : True
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : True
        }, 
        {
            "lemma" : "cierre",
            "tag" : "NCMP000",
            "word" : "cierres",
            "negated" : True
        }, 
        {
            "lemma" : "abrupto",
            "tag" : "AQ0MP00",
            "word" : "abruptos",
            "negated" : True
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : True
        }, 
        {
            "lemma" : "reportar",
            "tag" : "VMIP3P0",
            "word" : "reportan",
            "negated" : True
        }, 
        {
            "lemma" : "otro",
            "tag" : "DI0MP0",
            "word" : "otros",
            "negated" : True
        }, 
        {
            "lemma" : "usuario",
            "tag" : "NCMP000",
            "word" : "usuarios",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "b064eb40c7e4ed36637d615c172326b1",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP3S0",
            "word" : "tiene",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "DI0MP0",
            "word" : "muchos",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMP000",
            "word" : "niveles",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "etapa",
            "tag" : "NCFP000",
            "word" : "etapas",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFS000",
            "word" : "vez",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VMIP3S0",
            "word" : "hay",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "cosa",
            "tag" : "NCFP000",
            "word" : "cosas",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CPD0",
            "word" : "les",
            "negated" : False
        }, 
        {
            "lemma" : "sugerir",
            "tag" : "VMIP1S0",
            "word" : "sugiero",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "descargar",
            "tag" : "VMSP3P0",
            "word" : "descarguen",
            "negated" : True
        }, 
        {
            "lemma" : "amojar",
            "tag" : "VMM02S0",
            "word" : "amoja",
            "negated" : True
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3FSA0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "094fd0013bd7f24eaa8868435a9af04d",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "bueno",
            "tag" : "I",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "entender",
            "tag" : "VMP00SM",
            "word" : "entendido",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "amar",
            "tag" : "VMSP3S0",
            "word" : "ame",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "pasar",
            "tag" : "VMN0000",
            "word" : "pasar",
            "negated" : False
        }, 
        {
            "lemma" : "bien",
            "tag" : "RG",
            "word" : "bien",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "pez",
            "tag" : "NCCS000",
            "word" : "pez",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "relajar",
            "tag" : "VMN0000",
            "word" : "relajar",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "mente",
            "tag" : "NCFS000",
            "word" : "mente",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "poco",
            "tag" : "PI0MS00",
            "word" : "poco",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ónice",
            "tag" : "NCMS000",
            "word" : "ónice",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "fb15c4a84400e0d9c0dea151427daf9a",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "samsung",
            "tag" : "NCMS000",
            "word" : "samsung",
            "negated" : False
        }, 
        {
            "lemma" : "galaxy",
            "tag" : "RG",
            "word" : "galaxy",
            "negated" : False
        }, 
        {
            "lemma" : "segundo",
            "tag" : "NCMN000",
            "word" : "s",
            "negated" : False
        }, 
        {
            "lemma" : "avance",
            "tag" : "NCMS000",
            "word" : "avance",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "cual",
            "tag" : "PR0CS00",
            "word" : "cual",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP2S0",
            "word" : "puedes",
            "negated" : False
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMN0000",
            "word" : "hacer",
            "negated" : False
        }, 
        {
            "lemma" : "funcionar",
            "tag" : "VMN0000",
            "word" : "funcionar",
            "negated" : False
        }, 
        {
            "lemma" : "tu",
            "tag" : "DP2CSS",
            "word" : "tu",
            "negated" : False
        }, 
        {
            "lemma" : "mente",
            "tag" : "NCFS000",
            "word" : "mente",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "creer",
            "tag" : "VMIP1S0",
            "word" : "creo",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "PI0MP00",
            "word" : "todos",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "devenir",
            "tag" : "VMII3P0",
            "word" : "devenían",
            "negated" : False
        }, 
        {
            "lemma" : "instalar",
            "tag" : "VMN0000",
            "word" : "instalar",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "menos",
            "tag" : "RG",
            "word" : "menos",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "encontrar",
            "tag" : "VMIP1S0",
            "word" : "encuentro",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "calificar",
            "tag" : "VMIS3S0",
            "word" : "calificó",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FP0",
            "word" : "las",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "sugerencia",
            "tag" : "NCFP000",
            "word" : "sugerencias",
            "negated" : False
        }, 
        {
            "lemma" : ":",
            "tag" : "Fd",
            "word" : ":",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "PI0MS00",
            "word" : "todo",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSSP1S0",
            "word" : "sea",
            "negated" : False
        }, 
        {
            "lemma" : "gratuito",
            "tag" : "AQ0MS00",
            "word" : "gratuito",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "ir",
            "tag" : "VMIP1P0",
            "word" : "vamos",
            "negated" : False
        }, 
        {
            "lemma" : "ganar",
            "tag" : "VMG0000",
            "word" : "ganando",
            "negated" : True
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : True
        }, 
        {
            "lemma" : "través",
            "tag" : "NCMS000",
            "word" : "través",
            "negated" : True
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : True
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : True
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "31953841c1a4bf7a4527cf7a7a256774",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "enganchar",
            "tag" : "VMIP3S0",
            "word" : "engancha",
            "negated" : False
        }, 
        {
            "lemma" : "mogollón",
            "tag" : "NCMS000",
            "word" : "mogollón",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP1S0",
            "word" : "soy",
            "negated" : False
        }, 
        {
            "lemma" : "fan",
            "tag" : "NCCS000",
            "word" : "fan",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "aunque",
            "tag" : "CC",
            "word" : "aunque",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFP000",
            "word" : "veces",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "alguno",
            "tag" : "DI0MS0",
            "word" : "algún",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "otro",
            "tag" : "PI0MS00",
            "word" : "otro",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "desquiciar",
            "tag" : "VMIP3S0",
            "word" : "desquicia",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "desistir",
            "tag" : "VMIP1S0",
            "word" : "desisto",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "conseguir",
            "tag" : "VMIF1S0",
            "word" : "conseguiré",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "49e600f8648595e38f0676eaff916c83",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "jergón",
            "tag" : "NCMP000",
            "word" : "jergones",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "vez",
            "tag" : "NCFS000",
            "word" : "vez",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "mas",
            "tag" : "CC",
            "word" : "mas",
            "negated" : False
        }, 
        {
            "lemma" : "cefala",
            "tag" : "VMIP3S0",
            "word" : "cefala",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "privar",
            "tag" : "VMM02S0",
            "word" : "privá",
            "negated" : False
        }, 
        {
            "lemma" : "tela",
            "tag" : "NCFS000",
            "word" : "tela",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "aconsejar",
            "tag" : "VMIP1S0",
            "word" : "aconsejo",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : True
        }, 
        {
            "lemma" : "1",
            "tag" : "NCMS000",
            "word" : "1",
            "negated" : True
        }, 
        {
            "lemma" : "0",
            "tag" : "AQ0CS00",
            "word" : "0",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "2a325044641c08b9c31aea82fe1b7927",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "entretenido",
            "tag" : "NCMS000",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "resultar",
            "tag" : "VMIP3S0",
            "word" : "resulta",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSN0000",
            "word" : "ser",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "desafío",
            "tag" : "NCMS000",
            "word" : "desafío",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "alguno",
            "tag" : "DI0FP0",
            "word" : "algunas",
            "negated" : False
        }, 
        {
            "lemma" : "ocasión",
            "tag" : "NCFP000",
            "word" : "ocasiones",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMSP3S0",
            "word" : "tenga",
            "negated" : False
        }, 
        {
            "lemma" : "limitar",
            "tag" : "VMSP2S0",
            "word" : "limites",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "vida",
            "tag" : "NCFP000",
            "word" : "vidas",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "contrario",
            "tag" : "NCMS000",
            "word" : "contrario",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "pasar",
            "tag" : "VMIC2S0",
            "word" : "pasarías",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "día",
            "tag" : "NCMS000",
            "word" : "día",
            "negated" : False
        }, 
        {
            "lemma" : "enterar",
            "tag" : "VMIP1S0",
            "word" : "entero",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMG0000",
            "word" : "jugando",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "f71c53bfded7e4f50dbb834d18bfcd0d",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VAII3P0",
            "word" : "habían",
            "negated" : False
        }, 
        {
            "lemma" : "comentar",
            "tag" : "VMP00SM",
            "word" : "comentado",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "cual",
            "tag" : "PR0CS00",
            "word" : "cual",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "interesar",
            "tag" : "VMIP1S0",
            "word" : "intereso",
            "negated" : False
        }, 
        {
            "lemma" : "ya",
            "tag" : "RG",
            "word" : "ya",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP1S0",
            "word" : "soy",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "fan",
            "tag" : "NCCS000",
            "word" : "fan",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "bejeweld",
            "tag" : "NP00000",
            "word" : "bejeweld",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "retar",
            "tag" : "VMIP3S0",
            "word" : "reta",
            "negated" : False
        }, 
        {
            "lemma" : "por",
            "tag" : "SP",
            "word" : "por",
            "negated" : False
        }, 
        {
            "lemma" : "cada",
            "tag" : "DI0CS0",
            "word" : "cada",
            "negated" : False
        }, 
        {
            "lemma" : "avance",
            "tag" : "NCMS000",
            "word" : "avance",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "llevar",
            "tag" : "VMSP2S0",
            "word" : "lleves",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "sonido",
            "tag" : "NCMS000",
            "word" : "sonido",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "agradable",
            "tag" : "AQ0CP00",
            "word" : "agradables",
            "negated" : False
        }, 
        {
            "lemma" : "gráfico",
            "tag" : "AQ0MP00",
            "word" : "gráficos",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "altamente",
            "tag" : "RG",
            "word" : "altamente",
            "negated" : True
        }, 
        {
            "lemma" : "recomendable",
            "tag" : "AQ0CS00",
            "word" : "recomendable",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "7b3cf0474df84965fb16049c548dbe92",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "buenísimo",
            "tag" : "RG",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQSMS00",
            "word" : "buenísimo",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "últimamente",
            "tag" : "RG",
            "word" : "últimamente",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VAIP1S0",
            "word" : "he",
            "negated" : True
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMP00SM",
            "word" : "podido",
            "negated" : True
        }, 
        {
            "lemma" : "abrir",
            "tag" : "VMN0000",
            "word" : "abrir",
            "negated" : True
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP3S0",
            "word" : "da",
            "negated" : False
        }, 
        {
            "lemma" : "forzar",
            "tag" : "VMN0000",
            "word" : "forzar",
            "negated" : False
        }, 
        {
            "lemma" : "cierre",
            "tag" : "NCMS000",
            "word" : "cierre",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "ya",
            "tag" : "RG",
            "word" : "ya",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : True
        }, 
        {
            "lemma" : "seguir",
            "tag" : "VMN0000",
            "word" : "seguir",
            "negated" : True
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMG0000",
            "word" : "jugando",
            "negated" : True
        }, 
        {
            "lemma" : "arreglar",
            "tag" : "VMM03P0",
            "word" : "arreglen",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "porfiar",
            "tag" : "VMM02S0",
            "word" : "porfiá",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "arreglar",
            "tag" : "VMSP3P0",
            "word" : "arreglen",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "21cf865cba991853efc6bdb9a44a334f",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "espectacular",
            "tag" : "AQ0CS00",
            "word" : "espectacular",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "además",
            "tag" : "RG",
            "word" : "además",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "celular",
            "tag" : "AQ0CS00",
            "word" : "celular",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "conectar",
            "tag" : "VMIP2S0",
            "word" : "conectas",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : "asi",
            "tag" : "NCMS000",
            "word" : "asi",
            "negated" : False
        }, 
        {
            "lemma" : "te",
            "tag" : "PP2CS00",
            "word" : "te",
            "negated" : False
        }, 
        {
            "lemma" : "ayudar",
            "tag" : "VMIP3P0",
            "word" : "ayudan",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MP0",
            "word" : "los",
            "negated" : False
        }, 
        {
            "lemma" : "amigo",
            "tag" : "NCMP000",
            "word" : "amigos",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "podar",
            "tag" : "VMSP2S0",
            "word" : "podes",
            "negated" : False
        }, 
        {
            "lemma" : "usar",
            "tag" : "VMN0000",
            "word" : "usar",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "o",
            "tag" : "CC",
            "word" : "o",
            "negated" : False
        }, 
        {
            "lemma" : "sin",
            "tag" : "SP",
            "word" : "sin",
            "negated" : False
        }, 
        {
            "lemma" : "conexión",
            "tag" : "NCFS000",
            "word" : "conexión",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "único",
            "tag" : "AQ0MS00",
            "word" : "único",
            "negated" : False
        }, 
        {
            "lemma" : "malo",
            "tag" : "NCMS000",
            "word" : "malo",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMIP3S0",
            "word" : "tiene",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "celular",
            "tag" : "AQ0CS00",
            "word" : "celular",
            "negated" : False
        }, 
        {
            "lemma" : "andar",
            "tag" : "VMIP3S0",
            "word" : "anda",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "poco",
            "tag" : "RG",
            "word" : "poco",
            "negated" : False
        }, 
        {
            "lemma" : "lento",
            "tag" : "AQ0MS00",
            "word" : "lento",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "abbe765d3b35a88f0877fd506cf90bad",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "aunque",
            "tag" : "CC",
            "word" : "aunque",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "androide",
            "tag" : "NCMS000",
            "word" : "androide",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "conectar",
            "tag" : "VMIP3S0",
            "word" : "conecta",
            "negated" : True
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : True
        }, 
        {
            "lemma" : "facebook",
            "tag" : "NC00000",
            "word" : "facebook",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "sin",
            "tag" : "SP",
            "word" : "sin",
            "negated" : False
        }, 
        {
            "lemma" : "embargo",
            "tag" : "NCMS000",
            "word" : "embargo",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "facebook",
            "tag" : "NC00000",
            "word" : "facebook",
            "negated" : False
        }, 
        {
            "lemma" : "sí",
            "tag" : "RG",
            "word" : "sí",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "aparecer",
            "tag" : "VMIP3S0",
            "word" : "aparece",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "lista",
            "tag" : "NCFS000",
            "word" : "lista",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "aplicación",
            "tag" : "NCFP000",
            "word" : "aplicaciones",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "caso",
            "tag" : "NCMS000",
            "word" : "caso",
            "negated" : False
        }, 
        {
            "lemma" : "misterioso",
            "tag" : "AQ0MS00",
            "word" : "misterioso",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "quien",
            "tag" : "PR0CS00",
            "word" : "quien",
            "negated" : False
        }, 
        {
            "lemma" : "querer",
            "tag" : "VMSP3S0",
            "word" : "quiera",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "buen",
            "negated" : False
        }, 
        {
            "lemma" : "rato",
            "tag" : "NCMS000",
            "word" : "rato",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "ocio",
            "tag" : "NCMS000",
            "word" : "ocio",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "gustar",
            "tag" : "VMSP3S0",
            "word" : "guste",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMP000",
            "word" : "juegos",
            "negated" : False
        }, 
        {
            "lemma" : "tipo",
            "tag" : "NCMS000",
            "word" : "tipo",
            "negated" : False
        }, 
        {
            "lemma" : "pulir",
            "tag" : "VMIP2S0",
            "word" : "pules",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "simplemente",
            "tag" : "RG",
            "word" : "simplemente",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "7b8af6b063cc391ae6cdac544ea41440",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "superar",
            "tag" : "VMN0000",
            "word" : "superar",
            "negated" : False
        }, 
        {
            "lemma" : "genial",
            "tag" : "AQ0CS00",
            "word" : "genial",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0MS0",
            "word" : "este",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "muy",
            "tag" : "RG",
            "word" : "muy",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "para",
            "tag" : "SP",
            "word" : "para",
            "negated" : False
        }, 
        {
            "lemma" : "poner",
            "tag" : "VMN0000",
            "word" : "poner",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "cerebro",
            "tag" : "NCMS000",
            "word" : "cerebro",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "pensar",
            "tag" : "VMN0000",
            "word" : "pensar",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA00S0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "recomer",
            "tag" : "VMG0000",
            "word" : "recomiendo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "amojar",
            "tag" : "VMM02S0",
            "word" : "amoja",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3FSA0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP1S0",
            "word" : "doy",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "8f83e52959b8ebb4aef0157c5926d5fc",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "bueno",
            "tag" : "AQ0MS00",
            "word" : "bueno",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "entretener",
            "tag" : "VMP00SM",
            "word" : "entretenido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "gracia",
            "tag" : "NCFP000",
            "word" : "gracias",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "inventar",
            "tag" : "VMIP1S0",
            "word" : "invento",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : False
        }, 
        {
            "lemma" : "compartir",
            "tag" : "VMIS3S0",
            "word" : "compartió",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "todo",
            "tag" : "DI0MP0",
            "word" : "todos",
            "negated" : False
        }, 
        {
            "lemma" : "nosotros",
            "tag" : "PP1MP00",
            "word" : "nosotros",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "ahora",
            "tag" : "RG",
            "word" : "ahora",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "lo",
            "tag" : "PP3MSA0",
            "word" : "lo",
            "negated" : True
        }, 
        {
            "lemma" : "poder",
            "tag" : "VMIP1S0",
            "word" : "puedo",
            "negated" : True
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMN0000",
            "word" : "jugar",
            "negated" : True
        }, 
        {
            "lemma" : "pero",
            "tag" : "CC",
            "word" : "pero",
            "negated" : False
        }, 
        {
            "lemma" : "esperar",
            "tag" : "VMIP1S0",
            "word" : "espero",
            "negated" : False
        }, 
        {
            "lemma" : "pronto",
            "tag" : "RG",
            "word" : "pronto",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "volver",
            "tag" : "VMSP3P0",
            "word" : "vuelvan",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMN0000",
            "word" : "dar",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "oportunidad",
            "tag" : "NCFS000",
            "word" : "oportunidad",
            "negated" : False
        }, 
        {
            "lemma" : "aqui",
            "tag" : "VMIS1S0",
            "word" : "aqui",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "ayudar",
            "tag" : "VMIP3S0",
            "word" : "ayuda",
            "negated" : False
        }, 
        {
            "lemma" : "mucho",
            "tag" : "RG",
            "word" : "mucho",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : True
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : True
        }, 
        {
            "lemma" : "extraer",
            "tag" : "VMIP2S0",
            "word" : "extraés",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "823df6a049d5ff4d2b8fea4d31a319f1",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "fantástico",
            "tag" : "AQ0MS00",
            "word" : "fantástico",
            "negated" : False
        }, 
        {
            "lemma" : "juego",
            "tag" : "NCMS000",
            "word" : "juego",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSII3S0",
            "word" : "era",
            "negated" : False
        }, 
        {
            "lemma" : "hora",
            "tag" : "NCFS000",
            "word" : "hora",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "tener",
            "tag" : "VMSI1P0",
            "word" : "tuviéramos",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : False
        }, 
        {
            "lemma" : "poco",
            "tag" : "PI0MS00",
            "word" : "poco",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "entretenimiento",
            "tag" : "NCMS000",
            "word" : "entretenimiento",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMN0000",
            "word" : "dar",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0FS0",
            "word" : "una",
            "negated" : False
        }, 
        {
            "lemma" : "nuevo",
            "tag" : "AQ0FS00",
            "word" : "nueva",
            "negated" : False
        }, 
        {
            "lemma" : "dinámica",
            "tag" : "NCFS000",
            "word" : "dinámica",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "acebo",
            "tag" : "NCMS000",
            "word" : "acebo",
            "negated" : False
        }, 
        {
            "lemma" : "creer",
            "tag" : "VMIP1S0",
            "word" : "creo",
            "negated" : False
        }, 
        {
            "lemma" : "q",
            "tag" : "NCFN000",
            "word" : "q",
            "negated" : False
        }, 
        {
            "lemma" : "candy",
            "tag" : "NCMS000",
            "word" : "candy",
            "negated" : False
        }, 
        {
            "lemma" : "curar",
            "tag" : "VMIP2S0",
            "word" : "curás",
            "negated" : False
        }, 
        {
            "lemma" : "saga",
            "tag" : "NCFS000",
            "word" : "saga",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "cumplir",
            "tag" : "VMP00SM",
            "word" : "cumplido",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "DD0MS0",
            "word" : "ese",
            "negated" : False
        }, 
        {
            "lemma" : "requerimiento",
            "tag" : "NCMS000",
            "word" : "requerimiento",
            "negated" : False
        }, 
        {
            "lemma" : "x",
            "tag" : "NCFS000",
            "word" : "x",
            "negated" : False
        }, 
        {
            "lemma" : "ese",
            "tag" : "PD00S00",
            "word" : "eso",
            "negated" : False
        }, 
        {
            "lemma" : "yo",
            "tag" : "PP1CSN0",
            "word" : "yo",
            "negated" : False
        }, 
        {
            "lemma" : "le",
            "tag" : "PP3CSD0",
            "word" : "le",
            "negated" : False
        }, 
        {
            "lemma" : "dar",
            "tag" : "VMIP1S0",
            "word" : "doy",
            "negated" : False
        }, 
        {
            "lemma" : "cincar",
            "tag" : "VMIP1S0",
            "word" : "cinco",
            "negated" : False
        }, 
        {
            "lemma" : "estrella",
            "tag" : "NCFP000",
            "word" : "estrellas",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "eab2fd5638493a73de8e38cd577ea861",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "social",
            "tag" : "AQ0CS00",
            "word" : "social",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "divertir",
            "tag" : "VMP00SM",
            "word" : "divertido",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0MS00",
            "word" : "adictivo",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ir",
            "tag" : "VMIP1S0",
            "word" : "voy",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "nivel",
            "tag" : "NCMS000",
            "word" : "nivel",
            "negated" : False
        }, 
        {
            "lemma" : "5",
            "tag" : "NCFS000",
            "word" : "5",
            "negated" : False
        }, 
        {
            "lemma" : "0",
            "tag" : "AQ0CS00",
            "word" : "0",
            "negated" : False
        }, 
        {
            "lemma" : "y",
            "tag" : "CC",
            "word" : "y",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "haber",
            "tag" : "VAIP1S0",
            "word" : "he",
            "negated" : True
        }, 
        {
            "lemma" : "comprar",
            "tag" : "VMP00SM",
            "word" : "comprado",
            "negated" : True
        }, 
        {
            "lemma" : "uno",
            "tag" : "DI0MS0",
            "word" : "un",
            "negated" : True
        }, 
        {
            "lemma" : "sólo",
            "tag" : "RG",
            "word" : "sólo",
            "negated" : True
        }, 
        {
            "lemma" : "bono",
            "tag" : "NCMP000",
            "word" : "bonos",
            "negated" : True
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "clave",
            "tag" : "NCFS000",
            "word" : "clave",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "CS",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "jugar",
            "tag" : "VMSP2S0",
            "word" : "juegues",
            "negated" : False
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : False
        }, 
        {
            "lemma" : "otro",
            "tag" : "DI0FP0",
            "word" : "otras",
            "negated" : False
        }, 
        {
            "lemma" : "persona",
            "tag" : "NCFP000",
            "word" : "personas",
            "negated" : False
        }, 
        {
            "lemma" : "tan",
            "tag" : "RG",
            "word" : "tan",
            "negated" : False
        }, 
        {
            "lemma" : "obstinar",
            "tag" : "VMP00PF",
            "word" : "obstinadas",
            "negated" : True
        }, 
        {
            "lemma" : "con",
            "tag" : "SP",
            "word" : "con",
            "negated" : True
        }, 
        {
            "lemma" : "tu",
            "tag" : "DP2CSS",
            "word" : "tu",
            "negated" : True
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
},{
    "_id" : "573c39fc20bebf81dabfb91a730c4271",
    "category" : 80,
    "source" : "corpus_apps_android",
    "text" : [ 
        {
            "lemma" : "el",
            "tag" : "DA0FS0",
            "word" : "la",
            "negated" : False
        }, 
        {
            "lemma" : "mejor",
            "tag" : "AQ0CS00",
            "word" : "mejor",
            "negated" : False
        }, 
        {
            "lemma" : "ap",
            "tag" : "NCFS000",
            "word" : "ap",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "conocer",
            "tag" : "VMIP1S0",
            "word" : "conozco",
            "negated" : False
        }, 
        {
            "lemma" : "hasta",
            "tag" : "SP",
            "word" : "hasta",
            "negated" : False
        }, 
        {
            "lemma" : "el",
            "tag" : "DA0MS0",
            "word" : "el",
            "negated" : False
        }, 
        {
            "lemma" : "momento",
            "tag" : "NCMS000",
            "word" : "momento",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "me",
            "tag" : "PP1CS00",
            "word" : "me",
            "negated" : False
        }, 
        {
            "lemma" : "encantar",
            "tag" : "VMIP3S0",
            "word" : "encanta",
            "negated" : False
        }, 
        {
            "lemma" : "este",
            "tag" : "DD0FS0",
            "word" : "esta",
            "negated" : False
        }, 
        {
            "lemma" : "aplicación",
            "tag" : "NCFS000",
            "word" : "aplicación",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "ser",
            "tag" : "VSIP3S0",
            "word" : "es",
            "negated" : False
        }, 
        {
            "lemma" : "super",
            "tag" : "AQ0CN00",
            "word" : "super",
            "negated" : False
        }, 
        {
            "lemma" : "adictivo",
            "tag" : "AQ0FS00",
            "word" : "adictiva",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "a",
            "tag" : "SP",
            "word" : "a",
            "negated" : False
        }, 
        {
            "lemma" : "pesar",
            "tag" : "VMN0000",
            "word" : "pesar",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "que",
            "tag" : "PR0CN00",
            "word" : "que",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : False
        }, 
        {
            "lemma" : "basar",
            "tag" : "VMIP3S0",
            "word" : "basa",
            "negated" : False
        }, 
        {
            "lemma" : "en",
            "tag" : "SP",
            "word" : "en",
            "negated" : False
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMN0000",
            "word" : "hacer",
            "negated" : False
        }, 
        {
            "lemma" : "combinación",
            "tag" : "NCFP000",
            "word" : "combinaciones",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "caramelo",
            "tag" : "NCMP000",
            "word" : "caramelos",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "color",
            "tag" : "NCMP000",
            "word" : "colores",
            "negated" : False
        }, 
        {
            "lemma" : ",",
            "tag" : "Fc",
            "word" : ",",
            "negated" : False
        }, 
        {
            "lemma" : "no",
            "tag" : "RN",
            "word" : "no",
            "negated" : False
        }, 
        {
            "lemma" : "se",
            "tag" : "P00CN00",
            "word" : "se",
            "negated" : True
        }, 
        {
            "lemma" : "hacer",
            "tag" : "VMIP3S0",
            "word" : "hace",
            "negated" : True
        }, 
        {
            "lemma" : "nada",
            "tag" : "PI0CS00",
            "word" : "nada",
            "negated" : False
        }, 
        {
            "lemma" : "repetitivo",
            "tag" : "AQ0FS00",
            "word" : "repetitiva",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "bajo",
            "tag" : "SP",
            "word" : "bajo",
            "negated" : False
        }, 
        {
            "lemma" : "mi",
            "tag" : "DP1CSS",
            "word" : "mi",
            "negated" : False
        }, 
        {
            "lemma" : "punto",
            "tag" : "NCMS000",
            "word" : "punto",
            "negated" : False
        }, 
        {
            "lemma" : "de",
            "tag" : "SP",
            "word" : "de",
            "negated" : False
        }, 
        {
            "lemma" : "vista",
            "tag" : "NCFS000",
            "word" : "vista",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "excelente",
            "tag" : "AQ0CS00",
            "word" : "excelente",
            "negated" : False
        }, 
        {
            "lemma" : "aplicación",
            "tag" : "NCFS000",
            "word" : "aplicación",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : "enhorabuena",
            "tag" : "RG",
            "word" : "enhorabuena",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }, 
        {
            "lemma" : ".",
            "tag" : "Fp",
            "word" : ".",
            "negated" : False
        }
    ],
    "tagged" : "automatically"
    }]

score = evaluate({
    "decepción": {
        "inf": 1.08, 
        "val": -0.0004
    }, 
    "dar": {
        "inf": 1.9, 
        "val": 0.08924
    }
}, corpus)


print 'OK   '



# pos = dp.get_opinions( cat_cond={"$gt":50} )
# neg = dp.get_opinions( cat_cond={"$lt":50} )
# lemmas = dp.get_lemmas()

# li = load('./indeplex/indeplex_by_senti_tfidf_top150.json')

# opinions = dp.get_opinions( source='corpus_apps_android' )

# graph = MultiGraph( opinions, 'corpus_apps_android', filter_tags=USEFUL_TAGS )

# ld = by_influence( graph, li, limit=2000)

# graph.to_vis(ld,tofile="./visgraph")

