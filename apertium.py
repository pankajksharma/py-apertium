import argparse, re
from ap import Apertium

parser = argparse.ArgumentParser(description='Provides pairs of Languages')
parser.add_argument('S', help='Source Language Sentence')
parser.add_argument('T', help='Target Language Sentence')
parser.add_argument('P', help='Language Pair (for example en-eo)')
args = parser.parse_args()

pairs = args.P.split('-')
s_sentence = args.S
t_sentence = args.T
assert s_sentence != "", "S should be there."
assert t_sentence != "", "T should be there."
assert len(pairs) == 2, "P should be of form 'a-b', eg 'en-eo'"
apertium = Apertium(pairs[0], pairs[1])

(out,err) = apertium.test(s_sentence)
assert err == '', "Apertium can't be found. Please check the installation."

pair = re.findall(r'\w+-\w+', out)
assert args.P in pair, "Language Pair not found."

pairs = 0
words = s_sentence.split()
for i in range(len(words)):
	for j in range(i+1, len(words)):
		subseq = ' '.join(words[i:j+1])
		(out, err) = apertium.convert(subseq)
		if err == '' and out in t_sentence:
			print("({0}, {1})".format(subseq, out))
			pairs += 1
print("Found {0} pair(s).".format(pairs))