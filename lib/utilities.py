import re

def preprocess(sentence):
	"""Preprocesses the sentence to remove extra spaces."""
	sentence = sentence.strip()
	rex = re.compile(r'\s+')
	return rex.sub(' ', sentence)

def assertion(condition, statement):
	"""Checks condition and exits with NZ exit if it's not True."""
	if not condition:
		print (statement+"\nexiting...")
		exit(1)
