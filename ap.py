import subprocess

class Apertium(object):
	"""Base Class for Apertium Translations"""
	def __init__(self, s_lang, t_lang):
		self.s_lang = s_lang
		self.t_lang = t_lang

	def convert(self, src, dir=None):
		"""Converts src (source sentence) to t_lang (Target Language)"""
		if dir:
			process = subprocess.Popen(["apertium", "-d", dir, 
							"{0}-{1}".format(self.s_lang, self.t_lang)],
							stdin = subprocess.PIPE,
							stdout = subprocess.PIPE,
							stderr = subprocess.PIPE
						)
		else:
			process = subprocess.Popen(["apertium", 
							"{0}-{1}".format(self.s_lang, self.t_lang)],
							stdin = subprocess.PIPE,
							stdout = subprocess.PIPE,
							stderr = subprocess.PIPE
			)
		return process.communicate(input=src)

	def test_lp(self, dir):
		"""Test for installation of Language Pair."""
		try:
			process = subprocess.Popen(["apertium", "-d", dir,
									"{0}-{1}".format(self.s_lang, self.t_lang)], 
									stdout = subprocess.PIPE,
									stdin = subprocess.PIPE,
									stderr = subprocess.PIPE
							)
			return process.communicate("")
		except:
			return (None, None)

	def test_apertium(self):
		"""Test for installation of Apertium."""
		try:
			process = subprocess.Popen(["apertium","-l"], 
									stdout = subprocess.PIPE,
									stderr = subprocess.PIPE
								)
			return process.communicate()
		except:
			return (None, None)
