class memoize(dict):
	def __init__(self, func):
		self.func = func

	def __call__(self, *args):
		return self[args]

	def __missing__(self, key):
		result = self[key] = self.func(PhraseExtractor, *key)
		return result

class PhraseExtractor(object):
	def __init__(self, first_sentence, second_sentece, min_len=2, max_len=5):
		self._src = tuple(first_sentence.split())
		self._tgt = tuple(second_sentece.split())
		self._min_len = min_len
		self._max_len = max_len
		self._lcs = list(self._LCS(self._src, self._tgt))

	def _aligned(self, f_val, A, f_len, type='start'):
		if any(f_value == f_val for (_, f_value) in A):
			return True
		elif type=='start':
			return f_val < 0
		else:
			return f_val >= f_len
		return False

	def _extract(self, fs, fe, es, ee, f_len, A):
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
				if self._aligned(f_end, A, f_len, 'end'):
					break
			f_start -= 1
			if self._aligned(f_start, A, f_len):
				break
		return E


	def phrase_pairs(self):
		e = self._src
		f = self._tgt
		A = self.find_alignments()
		bp = []
		for es in range(len(e)):
			for ee in range(es, len(e)):
				fs, fe = (len(f), -1)
				for em,fm in A:
					if es <= em <= ee:
						fs = min(fm, fs)
						fe = max(fm, fe)
				bp += self._extract(fs, fe, es, ee, len(f), A)
		return bp

	@memoize
	def _LCS(self, seq1, seq2):
		if len(seq1)==0 or len(seq2)==0:
			return tuple()
		if seq1[-1] == seq2[-1]:
			return self._LCS(seq1[:-1], seq2[:-1]) + tuple([seq1[-1]])
		else:
			candidate1 = self._LCS(seq1[:-1], seq2)
			candidate2 = self._LCS(seq1, seq2[:-1])
			if len(candidate1) >= len(candidate2):
				return candidate1
			else:
				return candidate2

	def find_alignments(self):
		s = self._src
		s1 = self._tgt
		lcs = self._lcs
		aligns = []
		s_in, s1_in = -1, -1
		for cs in lcs:
			s_in = min([a for a in range(len(s)) if a > s_in and s[a] == cs])
			s1_in = min([a for a in range(len(s1)) if a > s1_in and s1[a] == cs])
			aligns.append((s_in, s1_in))
		return aligns

	def find_non_alignments(self):
		src_non_aligns = list(range(len(self._src)))
		tgt_non_aligns = list(range(len(self._tgt)))
		
		aligns = self.find_alignments()
		for (s,t) in aligns:
			src_non_aligns.remove(s)
			tgt_non_aligns.remove(t)
		return src_non_aligns, tgt_non_aligns

	def extract_pairs(self):
		src_non_aligns, tgt_non_aligns = self.find_non_alignments()
		all_pairs = self.phrase_pairs()
		selected_pairs = []
		m = self._min_len
		n = self._max_len

		for a,b,c,d in all_pairs:
			if m<=(b-a)+1<=n and \
				(any(a<=e<=b for e in src_non_aligns) or \
				any(c<=e<=d for e in tgt_non_aligns)): #Checks for lengths & mis-alignments
				selected_pairs.append((a,b,c,d))
		return selected_pairs
