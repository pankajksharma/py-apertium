import re, sys

def preprocess(sentence):
	"""Preprocesses the sentence to remove extra spaces."""
	sentence = sentence.strip()
	rex = re.compile(r'\s+')
	return rex.sub(' ', sentence)

def assertion(condition, statement):
	"""Checks condition and exits with NZ exit if it's not True."""
	if not condition:
		sys.stderr.write(statement+"\nexiting...")
		exit(1)

def is_subsegment(segment, sentence):
	"""Checks for subsegments."""
	seg, sen = segment.lower(), sentence.lower()
	if seg not in sen:
		return False
	return True

def get_subsegment_locs(segment, sentence):
	"""Returns locations of segment in sentence."""
	seg, sen = segment.lower().split(), sentence.lower().split()
	locs, a, b = [], 0, 0
	while a < len(sen):
		if sen[a] == seg[b]:
			b += 1
		else:
			b = 0
		if b == len(seg):
			locs.append((a-b+1, a))
			b = 0
		a += 1
	return locs

def patch(t_app, tau, tau1, covered_pos):
	print(t_app, tau, tau1)
	(a,b) = tau
	t_app = t_app.split()

	if(any(a<=c<=b for c in covered_pos)):
		return None, None
	seg = tau1.split()

	print(a,b, seg, t_app[a:b+1])
	for i in range(a, b+1):
		try:
			if t_app[i].lower() != seg[i-a].lower():
				covered_pos.append(i)
		except:
			covered_pos.append(i)
			
	seg = ' '.join(t_app[a:b+1])
	seg_left = ' '.join(t_app[:a])
	seg_right = ' '.join(t_app[b+1:])

	if seg_left != '':
		tau1 = tau1.lower()
	return (seg_left + ' ' + tau1 + ' ' + seg_right).strip(), covered_pos

