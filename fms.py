import argparse
from utilities import *

parser = argparse.ArgumentParser(description='Provides FMS of strings S and S1')
parser.add_argument('S', help='First Sentence')
parser.add_argument('S1', help='Second Sentence')
args = parser.parse_args()

#Applying some preprocessing on input data.
s_sentence = preprocess(args.S)
s1_sentence = preprocess(args.S1)

#Testing Input data
assertion(s_sentence != "", "S should be there.\nSee -h for help")
assertion(s1_sentence != "", "S1 should be there.\nSee -h for help")

(larger, smaller) = (s_sentence, s1_sentence) if len(s_sentence) > len(s1_sentence) \
					else (s1_sentence, s_sentence)
ll, sl = larger.split(), smaller.split()

#Find Cost Distance
cost = 0.0
for word in sl:
	if word not in ll:
		cost += 1

fms = 1.0 - (cost/len(ll))

print ('%.02f' %(fms*100))