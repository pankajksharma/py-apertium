import argparse, re, sys
import os.path
from ap import Apertium
from utilities import *
from translate.storage.tmx import *
from tmxunit import TMXUnit
from tmxfile import TMXFile

reload(sys)
sys.setdefaultencoding('utf-8')
parser = argparse.ArgumentParser(description='Reads Translation Memory and saves the sub-segments')
parser.add_argument('TM', help='Translation Memory')
parser.add_argument('P', help='Language Pair for TM (for example en-eo)')
parser.add_argument('-o', help='Output file to save new TMX')
parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('-r', help='Check for pairs reversibly as well',  action='store_true')
parser.add_argument('-s', help='Ignore single words',  action='store_true')
args = parser.parse_args()

#Getting optional command line inputs.
tmx_out	= args.o
single_words_allowed = args.s
reverse = args.r

#Applying some preprocessing on input data.
l_dir = args.d
tmname = args.TM
lp = args.P
pairs = args.P.split('-')

#Testing for Apertium system wide installation.
apertium = Apertium(pairs[0], pairs[1])
(lps,err) = apertium.test_apertium()
assertion(err == '', "Apertium can't be found.\nPlease check the installation.")

#Testing Input data
assertion(os.path.isfile(tmname), "TM couldn't be found.\nSee -h for help")
assertion(len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'\nSee -h for help")

#Checking Language pair Installation.
check_installation(apertium, lp, lps, l_dir)

#If reverse, test for reverse
if reverse:
	apertium_rev = Apertium(pairs[1], pairs[0])
	lp_rev = '-'.join(lp.split('-'))
	check_installation(apertium_rev, lp_rev, lps, l_dir)

tmxf = TMXFile(tmname, pairs[0], pairs[1])
tmunits = tmxf.getunits()

for tmxu in tmunits:
	src, tgt = preprocess(tmxu.getsource()), preprocess(tmxu.gettarget())
	
	#Obtain Subsequences
	out_locations = {}
	seqs_covered = []
	sub_segments = ""
	seqs_covered_in_tgt = []

	subseq = get_subseq_locations(src, single_words_allowed)
	for s in subseq:
		seg = src[s[0]:s[1]]
		if seg.lower() not in seqs_covered:
			sub_segments += seg + '.|'
			seqs_covered.append(seg.lower())

	(outp, err) = apertium.convert(sub_segments, l_dir)
	
	for s, out in zip(subseq, outp.split('.|')):
		out = preprocess(out)
		out_locs = get_out_locations(out, tgt)
		if out_locs != []:
			out_locations[s] = out_locs
			seqs_covered_in_tgt += out_locs

	if reverse:
		seqs_covered = []
		subseq = get_subseq_locations(tgt, single_words_allowed)
		for s in subseq:
			# if s in seqs_covered_in_tgt:
			# 	continue
			seg = tgt[s[0]:s[1]]
			if seg.lower() not in seqs_covered:
				sub_segments += seg + '.|'
				seqs_covered.append(seg.lower())

		(outp, err) = apertium_rev.convert(sub_segments, l_dir)
		
		for s, out in zip(subseq, outp.split('.|')):
			out = preprocess(out)
			out_locs = get_out_locations(out, tgt)
			if out_locs != []:
				for loc in out_locs:
					out_locations[loc] = [s]
							
	add_bpt_ept(tmxu, src, tgt, lp, out_locations)
	


if tmx_out:
	tmxf.save(tmx_out)
else:
	tmxf.save(tmname)
	