import argparse
import os.path
from lib.fms import FMS
from lib.utilities import assertion

parser = argparse.ArgumentParser(description='Regression test for repair.py')
parser.add_argument('F', help='First file')
parser.add_argument('F1', help='Second file')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.', default='5')
args = parser.parse_args()

#Command line params
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) 

#Some checks
assertion(os.path.isfile(args.F), "File 1 not found.")
assertion(os.path.isfile(args.F1), "File 2 not found.")

file1 = open(args.F)
file2 = open(args.F1)

src_sentences, tgt_sentences = [],[]

while True:
	line = file1.readline()
	line2 = file2.readline()
	if not line:
		break
	src_sentences.append(line)
	tgt_sentences.append(line2)

assertion(len(src_sentences) == len(tgt_sentences), "Files are of different sizes.")

fms_map = {}
for s in src_sentences:
	for s1 in src_sentences:
		if s != s1:
			# print(s,s1)
			fms = FMS(s, s1).calculate()
			if fms >= min_fms:
				i,j = src_sentences.index(s), src_sentences.index(s1)
				fms_map[(s,s1)] = (tgt_sentences[i], tgt_sentences[j])

print(fms_map)
