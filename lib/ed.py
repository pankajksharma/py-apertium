class memoize(dict):
	def __init__(self, func):
		self.func = func

	def __call__(self, *args):
		return self[args]

	def __missing__(self, key):
		result = self[key] = self.func(*key)
		return result

def subst_cost(x,y):
	if x == y: 
		return 0 
	return 1

@memoize
def edit_distance(target, source):
   """ Minimum edit distance. Straight from the recurrence."""
   i = len(target)
   j = len(source)
   if i == 0:  return j
   elif j == 0: return i
   return(min(edit_distance(target[:i-1],source)+1,
              edit_distance(target, source[:j-1])+1,
              edit_distance(target[:i-1], source[:j-1])+
              subst_cost(source[j-1], target[i-1])))
