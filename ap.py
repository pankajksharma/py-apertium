import subprocess, shlex

class Apertium(object):
	"""Base Class for Apertium Translations"""
	def __init__(self, s_lang, t_lang):
		self.s_lang = s_lang
		self.t_lang = t_lang

	def convert(self, src):
		"""Converts src (source sentence) to t_lang (Target Language)"""
		process = subprocess.Popen(["apertium", 
							"{0}-{1}".format(self.s_lang, self.t_lang)],
							stdin = subprocess.PIPE,
							stdout = subprocess.PIPE,
							stderr = subprocess.PIPE
						)
		return process.communicate(input=src)

	def test(self, slc):
		"""Test for installation of Language Pair."""
		devnull = open('/dev/null', 'w')
		try:
			process = subprocess.Popen(["apertium","-l"], 
									stdout = subprocess.PIPE,
									stderr = subprocess.PIPE
								)
			return process.communicate()
		except:
			return (None, None)