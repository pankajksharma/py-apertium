import argparse
from lib.fms import FMS
from lib.ap import Apertium
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, is_subsegment

parser = argparse.ArgumentParser(description='Generates set D.')
parser.add_argument('S', help='Second Sentence')
parser.add_argument('T', help='First Sentence Translation')
parser.add_argument('S1', help='Second Sentence')
parser.add_argument('LP', help='Language Pair')

parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.')
args = parser.parse_args()

#Applying some preprocessing on input data.
s_sentence = preprocess(args.S)
t_sentence = preprocess(args.T)
s1_sentence = preprocess(args.S1)

lp = args.LP
lps = lp.split('-')

#Testing Input data
assertion(s_sentence != "", "S should not be blank.\nSee -h for help")
assertion(s1_sentence != "", "S1 should not be blank.\nSee -h for help")
assertion(len(lps) == 2, "LP should be of type a-b, eg, 'en-eo'")

#Read optional params
lp_dir = args.d
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) if args.max_len else max(len(s_sentence.split()), len(s1_sentence.split()))

#Calculate FMS between S and S1.
fms = FMS(s_sentence, s1_sentence).calculate()

#Exit if low FMS.
assertion(fms >= min_fms, "Sentences have low fuzzy match score of %.02f." %fms)

#Get A set
phrase_extractor = PhraseExtractor(s_sentence, s1_sentence, min_len, max_len)
a_set = phrase_extractor.extract_pairs()

#Initiate and check Apertium
apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)


# Prepare to Generate D set.
S = s_sentence.split()
S1 = s1_sentence.split()

src = ""
src1 = ""

for a,b,c,d in a_set:
	str1 = ' '.join(S[a: b+1])
	str2 = ' '.join(S1[c: d+1])
	print('("{0}", "{1}")'.format(str1, str2))
	src += str1 + '.|'
	src1 += str2 + '.|'

src_combined = src+'.||.'+src1

src_segments = src.split('.|')
src1_segments = src1.split('.|')

#Get translations for segments.
(out, err) = apertium.translate(src_combined)
print(out)
(out, out1) = out.split('.||.')

tgt_segments = out.split('.|')
tgt1_segments = out1.split('.|')

#Generate D set
d_set = []
for (s, s1, t, t1) in list(zip(src_segments, src1_segments, tgt_segments, tgt1_segments))[:-1]:
	print(s,s1,t,t1)
	# if is_subsegment(t, t_sentence):
	# 	d_set.append((t, t1))
	# print ('("{0}", "{1}")'.format(t,t1))
