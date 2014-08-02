import os.path
import argparse, re, sys
from lib.fms import FMS
from lib.ap import Apertium
from lib.tmxfile import TMXFile
from lib.patcher import Patcher
from lib.utilities import preprocess, assertion

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Reads Translation Memory and tries to patch given sentence based on TMX')
parser.add_argument('TM', help='Translation Memory')
parser.add_argument('S', help='Second Sentence')
parser.add_argument('LP', help='Language Pair for TM (for example en-eo)')

parser.add_argument('-v', help='Verbose Mode', action='store_true')
parser.add_argument('-t', help='Show patching traces', action='store_true')
parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('--cam', help='Only those patches which cover all the mismatches', action='store_true')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-segment allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-segment allowed.', default='5')
args = parser.parse_args()

#Applying some preprocessing on input data.
s_sentence = preprocess(args.S)
tmxfile = preprocess(args.TM)
lp = args.LP
lps = lp.split('-')


#Testing Input data
assertion(s_sentence != "", "S should not be blank. See -h for help")
assertion(os.path.isfile(tmxfile), "TM does not exist")
assertion(len(lps) == 2, "LP should be of type a-b, eg, 'en-eo'")

#Read optional params
lp_dir = args.d
verbose = args.v
show_traces = args.t
cover_all = args.cam
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len)

#Initiate and check Apertium
apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)

tmxf = TMXFile(tmxfile, lps[0], lps[1])
tmunits = tmxf.getunits()

fmses = {}

for tmxu in tmunits:
	src, tgt = preprocess(tmxu.getsource()), preprocess(tmxu.gettarget())
	fms = FMS(s_sentence, src)
	max_fms = fms.get_max_fms()
	if max_fms >= min_fms:
		fms = fms.calculate_using_wanger_fischer()
		if fms >= min_fms:
			fmses[(src, tgt)] = fms

assertion(fmses != {}, "No proper match with FMS > {0} could be found".format(min_fms))

sorted_fms = sorted(fmses, key=fmses.get)

(src, tgt) = sorted_fms[0] #Best match 
# print(s_sentence, src, tgt)
patches = Patcher(apertium, src, s_sentence, tgt).patch(min_len, max_len)
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

