from translate.storage.tmx import tmxunit
from lxml import etree 

class TMXUnit(tmxunit):
	"""Improved tmxunit"""
	def __init__(self, sentence, segtype="sentence", tuid=None):
		tmxunit.__init__(self, "")
		self.tuid = tuid
		self.sentence = sentence
		self._set_property("segtype", segtype)
		self._set_property("tuid", self.getid())

	def getid(self):
		return self.tuid or self.sentence

	def addprop(self, type, value):
		"""Add a property under a "prop" tag."""
		value = value.decode("utf-8")
		prop = etree.SubElement(self.xmlelement, self.namespaced("prop"))
		prop.attrib[type] = type.strip() 
		prop.text = value.strip()
