import argparse
from lib.fms import FMS
from lib.ap import Apertium
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch

parser = argparse.ArgumentParser(description='On the fly repairing of sentence.')
parser.add_argument('S', help='Second Sentence')
parser.add_argument('T', help='First Sentence Translation')
parser.add_argument('S1', help='Second Sentence')
parser.add_argument('LP', help='Language Pair')

parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-segment allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-segment allowed.')
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

#Initiate and check Apertium
apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)

#Calculate FMS between S and S1.
fms = FMS(s_sentence, s1_sentence).calculate()

#Exit if low FMS.
assertion(fms >= min_fms, "Sentences have low fuzzy match score of %.02f." %fms)

#Get A set
phrase_extractor = PhraseExtractor(s_sentence, s1_sentence, min_len, max_len)
a_set = phrase_extractor.extract_pairs()
a_set_pairs = {}

# Prepare to Generate D set.
S = s_sentence.split()
S1 = s1_sentence.split()

src = ""
src1 = ""

for a,b,c,d in a_set:
	try:
		a_set_pairs[(a,b)].append((c,d))
	except KeyError:
		a_set_pairs[(a,b)] = [(c,d)]

	str1 = ' '.join(S[a: b+1])
	str2 = ' '.join(S1[c: d+1])
	src += str1 + '.|'
	src1 += str2 + '.|'

src_combined = src+'.||.'+src1

src_segments = src.split('.|')
src1_segments = src1.split('.|')

#Get translations for segments.
(out, err) = apertium.translate(src_combined)
(out, out1) = out.split('.||.')

tgt_segments = out.split('.|')
tgt1_segments = out1.split('.|')

src_trans_pairs = {}
src_trans_pairs1 = {}
for (x, t, t1) in zip(a_set, tgt_segments[:-1], tgt1_segments[:-1]):
	(a,b,c,d) = x
	src_trans_pairs[(a,b)] = t
	src_trans_pairs1[(c,d)] = t1

#Main Algorithm begins
s_set = [(t_sentence, 0, [])]	#[] for maintaing which words are changed	
p = 0 							#Indexing begins with 0
while p <= len(S):
	for j in range(max([0, p-max_len]), p-min_len+1):
		sigma = (j, p-1)	
		if sigma not in src_trans_pairs.keys():	#Covers mismatch
			continue
		y = src_trans_pairs[sigma]	#No need for 'for' now
		T = get_subsegment_locs(y, t_sentence)
		if T != []:					#if y is not found in t
			for sigma1 in a_set_pairs[sigma]:	#Source aligns
				for tau in T:
					tau1 = src_trans_pairs1[sigma1]	#No need for another 'for' now
					for (t1, features, covered) in s_set:
						# print tau, tau1
						t1_new = patch(t1, tau, tau1, covered)
						if t1_new != None:
							pass
	p += 1
