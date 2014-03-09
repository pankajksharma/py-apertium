import argparse, re
from ap import Apertium
from utilities import *

parser = argparse.ArgumentParser(description='Provides pairs of Languages')
parser.add_argument('S', help='Source Language Sentence')
parser.add_argument('T', help='Target Language Sentence')
parser.add_argument('P', help='Language Pair (for example en-eo)')
parser.add_argument('-d', help='Specify the lanuguage pair directory')
parser.add_argument('-r', help='Checks for pairs reversibly',  action='store_true')
args = parser.parse_args()

l_dir = args.d
reverse = args.r
pairs = args.P.split('-')
s_sentence = preprocess(args.S)
t_sentence = preprocess(args.T)

assert s_sentence != "", "S should be there."
assert t_sentence != "", "T should be there."
assert len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'"

apertium = Apertium(pairs[0], pairs[1])
if reverse:
	s_sentence, t_sentence = t_sentence, s_sentence
	apertium = Apertium(pairs[1], pairs[0])

(lps,err) = apertium.test_apertium()
assert err == '', "Apertium can't be found.\nPlease check the installation."

if not l_dir:
	pair = re.findall(r'\w+-\w+', lps)
	assert args.P in pair, "Language Pair not installed."
else:
	(out,err) = apertium.test_lp(l_dir)
	assert out == '', "Language Pair not found in directory %s. %l_dir"

t_sentence = t_sentence.lower()

subseq = ""
words = s_sentence.split()
for i in range(len(words)):
	for j in range(i+1, len(words)):
		subseq += ' '.join(words[i:j+1])+'.|'
(out, err) = apertium.convert(subseq, l_dir)

print_sequences(subseq, out, t_sentence, reverse)
