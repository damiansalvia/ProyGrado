
import xml.etree.ElementTree as xmlreader
import glob

from printHelper import *
from utils import *

inputdir  =  'corpus/corpus_cine/corpus_test/'
outputdir =  'apps/dictionaries/'
logdir    =  'apps/log/'

magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
            <!ENTITY nbsp ' '>
            ]>''' 

summarize = False

def extract(xml):
    # extract the information from the file (film - text - rank )
    return xml.get("title"), xml.find("summary" if summarize else "body").text, int(xml.get("rank"))

log = Log(logdir)
files = glob.glob(inputdir + '*.xml')
total = len(files)

reviews = []

for idx, file in enumerate(files):
    with open(file) as xml_file:
        data = xml_file.read().decode('cp1252').encode('utf8')
        try:
            xml = xmlreader.fromstring(magic + data)
        except Exception as e:
            log("error con el archivo: " + file + " " + str(e), 'warning' )
            continue
        if is_valid_file(data):
            film, text, rank, = extract(xml)
            reviews.append({'subject': film, 'review': text, 'rank':rank })
    progressive_bar("Reading files:     ", total, idx)
sys.stdout.write('\n')
sys.stdout.flush()

with codecs.open(outputdir + "reviews.json", "w", "utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False)

print '\nFIN'

