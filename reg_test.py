import argparse
import os.path, sys
from lib.fms import FMS
from lib.ap import Apertium
from lib.patcher import Patcher
from lib.utilities import assertion
from lib.features import get_features
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch, warning

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Regression test for preprocess.py')
parser.add_argument('out', help='Output file generated from test.py')

parser.add_argument('LP', help='Language Pair (sl-tl)')

parser.add_argument('-d', help='Specify the language-pair installation directory')
parser.add_argument('-c', help='Specify the sqlite3 db to be used for caching', default='')
parser.add_argument('-v', help='Verbose Mode', action='store_true')
parser.add_argument('--mode', help="Modes('all', 'cam', 'compare')", default='all')
parser.add_argument('--go', help='To patch only grounded mismatches', action='store_true')
parser.add_argument('--bo', help='Uses the best possible transalation only', action='store_true')
parser.add_argument('--min-fms', help='Minimum value of fuzzy match score of S and S1.', default='0.8')
parser.add_argument('--min-len', help='Minimum length of sub-string allowed.', default='2')
parser.add_argument('--max-len', help='Maximum length of sub-string allowed.', default='5')
args = parser.parse_args()

#Preprocessing
lp = args.LP
lps = lp.split('-')
assertion(len(lps) == 2, "LP should be of type a-b, eg, 'en-eo'")

#Make sure all files exist
assertion(os.path.isfile(args.out), args.out+" doesn't exist")

#TODO:Check lines are equal in SLFs and TLFs.

#Command line params
cache = args.c
lp_dir = args.d
verbose = args.v
mode = args.mode.lower()

assertion(mode in ['all', 'cam', 'compare'], "Mode couldn't be identified.")
grounded = args.go
best_only = args.bo
min_fms = float(args.min_fms)
min_len = int(args.min_len)
max_len = int(args.max_len) 

warning(min_len > 1 & grounded, "min_len should be greater than 1")

cache_db_file = None
if cache != '':
	cache_db_file = cache

use_caching = True if cache_db_file else False

apertium = Apertium(lps[0], lps[1])
(out, err) = apertium.check_installations(lp_dir)
assertion(out, err)

#Reopen new file
file1 = open(args.out)

#Global values
gl_wer = []
best_wer = []
gl_up_wer = []
gl_no_of_patches = 0.0

if mode == 'compare':
	gl_wer2 = []
	best_wer2 = []
	gl_no_of_patches2 = 0.0

count = 1

while True:
	s = file1.readline().rstrip()
	t = file1.readline().rstrip()
	s1 = file1.readline().rstrip()
	t1 = file1.readline().rstrip()

	if not (s and s1 and t and t1):
		break

	wer = []
	no_of_patches = 0.0
	if mode == 'compare':
		wer2 = []
		no_of_patches2 = 0.0

	tgt_sentences = t1.lower()
	
	patcher = Patcher(apertium, s, s1, t, use_caching, cache_db_file)
	patches = patcher.patch(min_len, max_len, grounded, lp_dir)
	best_patch = patcher.get_best_patch()
	best_patch_with_cam = patcher.get_best_patch(True) #Best patched result covering all mismatches
	
	if best_patch:
		patches.append(best_patch)

	all_patches = patches[:]
	
	if not grounded:
		unpatched = patches[0]
		all_patches.pop(0)
	else:
		unpatched = (t1,)

	if best_only:
		up_wer = 1.0 - FMS(unpatched[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
		gl_up_wer.append(up_wer)
		wer = -1
		try:
			cam = best_patch[5]
		except:
			cam = False

		if not best_patch:
			best_patch = unpatched

		if mode == 'all':
			fms = FMS(best_patch[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
			wer = 1.0-fms
			best_wer.append(wer)
			gl_wer.append(wer)
			gl_no_of_patches += 1

		elif mode == 'cam':
			if best_patch_with_cam:
				fms = FMS(best_patch_with_cam[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
				wer = 1.0-fms
				best_wer.append(wer)
				gl_wer.append(wer)
				gl_no_of_patches += 1
			else:
				warning(True, "No patch with bo and cam")

		else:	#Assuming mode = 'compare'
			if best_patch_with_cam:
				fms = FMS(best_patch[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
				wer = 1.0-fms
				best_wer.append(wer)
				gl_wer.append(wer)
				gl_no_of_patches += 1

				fms = FMS(best_patch_with_cam[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
				wer2 = 1.0-fms
				best_wer2.append(wer2)
				gl_wer2.append(wer2)
				gl_no_of_patches2 += 1
			else:
				warning(True, "No patch with bo and cam")

		if verbose and wer != -1:
			print("#%d Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%%"
				%(count, wer*100, ((wer+up_wer)/2.0)*100, up_wer*100))
			if mode == 'compare':
				print("#%d(cam) Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%%"
					%(count, wer2*100, ((wer2+up_wer)/2.0)*100, up_wer*100))
			count += 1
		continue

	up_wer = 1.0 - FMS(unpatched[0].lower(), tgt_sentences).calculate_using_wanger_fischer()
	gl_up_wer.append(up_wer)

	for (patch, features, _, _, _, cam, traces) in all_patches:
		if mode == 'all':
			fms = FMS(patch.lower(), tgt_sentences).calculate_using_wanger_fischer()
			wer.append(1.0-fms)
			no_of_patches += 1
		elif mode == 'cam' and cam:
			fms = FMS(patch.lower(), tgt_sentences).calculate_using_wanger_fischer()
			wer.append(1.0-fms)			
			no_of_patches += 1
		elif mode == 'compare':
			fms = FMS(patch.lower(), tgt_sentences).calculate_using_wanger_fischer()
			wer.append(1.0-fms)
			no_of_patches += 1
			if cam:
				fms = FMS(patch.lower(), tgt_sentences).calculate_using_wanger_fischer()
				wer2.append(1.0-fms)
				no_of_patches2 += 1

	if mode == 'compare' and wer2 != []:
		gl_wer += wer
		best_wer.append(min(wer))
		gl_no_of_patches += no_of_patches

		gl_wer2 += wer2
		best_wer2.append(min(wer2))
		gl_no_of_patches2 += no_of_patches2

	elif mode != 'compare':
		gl_wer += wer
		gl_no_of_patches += no_of_patches

		if wer != []:
			best_wer.append(min(wer))

	if verbose:
		if wer != []:
			print("#%d Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%% N = %d"
				%(count, min(wer)*100, (sum(wer)/no_of_patches)*100, up_wer*100, int(no_of_patches)))
		else:
			print("#%d Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%% N = %d"
				%(count, up_wer*100, up_wer*100, up_wer*100, int(no_of_patches)))
		if mode == 'compare':
			if wer2 != []:
				print("#%d Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%% N = %d"
					%(count, min(wer2)*100, (sum(wer2)/no_of_patches2)*100, up_wer*100, int(no_of_patches2)))
			else:
				print("#%d(cam) Best = %.02f%% Avg = %.02f%% Unpatched = %.02f%% N = %d"
					%(count, up_wer*100, up_wer*100, up_wer*100, int(no_of_patches2)))
		count += 1

if mode == 'compare':
	print("Global Statistics(all):")
else:
	print("Global Statistics:")
warning(best_wer != [], "No suitable patched candidate could be obtained")
if best_wer != []:
	print("Average best patched WER: %.02f%%" %(sum(best_wer) / len(best_wer) * 100))
	print("Average WER: %.02f%%" %(sum(gl_wer) / len(gl_wer) * 100))
print("Average unpatched WER: %.02f%%" %(sum(gl_up_wer) / len(gl_up_wer) * 100))
print("Number of patched sentences: %d" %(int(gl_no_of_patches)))
if best_wer != []:
	print("Average number of patches per sentences: %.02f" %(gl_no_of_patches / len(best_wer)))

if mode == 'compare':
	print("Global Statistics (covering all mismatches):")
	if best_wer != []:
		print("Average best patched WER: %.02f%%" %(sum(best_wer2) / (len(best_wer2) * 100)))
		print("Average WER: %.02f%%" %(sum(gl_wer2) / len(gl_wer2) * 100))
	print("Average unpatched WER: %.02f%%" %(sum(gl_up_wer) / len(gl_up_wer) * 100))
	print("Number of patched sentences: %d" %(int(gl_no_of_patches2)))
	if best_wer != []:
		print("Average number of patches per sentences: %.02f" %(gl_no_of_patches2 / len(best_wer2)))

print("Number of unpatched pairs: %d" %(len(gl_up_wer) - len(best_wer)))
