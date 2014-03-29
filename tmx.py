import argparse, re
import os.path
from ap import Apertium
from utilities import *
from translate.storage.tmx import *
from tmxunit import TMXUnit
from tmxfile import TMXFile

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
reverse = args.r
single_words_allowed = args.s

#Applying some preprocessing on input data.
l_dir = args.d
tmname = args.TM
pairs = args.P.split('-')

#Testing for Apertium system wide installation.
apertium = Apertium(pairs[0], pairs[1])
(lps,err) = apertium.test_apertium()
assertion(err == '', "Apertium can't be found.\nPlease check the installation.")

#Testing Input data
assertion(os.path.isfile(tmname), "TM couldn't be found.\nSee -h for help")
assertion(len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'\nSee -h for help")

#Checking Language pair Installation.
check_installation(apertium, args.P, lps, l_dir)

tmxf = TMXFile(tmname, pairs[0], pairs[1])
tmunits = tmxf.getunits()

for tmxu in tmunits:
	src, tgt = tmxu.getsource(), tmxu.gettarget()
	if not tgt:
		continue

	#Obtain Subsequences.
	subseq = get_subseq_locations(src, single_words_allowed)
	
	srcl = src.split()
	out_locations = {}

	#Conversion
	seqs_covered = []
	for s in subseq:
		seq = ' '.join(srcl[s[0]: s[1]])
		if seq.lower() == src.lower():
			continue
		if seq.lower() not in seqs_covered:
			(out, err) = apertium.convert(seq, l_dir)
			out_locations[s] = get_out_locations(out, tgt)
			seqs_covered.append(seq.lower())
	
	#If -r Option (does nothing for now).
	if reverse:
		pass

	add_bpt_ept(tmxu, src, tgt, subseq, out_locations)
	if tmx_out:
		tmxf.save(tmx_out)
	else:
		tmxf.save(tmname)
	