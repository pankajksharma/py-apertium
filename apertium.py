import argparse, re
from ap import Apertium

parser = argparse.ArgumentParser(description='Provides pairs of Languages')
parser.add_argument('S', help='Source Language Sentence')
parser.add_argument('T', help='Target Language Sentence')
parser.add_argument('P', help='Language Pair (for example en-eo)')
parser.add_argument('-d', help='Specify the lanuguage pair directory')
args = parser.parse_args()

l_dir = args.d

pairs = args.P.split('-')
s_sentence = args.S
t_sentence = args.T
assert s_sentence != "", "S should be there."
assert t_sentence != "", "T should be there."
assert len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'"
apertium = Apertium(pairs[0], pairs[1])

(lps,err) = apertium.test_apertium()
assert err == '', "Apertium can't be found.\nPlease check the installation."

if not l_dir:
	pair = re.findall(r'\w+-\w+', lps)
	assert args.P in pair, "Language Pair not installed."
else:
	(out,err) = apertium.test_lp(l_dir)
	assert out == '', "Language Pair not found."

subseq = ""
t_sentence = t_sentence.lower()

words = s_sentence.split()
for i in range(len(words)):
	for j in range(i+1, len(words)):
		subseq += ' '.join(words[i:j+1])+'.|'
(out, err) = apertium.convert(subseq, l_dir)

for sub, msub in zip(subseq.split('.|'), out.split('.|')):
	if sub != "" and msub != "" and msub.lower() in t_sentence:
		if sub[0].islower() and len(msub) > 1:
			msub = msub[0].lower() + msub[1:]
		elif sub[0].islower():
			msub = msub.lower()
		print ('("{0}", "{1}")'.format(sub, msub)) 
	