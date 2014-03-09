import re

def preprocess(sentence):
	"""Preprocesses the sentence to remove extra spaces."""
	sentence = sentence.strip()
	rex = re.compile(r'\s+')
	return rex.sub(' ', sentence)

def print_sequences(inp, out, t_sentence, reverse=None):
	"""Prints Languge pair sequences."""
	if not reverse:
		for sub, msub in zip(inp.split('.|'), out.split('.|')):
			sub, msub = preprocess(sub), preprocess(msub)
			if sub != "" and msub != "" and msub.lower() in t_sentence:
				if sub[0].islower() and len(msub) > 1:
					msub = msub[0].lower() + msub[1:]
				elif sub[0].islower():
					msub = msub.lower()
				print ('("{0}", "{1}")'.format(sub, msub)) 
	else:
		for sub, msub in zip(inp.split('.|'), out.split('.|')):
			sub, msub = preprocess(sub), preprocess(msub)
			if sub != "" and msub != "" and msub.lower() in t_sentence:
				if sub[0].islower() and len(msub) > 1:
					msub = msub[0].lower() + msub[1:]
				elif sub[0].islower():
					msub = msub.lower()
				print ('("{0}", "{1}")'.format(msub, sub)) 
	
