import re
from lxml import etree

def preprocess(sentence):
	"""Preprocesses the sentence to remove extra spaces."""
	sentence = sentence.strip()
	rex = re.compile(r'\s+')
	return rex.sub(' ', sentence)

def assertion(condition, statement):
	"""Checks condition and exits with NZ exit if it's not True."""
	if not condition:
		print (statement)
		exit(1)

def check_installation(apertium, lp, lps, lp_dir=None):
	"""Checks for apertium lp installations."""
	if not lp_dir:
		pair = re.findall(r'\w+-\w+', lps)
		assertion(lp in pair, "Language Pair not installed.")
	else:
		(out,err) = apertium.test_lp(lp_dir)
		assertion(out == '', "Language Pair not found in directory '%s'" %lp_dir)

def get_subseqs(sentence, single_words_allowed=False):
	"""Returns subsequences from sentence."""
	subseq = ""
	words = sentence.split()
	for i in range(len(words)):
		k = i if not single_words_allowed else i+1
		for j in range(k, len(words)):
			subseq += ' '.join(words[i:j+1])+'.|'
	return subseq

def get_pairs(inp, out, sentence, converions, reverse=None):
	"""Returns Languge pair sequences."""	
	subsequences = []
	t_sentence = sentence.lower()
	if not reverse:
		for sub, msub in zip(inp.split('.|'), out.split('.|')):
			sub, msub = preprocess(sub), preprocess(msub)
			if sub != "" and msub != "" and msub.lower() in t_sentence:
				if sub[0].islower() and len(msub) > 1:
					msub = msub[0].lower() + msub[1:]
				elif sub[0].islower():
					msub = msub.lower()
				converions[sub.lower()] = msub
				subsequences.append(sub)
	else:
		for sub, msub in zip(inp.split('.|'), out.split('.|')):
			sub, msub = preprocess(sub), preprocess(msub)
			if sub != "" and msub != "" and msub.lower() in t_sentence:
				if sub[0].islower() and len(msub) > 1:
					msub = msub[0].lower() + msub[1:]
				elif sub[0].islower():
					msub = msub.lower()
				converions[msub.lower()] = sub
				subsequences.append(msub)
	return subsequences

def get_subseq_locations(sentence, single_words_allowed=False):
	"""Returns subsequences' locations from sentence."""
	subseq = []
	words = sentence.split()
	for i in range(len(words)):
		beg = len(' '.join(words[0:i])) 
		if i != 0:
			beg += 1
		k = i if not single_words_allowed else i+1
		for j in range(k, len(words)):
			end = len(' '.join(words[i:j+1]))
			subseq.append((beg, beg+end)) 	
	return subseq

def get_out_locations(out, t_sentence):
	"""Returns locations at with out is present in t_sentence"""
	t_sentence = t_sentence.lower()
	out = out.lower()
	locations = []
	starti = 0
	while True:
		beg = t_sentence.find(out[starti:])
		if beg == -1 or starti >= len(out):
			break
		if (beg == 0 or t_sentence[beg-1] == " ") \
			and (beg+len(out) == len(t_sentence) or t_sentence[beg+len(out)] in [" ", ",", ".", "!"]):	#The word ends
			locations.append((beg, beg+len(out)))
		starti += len(out)
	return locations


def add_bpt_ept(tmxu, src, tgt, lp, out_locations): 
		"""Adds <bpt>, <ept> tags to tmx unit."""
		src_pts = []
		tgt_pts = []
		i,j,x = 1,1,1

		for s, locs in out_locations.iteritems():
			src_pts.append([s[0], 'bpt', i, x])
			src_pts.append([s[1], 'ept', i])
			for loc in locs:
				tgt_pts.append([loc[0], 'bpt', j, x])
				tgt_pts.append([loc[1], 'ept', j])
				j += 1
			i += 1
			x += 1
		
		src_pts.sort()
		tgt_pts.sort()

		for i in range(2):
			if i == 0:
				pts = src_pts
				src_dom = tmxu.get_source_dom()
				seg = list(src_dom.iter('seg'))[0]
				initial_text = src
			else:
				pts = tgt_pts
				tgt_dom = tmxu.get_target_dom()
				seg = list(tgt_dom.iter('seg'))[0]
				initial_text = tgt
			seg.clear()

			if pts == []:
				seg.text = initial_text
			else:
				seg.text = initial_text[0:pts[0][0]].strip()
				for p in range(len(pts)):
					ele = etree.Element(pts[p][1])
					ele.attrib['i'] = str(pts[p][2])
					if pts[p][1] == 'bpt':
						ele.attrib['x'] = str(pts[p][3])
						ele.attrib['type'] = 'apertium-'+lp
					if p != len(pts) - 1: 
						ele.tail = initial_text[pts[p][0]: pts[p+1][0]].strip()
					seg.append(ele)

				ele.tail = initial_text[pts[-1][0]:].strip()
				