
def cover_all_mismatches(p, mismatches, sigma):
	(a, b) = sigma
	mismatches_le_p = [ m for m in mismatches if m <= p ]
	return all(b >= m for m in mismatches_le_p)

def coverage(mismatches, sigma):
	(a, b) = sigma
	mismatches_le_b = [ m for m in mismatches if m <= b ]
	return (abs(b-a)+1.0)/(len(mismatches_le_b)+1.0)

def contexts(t_app, tau):
	(a,b) = tau
	t_app = t_app.split()
	sen_len = len(t_app)*1.0
	seg_left = t_app[:a]
	seg_right = t_app[b+1:]
	return (len(seg_left)/sen_len, len(seg_right)/sen_len)


def get_features(p, sigma, mismatches, new_sen, old_sen, tau):
	return (cover_all_mismatches(p, mismatches, sigma),
			coverage(mismatches, sigma),
			contexts(old_sen, tau))
