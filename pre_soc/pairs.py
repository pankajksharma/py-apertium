import argparse, re
from utilities import *
from ed import memoize

def aligned(f_val, A, f_len, type='start'):
	if any(f_value == f_val for (_, f_value) in A):
		return True
	elif type=='start':
		return f_val < 0
	else:
		return f_val >= f_len
	return False

def extract(fs, fe, es, ee, f_len, A):
	if fe == -1:
		return []
	for (e,f) in A:
		if (e < es or e > ee):
			if (fs <= f <= fe):
				return []
	E = []
	f_start = fs
	while True:
		f_end = fe
		while True:
			E.append((es,ee,f_start,f_end))
			f_end += 1
			if aligned(f_end, A, f_len, 'end'):
				break
		f_start -= 1
		if aligned(f_start, A, f_len):
			break
	return E


def phrase_pairs(e,f,A):
	bp = []
	for es in range(len(e)):
		for ee in range(es, len(e)):
			fs, fe = (len(f), -1)
			for em,fm in A:
				if es <= em <= ee:
					fs = min(fm, fs)
					fe = max(fm, fe)
			bp += extract(fs, fe, es, ee, len(f), A)
	return bp

@memoize
def LCS(seq1, seq2):
	if len(seq1)==0 or len(seq2)==0:
		return tuple()
	if seq1[-1] == seq2[-1]:
		return LCS(seq1[:-1], seq2[:-1]) + tuple([seq1[-1]])
	else:
		candidate1 = LCS(seq1[:-1], seq2)
		candidate2 = LCS(seq1, seq2[:-1])
		if len(candidate1) >= len(candidate2):
			return candidate1
		else:
			return candidate2

def find_alignment(s, s1):
	lcs = list(LCS(tuple(s), tuple(s1)))
	print lcs
	aligns = []
	s_in, s1_in = -1, -1
	for cs in lcs:
		s_in = min([a for a in range(len(s)) if a > s_in and s[a] == cs])
		s1_in = min([a for a in range(len(s1)) if a > s1_in and s1[a] == cs])
		aligns.append((s_in, s1_in))
	return aligns

parser = argparse.ArgumentParser(description='Provides phrase pairs')
parser.add_argument('S', help='First Sentence')
parser.add_argument('S1', help='Second Sentence')
args = parser.parse_args()

S = preprocess(args.S).split()
S1 = preprocess(args.S1).split()

print find_alignment(S, S1)

pairs = phrase_pairs(S, S1, find_alignment(S, S1))

for p in pairs:
	str1 = ' '.join(S[p[0]:p[1]+1])
	str2 = ' '.join(S1[p[2]:p[3]+1])
	print '("{0}", "{1}")'.format(str1, str2)
