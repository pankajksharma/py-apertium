from translate.storage.tmx import tmxfile
from lxml import etree 

class TMXFile(tmxfile):
	"""Improved tmxfile"""
	def parse(self, xml):
		"""Populates this object from the given xml string"""
		if not hasattr(self, 'filename'):
			xml = open(xml, 'r')
			xml.seek(0)
			posrc = xml.read()
			xml = posrc
		if etree.LXML_VERSION >= (2, 1, 0): 
			parser = etree.XMLParser(strip_cdata=False)
		else:
			parser = etree.XMLParser()
		self.document = etree.fromstring(xml, parser).getroottree()
		self._encoding = self.document.docinfo.encoding
		self.initbody()
		assert self.document.getroot().tag == self.namespaced(self.rootNode)
		for entry in self.document.getroot().iterdescendants(self.namespaced(self.UnitClass.rootNode)):
			term = self.UnitClass.createfromxmlElement(entry)
			self.addunit(term, new=False) 

	def save(self, filename):
		op = open(filename, 'w')
		op.write(str(self))
		op.close()

