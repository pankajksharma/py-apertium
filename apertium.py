import argparse, re
from ap import Apertium
from utilities import *

parser = argparse.ArgumentParser(description='Provides pairs of Languages')
parser.add_argument('S', help='Source Language Sentence')
parser.add_argument('T', help='Target Language Sentence')
parser.add_argument('P', help='Language Pair (for example en-eo)')
parser.add_argument('-d', help='Specify the lanuguage-pair installation directory')
parser.add_argument('-r', help='Check for pairs reversibly as well',  action='store_true')
parser.add_argument('-s', help='Ignore single words',  action='store_true')
args = parser.parse_args()

#Getting optional command line inputs.
l_dir = args.d
reverse = args.r
single_words_allowed = args.s

#Applying some preprocessing on input data.
pairs = args.P.split('-')
s_sentence = preprocess(args.S)
t_sentence = preprocess(args.T)

#Testing for Apertium system wide installation.
apertium = Apertium(pairs[0], pairs[1])
(lps,err) = apertium.test_apertium()
assertion(err == '', "Apertium can't be found.\nPlease check the installation.")

#Testing Input data
assertion(s_sentence != "", "S should be there.\nSee -h for help")
assertion(t_sentence != "", "T should be there.\nSee -h for help")
assertion(len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'\nSee -h for help")

#Checking Language pair Installation.
check_installation(apertium, args.P, lps, l_dir)

#Obtain Subsequences.
subseq = get_subseqs(s_sentence, single_words_allowed)

#Conversion and printing
(out, err) = apertium.convert(subseq, l_dir)
means = {}
outp = get_pairs(subseq, out, t_sentence, means)

#If -r Option is set then doing all above stuff in reverse.
if reverse:
	apertium = Apertium(pairs[1], pairs[0])
	check_installation(apertium, 
		"{0}-{1}".format(pairs[1], pairs[0]), lps, l_dir)
	subseq = get_subseqs(t_sentence, single_words_allowed)
	(out, err) = apertium.convert(subseq, l_dir)
	outp += get_pairs(subseq, out, s_sentence, means, reverse)

#Print pairs
printed_pairs = []
for out in outp:
	if (out.lower(), means[out.lower()]) not in printed_pairs:
		print ('("{0}", "{1}")'.format(out, means[out.lower()]))
		printed_pairs.append((out.lower(), means[out.lower()])) 
