#! /bin/env python
#
## Python Implementation of Wagner Fischer algorithm for finding edit distance between two sentences.
## Author: pankajksharma

import numpy

class EDWF(object):
	def __init__(self, source, target):
		self._src = source
		self._tgt = target

	def get_distance(self):
		sl, tl = len(self._src)+1, len(self._tgt)+1
		mat = numpy.zeros((sl, tl))

		for i in range(sl):
			mat[i,0] = i
		
		for i in range(tl):
			mat[0,i] = i

		for j in range(1, tl):
			for i in range(1, sl):
				if self._src[i-1] == self._tgt[j-1]:
					mat[i,j] = mat[i-1,j-1]
				else:
					mat[i,j] = min([mat[i-1,j]+1, mat[i, j-1]+1, mat[i-1, j-1]+1])

		return mat[sl-1, tl-1]

