import argparse
from lib.utilities import preprocess, assertion
from lib.fms import FMS
from lib.phrase_extractor import PhraseExtractor

parser = argparse.ArgumentParser(description='Generates set A.')
parser.add_argument('S', help='First Sentence')
parser.add_argument('S1', help='Second Sentence')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.')
args = parser.parse_args()

#Applying some preprocessing on input data.
s_sentence = preprocess(args.S)
s1_sentence = preprocess(args.S1)

#Testing Input data
assertion(s_sentence != "", "S should not be blank.\nSee -h for help")
assertion(s1_sentence != "", "S1 should not be blank.\nSee -h for help")

min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) if args.max_len else max(len(s_sentence.split()), len(s1_sentence.split()))

fms = FMS(s_sentence, s1_sentence).calculate()

assertion(fms >= min_fms, "Sentences have low fuzzy match score of %.02f." %fms)

phrase_extractor = PhraseExtractor(s_sentence, s1_sentence, min_len, max_len)
a_set = phrase_extractor.extract_pairs()

# print set A
S = s_sentence.split()
S1 = s1_sentence.split()

for a,b,c,d in a_set:
	str1 = ' '.join(S[a: b+1])
	str2 = ' '.join(S1[c: d+1])
	print('("{0}", "{1}")'.format(str1, str2))
