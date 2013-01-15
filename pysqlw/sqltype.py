# -*- coding: utf-8 -*-
# The base for SQL wrappers to implement.
class sqltype:
	def __init__(self, **kwargs):
		for req in self.required:
			if req in kwargs:
				continue
			raise ValueError('{0} was not passed, but it is required.'.format(req))
		self.args = kwargs

	@property
	def required(self):
		""" What do we *require* to be in the kwargs?
			As in, without these, nothing will function.

			Return a list with required strings.
		"""
		return []

	def connect(self):
		""" Connect to the database and perform any required actions to setup.
			Return a (database, cursor) tuple, or False if something went wrong.
		"""
		return False

	def format(self, item):
		""" In a prepared statement, what does this database use for formatting?
			e.g., '?' for sqlite, '%s' for MySQL.
			Return a string.
		"""
		return '?'