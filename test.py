import argparse
import os.path, sys
from lib.fms import FMS
from lib.ap import Apertium
from lib.utilities import assertion
from lib.features import get_features
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Regression test for repair.py')
parser.add_argument('SLF', help='Source Language file for training')
parser.add_argument('TLF', help='Target Language file for training')
parser.add_argument('SLFT', help='Source Language file for testing')
parser.add_argument('TLFT', help='Target Language file for testing')

parser.add_argument('LP', help='Language Pair (sl-tl)')

parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('-v', help='Verbose Mode', action='store_true')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.', default='5')
args = parser.parse_args()

#Preprocessing
lp = args.LP
lps = lp.split('-')
assertion(len(lps) == 2, "LP should be of type a-b, eg, 'en-eo'")

#Make sure all files exist
assertion(os.path.isfile(args.SLF), "Source Language file for training could not be found.")
assertion(os.path.isfile(args.TLF), "Target Language file for training could not be found.")
assertion(os.path.isfile(args.SLFT), "Source Language file for testing could not be found.")
assertion(os.path.isfile(args.TLFT), "Target Language file for testing could not be found.")

#TODO:Check lines are equal in SLFs and TLFs.

#Command line params
lp_dir = args.d
verbose = args.v
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) 

#Training file pointers
file1 = open(args.SLF)
file2 = open(args.TLF)

#Testing file pointers
file3 = open(args.SLFT)
file4 = open(args.TLFT)

src_sentences, tgt_sentences = [], []
fms_map = {}

while True:
	line = preprocess(file1.readline())
	line1 = preprocess(file2.readline())
	if not line or not line1:
		break
	src_sentences.append(line)
	tgt_sentences.append(line1)

while True:
	line = preprocess(file3.readline())
	line1 = preprocess(file4.readline())
	if not line or not line1:
		break
	for s,t in zip(src_sentences, tgt_sentences):
		fms = FMS(s, line)
		max_fms = fms.get_max_fms()			#Get max possible FMS for the pair
		if max_fms >= min_fms:
			fms = fms.calculate_using_wanger_fischer()	#Get actual FMS
			if fms >= min_fms:
				fms_map[(s,t)] = (line, line1)
	print(len(fms_map))


apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)

#Global values
gl_wer = []
best_wer = []
gl_no_of_patches = 0.0

for (s, s1) in fms_map.keys():
	# print([s,s1,fms_map[s,s1]])
	s_sentence, s1_sentence, (t_sentence, t1_sentence) = s, s1, fms_map[(s,s1)]
	#Extracrt phrases
	phrase_extractor = PhraseExtractor(s_sentence, s1_sentence, min_len, max_len)
	a_set = phrase_extractor.extract_pairs()
	src_mismatches,_ = phrase_extractor.find_non_alignments()


	a_set_pairs = {}

	# Prepare to Generate D set.
	S = s_sentence.split()
	S1 = s1_sentence.split()
	TS = t_sentence.split()

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
	# print(out, err)
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
	wer = []
	no_of_patches = 0.0
	i = 0
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
							i += 1
							if i > 100:
								break
							t1_new, covered_new = patch(t1, tau, tau1, covered[:])
							if t1_new != None:
								# print(t1_new)
								features = get_features(p, sigma, src_mismatches, t1_new, t1, tau)
								s_set.append((t1_new, features, covered_new))
								fms = FMS(t1_sentence, t1_new).calculate_using_wanger_fischer()
								wer.append(1.0 - fms)
								no_of_patches += 1
								gl_wer.append(1.0 - fms)
								gl_no_of_patches += 1
		p += 1
	if wer != []:
		best_wer.append(min(wer))
	if verbose:
		if wer != []:
			print("Best patched WER: {0}".format(min(wer)))
			print("Average WER: {0}".format(sum(wer)/no_of_patches))
		print("Number of patched sentences: {0}".format(int(no_of_patches)))
		print("")	#Blank line

print("Global Statistics:")
print("Best Patch WER: {0}".format(min(gl_wer)))
print("Average WER of best Patched sentences: {0}".format(sum(best_wer) / (len(best_wer)*1.0)))
print("Average WER value: {0}".format(sum(gl_wer) / gl_no_of_patches))
print("Number of patched sentences: {0}".format(int(gl_no_of_patches)))