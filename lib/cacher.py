import sqlite3
from os.path import isfile

class Cacher(object):
	"""Cacher for caching phrases using sqlite3"""
	def __init__(self, sl, tl, file=':memory:'):
		self._sl = sl.lower()
		self._tl = tl.lower()

		new = False
		if not isfile(file):
			new = True
		self._conn = sqlite3.connect(file)
		self._conn.text_factory = str
		self._cursor = self._conn.cursor()
		if new:
			self._create_tables()

	def _create_tables(self):
		self._cursor.execute(
			'''
				CREATE TABLE phrases (sl text, tl text, sp text, tp text)
			'''
		)
		self._cursor.execute(
			'''
				CREATE UNIQUE INDEX phraseindex ON phrases(sl, tl, sp)
			'''
		)
		self._conn.commit()

	def insert(self, phrase, meaning):
		values = (self._sl, self._tl, phrase.lower().strip(), meaning.lower().strip())
		self._cursor.execute(
			'''
				INSERT INTO phrases VALUES(?, ?, ?, ?)
			''',
			values
		)
		self._conn.commit()

	def retrieve(self, phrase):
		values = (self._sl, self._tl, phrase.lower().strip())
		self._cursor.execute(
			'''
				SELECT tp FROM phrases WHERE sl = ? AND tl = ? AND sp = ? 
			''',
			values
		)
		return self._cursor.fetchone()
