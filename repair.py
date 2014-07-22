import argparse, sys, time
from lib.fms import FMS
from lib.ap import Apertium
from lib.patcher import Patcher
from lib.utilities import preprocess, assertion

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='On the fly repairing of sentence.')
parser.add_argument('S', help='Second Sentence')
parser.add_argument('T', help='First Sentence Translation')
parser.add_argument('S1', help='Second Sentence')
parser.add_argument('LP', help='Language Pair')

parser.add_argument('-v', help='Verbose Mode', action='store_true')
parser.add_argument('-t', help='Show patching traces', action='store_true')
parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('--cam', help='Only those patches which cover all the mismatches', action='store_true')
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
assertion(s_sentence != "", "S should not be blank. See -h for help")
assertion(s1_sentence != "", "S1 should not be blank. See -h for help")
assertion(len(lps) == 2, "LP should be of type a-b, eg, 'en-eo'")

#Read optional params
lp_dir = args.d
verbose = args.v
show_traces = args.t
cover_all = args.cam
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) if args.max_len else max(len(s_sentence.split()), len(s1_sentence.split()))

#Initiate and check Apertium
apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)

#Calculate FMS between S and S1.
fms = FMS(s_sentence, s1_sentence).calculate_using_wanger_fischer()

#Exit if low FMS.
assertion(fms >= min_fms, "Sentences have low fuzzy match score of %.02f." %fms)

patches = Patcher(apertium, s_sentence, s1_sentence, t_sentence).patch(min_len, max_len)
# print patches
for (patch, features, _, _, _, cam, traces) in patches:
	if cover_all and cam:
		print(patch)
		if verbose:
			print(features)
		if show_traces:
			print(traces)
	elif not cover_all:
		print(patch)
		if verbose:
			print(features)
		if show_traces:
			print(traces)
