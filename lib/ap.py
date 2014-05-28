import subprocess, re

class Apertium(object):
	"""Base Class for Apertium Translations"""
	def __init__(self, s_lang, t_lang):
		self.s_lang = s_lang
		self.t_lang = t_lang

	def translate(self, src, dir=None):
		"""Translates src (source sentence) to t_lang (Target Language)"""
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
		(out,err) = process.communicate(bytearray(src, 'utf-8'))
		out, err = out.decode('utf-8'), err.decode('utf-8')
		return (out, err)

	def test_lp(self, directory):
		"""Test for installation of Language Pair."""
		try:
			process = subprocess.Popen(["apertium", "-d", directory,
									"{0}-{1}".format(self.s_lang, self.t_lang)], 
									stdout = subprocess.PIPE,
									stdin = subprocess.PIPE,
									stderr = subprocess.PIPE
							)
			(out,err) = process.communicate(bytearray("", 'utf-8'))
			out, err = out.decode('utf-8'), err.decode('utf-8')
			return (out, err)
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

	def check_installations(self, lp_dir=None):
		"""Checks for apertium and lp installations."""
		lp = "{0}-{1}".format(self.s_lang, self.t_lang)
		(lps,err) = self.test_apertium()

		if err.decode('utf-8') != '':
			return (False, "Apertium can't be found. Please check the installation.")
		if not lp_dir:
			pairs = re.findall(r'\w+-\w+', lps.decode('utf-8'))
			if lp not in pairs:
				return (False, "Language Pair not installed.")
		else:
			(out,err) = self.test_lp(lp_dir)
			if out != '':
				return (False, "Language Pair not found in directory '%s'" %lp_dir)
		return (True, "")
