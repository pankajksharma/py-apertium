import re, sys

def preprocess(sentence):
	"""Preprocesses the sentence to remove extra spaces."""
	sentence = sentence.strip()
	rex = re.compile(r'\s+')
	return rex.sub(' ', sentence)

def assertion(condition, statement):
	"""Checks condition and exits with NZ exit if it's not True."""
	if not condition:
		print >> sys.stderr, (statement+"\nexiting...")
		exit(1)

def is_subsegment(segment, sentence):
	"""Checks for subsegments."""
	seg, sen = segment.lower(), sentence.lower()
	if seg not in sen:
		return False
	return True

