import pylab
import argparse
import pylab  as plb
import os.path, sys, re
from lib.fms import FMS
from lib.utilities import assertion
from lib.ap import Apertium
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Regression test for repair.py')
parser.add_argument('D', help='Corpus directory.')

parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.', default='5')
args = parser.parse_args()

#Preprocessing
path = args.D
assertion(os.path.isdir(path), "Directory not found.")

#Command line params
lp_dir = args.d
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) 

all_files = os.listdir(path)
files_map = {}
test_sentences = 0
fmses = []

for file1 in all_files:
	match = re.match(r'[a-z]{2}\.[a-z]{2}\-[a-z]{2}\.(test|train)', file1)
	if match:
		print(file1)
		src_sentences = []
		f1 = open(path+'/'+file1)
		while True:
			line = preprocess(f1.readline())
			if not line:
				break
			if line == '':
				continue
			src_sentences.append(line)

		sys.setrecursionlimit(10000)

		for i in range(len(src_sentences)):
			for j in range(i+1, len(src_sentences)):
				s, s1 = src_sentences[i], src_sentences[j]
				fms = FMS(s, s1).calculate_using_wanger_fischer()
				fmses.append(fms)
		break

pylab.hist(fmses, 100)

pylab.show()
