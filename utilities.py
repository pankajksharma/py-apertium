import re

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
		k = i if single_words_allowed else i+1
		for j in range(k, len(words)):
			subseq += ' '.join(words[i:j+1])+'.|'
	return subseq

def get_pairs(inp, out, sentence, converions, reverse=None):
	"""Prints Languge pair sequences."""	
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
				# print ('("{0}", "{1}")'.format(sub, msub)) 
				# if not converions.has_key(sub.lower()):
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
				# print ('("{0}", "{1}")'.format(msub, sub)) 
				# if not converions.has_key(msub.lower()):
				converions[msub.lower()] = sub
				subsequences.append(msub)
	return subsequences
	
