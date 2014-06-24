import argparse
import os.path
from lib.utilities import assertion

parser = argparse.ArgumentParser(description='Regression test for repair.py')
parser.add_argument('F', help='First file')
parser.add_argument('F1', help='Second file')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.')
args = parser.parse_args()

assertion(os.path.isfile(args.F), "File 1 not found.")
assertion(os.path.isfile(args.F1), "File 2 not found.")

file1 = open(args.F)
file2 = open(args.F1)

src_sentences, tgt_sentences = [],[]

while True:
	
