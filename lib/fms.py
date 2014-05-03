from ed import edit_distance

class FMS(object):
	def __init__(self, source_sentence, target_sentence):
		"""Class for calculating fuzzy match score between source and target sentences."""
		self._src = tuple(source_sentence.split())
		self._tgt = tuple(target_sentence.split())

	def calculate(self):
		self._ed = edit_distance(self._src, self._tgt) * 1.0
		self._max_len = len(self._src) if len(self._src) > len(self._tgt) else len(self._tgt)
		self.fms = 1.0 - (self._ed / self._max_len)
		return self.fms
