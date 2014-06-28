import pylab
import argparse
import os.path, sys, re
import pylab  as plb
from lib.fms import FMS
from lib.utilities import assertion
from lib.ap import Apertium
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch


parser = argparse.ArgumentParser(description='Calculate the distribution of FMS between pair of sentences.')
parser.add_argument('F', help='Corpus path.')

parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
args = parser.parse_args()

#Preprocessing
file1 = args.F
assertion(os.path.isfile(file1), "Corpus not found.")

#Command line params
min_fms = float(args.min_fms)

fmses = []
src_sentences = []
f1 = open(file1)

while True:
	line = preprocess(f1.readline())
	if not line:
		break
	if line == '':
		continue
	src_sentences.append(line)

for i in range(len(src_sentences)):
	for j in range(i+1, len(src_sentences)):
		s, s1 = src_sentences[i], src_sentences[j]
		fms = FMS(s, s1).calculate_using_wanger_fischer()
		fmses.append(fms)
		
pylab.hist(fmses, 100)

pylab.show()
