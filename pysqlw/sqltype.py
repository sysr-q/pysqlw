# -*- coding: utf-8 -*-
# The base for SQL wrappers to implement.
class sqltype:
	""" pysqlw.sqltype is a parent class to the meta-wrappers
		provided by pysqlw. This allows for simple integration
		into the pysqlw meta-wrapper family.
	"""

	def __init__(self, **kwargs):
		""" Check that all required arguments are given.
			If they are, keep going, otherwise raise a ValueError.

			:raises ValueError: If a required argument is not given
		"""
		for req in self.required:
			if req in kwargs:
				continue
			raise ValueError('{0} was not passed, but it is required.'.format(req))
		self.args = kwargs

	@property
	def required(self):
		""" What do we *require* to be in the kwargs?
			As in, without these, nothing will function.

			:return: required arguments in kwargs
			:rtype: list
		"""
		return []

	def connect(self):
		""" Connect to the database and perform any required actions to setup.
			
			:return: a (database, cursor) tuple, or False if something went wrong
			:rtype: tuple or False
		"""
		return False

	def format(self, item):
		""" In a prepared statement, what does this database use for param binding?
			e.g., '?' for sqlite, '%s' for MySQL.
			
			:return: The format string for param binding
			:rtype: string
		"""
		return '?'