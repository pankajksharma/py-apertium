from lib.ap import Apertium
from lib.features import get_features
from lib.phrase_extractor import PhraseExtractor
from lib.utilities import preprocess, assertion, get_subsegment_locs, patch

class Patcher(object):
	"""
		Patches the strings passed.
	"""
	def __init__(self, apertium, first_source_sentence, second_source_sentence, target_sentence):		
		self.apertium = apertium
		self.s_sentence = first_source_sentence.lower()
		self.s1_sentence = second_source_sentence.lower()
		self.t_sentence = target_sentence.lower()

	def _do_edit_distace_alignment(self, min_len, max_len):
		#Do edit distance alignment
		phrase_extractor = PhraseExtractor(self.s_sentence, self.s1_sentence, min_len, max_len)
		self.phrases = phrase_extractor.extract_pairs()
		self.src_mismatches, self.tgt_mismatches = phrase_extractor.find_non_alignments()

	def _check_for_all_mismatches(self, cs, cs1):
		for sm in self.src_mismatches:
			for (a,b) in cs:
				if a <= sm <= b:
					break
			else:
				return False
		for tm in self.tgt_mismatches:
			for (a,b) in cs1:
				if a <= tm <= b:
					break
			else:
				return False
		return True

	def _covers_all_mimatches(self, sigma, sigma1, cs, cs1):
		cs.append(sigma)
		cs1.append(sigma1)
		return self._check_for_all_mismatches(cs, cs1)

	def _do_translations(self):
		S = self.s_sentence.split()
		S1 = self.s1_sentence.split()
		
		src = ""
		src1 = ""
		self.mismatches_map = {}

		for a,b,c,d in self.phrases:
			try:
				self.mismatches_map[(a,b)].append((c,d))
			except KeyError:
				self.mismatches_map[(a,b)] = [(c,d)]

			str1 = ' '.join(S[a: b+1])
			str2 = ' '.join(S1[c: d+1])
			src += str1 + '.|'
			src1 += str2 + '.|'

		src_combined = src+'.||.'+src1

		#Get translations for segments.
		(out, err) = self.apertium.translate(src_combined)
		# print(out, err)
		(out, out1) = out.split('.||.')

		tgt_segments = out.split('.|')
		tgt1_segments = out1.split('.|')

		self.src_trans_map = {}
		self.src_trans_map1 = {}
		for (x, t, t1) in zip(self.phrases, tgt_segments[:-1], tgt1_segments[:-1]):
			(a,b,c,d) = x
			self.src_trans_map[(a,b)] = t
			self.src_trans_map1[(c,d)] = t1

	def _do_patching(self, t_app, tau, tau1, covered_pos, grounded_only):
		(a,b) = tau
		t_app = t_app.split()

		if(any(a<=c<=b for c in covered_pos)):
			return None, None

		seg = ' '.join(t_app[a:b+1])
		seg_left = ' '.join(t_app[:a])
		seg_right = ' '.join(t_app[b+1:])

		if grounded_only:
			if not (seg_left and seg_right):
				return None, None
		
		seg = tau1.split()
		# print(a,b, covered_pos, t_app[a:b+1], seg, t_app)
		
		pe = PhraseExtractor(' '.join(t_app[a:b+1]).lower(), tau1.lower())
		aligns = pe.find_alignments()
		
		tg_aligns = [x for (_, x) in aligns]
		cp = [a+i for i in range(len(seg)) if i not in tg_aligns]
		cp += covered_pos
		# print(cp)

		if seg_left != '':
			tau1 = tau1.lower()
		return (seg_left + ' ' + tau1 + ' ' + seg_right).strip(), cp
		
	def _covers_mismatch(self, sigma):
		return sigma in self.mismatches_map.keys() 

	def patch(self, min_len=2, max_len=5, grounded_only=False):
		#Some preprocessings
		self._do_edit_distace_alignment(min_len, max_len)
		self._do_translations()

		S = self.s_sentence.split()
		S1 = self.s1_sentence.split()
		TS = self.t_sentence.split()
		s_set = [(self.t_sentence, "unpatched", [], [], [], False, [])]	#[] for maintaing which words are changed	

		p = 0 							#Indexing begins with 0
		while p <= len(S):
			for j in range(max([0, p-max_len]), p-min_len+1):
				sigma = (j, p-1)	
				if not self._covers_mismatch(sigma):	#Covers mismatch
					continue
				y = self.src_trans_map[sigma]	#No need for 'for' now
				T = get_subsegment_locs(y, self.t_sentence)
				
				if T != []:					#if y is not found in t
					for sigma1 in self.mismatches_map[sigma]:	#Source aligns
						for tau in T:
							tau1 = self.src_trans_map1[sigma1]	#No need for another 'for' now
							s_set_temp = []
							for (t1, features, covered, cs, cs1, c_all) in s_set:
								if c_all:
									continue
								t1_new, covered_new = self._do_patching(t1, tau, tau1, covered[:], grounded_only)
								if t1_new != None:
									features = get_features(p, sigma, self.src_mismatches, t1_new, t1, tau)
									cam = self._covers_all_mimatches(sigma, sigma1, cs, cs1)
									s_set_temp.append((t1_new, features, covered_new, cs, cs1, cam,
										(' '.join(S[sigma[0]:sigma[1]+1]).strip().lower(), 
												' '.join(S1[sigma1[0]:sigma1[1]+1]).strip().lower(), 
												' '.join(TS[tau[0]:tau[1]+1]).strip().lower())))
									# s_set_temp[(t1_new, features, covered_new)] = self._covers_all_mimatches(sigma, sigma1)))
									# print(t_out)
									# if verbose:
									# print(covered_new)
									# print(features)
									# print((' '.join(S[sigma[0]:sigma[1]+1]).strip().lower(), 
									# 			' '.join(S1[sigma1[0]:sigma1[1]+1]).strip().lower(), 
									# 			' '.join(TS[tau[0]:tau[1]+1]).strip().lower(), tau1))
									# time.sleep(2)
							s_set += s_set_temp
			p += 1
		return s_set
		