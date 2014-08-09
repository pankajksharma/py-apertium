from lib.ed import edit_distance
from lib.edwf import EDWF

class FMS(object):
	def __init__(self, source_sentence, target_sentence):
		"""Class for calculating fuzzy match score between source and target sentences."""
		self._src = tuple(source_sentence.split())
		self._tgt = tuple(target_sentence.split())

	def _max_len(self):
		return max([len(self._src), len(self._tgt)])*1.0

	def get_max_fms(self):
		"""returns max possible value of fms without calculating the actual value."""
		return 1.0 - (abs(len(self._src) - len(self._tgt)) / self._max_len())

	def calculate(self):
		"""returns FMS using old recursion method."""
		self._ed = edit_distance(self._src, self._tgt) * 1.0
		self.fms = 1.0 - (self._ed / self._max_len())
		return self.fms

	def calculate_using_wanger_fischer(self):
		"""returns FMS using Wanger Fischer Algorithm."""
		wf = EDWF(self._src, self._tgt)
		ed = wf.get_distance()*1.0
		return 1.0 - (ed / self._max_len())

	def calculate_using_wagner_fischer(self):
		"""returns FMS using Wanger Fischer Algorithm."""
		wf = EDWF(self._src, self._tgt)
		ed = wf.get_distance()*1.0
		return 1.0 - (ed / self._max_len())		
