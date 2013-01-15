# -*- coding: utf-8 -*-
from sqltype import sqltype

class mysqlw(sqltype):
	@property
	def required(self):
		return ['db_host', 'db_user', 'db_pass', 'db_name']

	def connect(self):
		try:
			import MySQLdb
			self.dbc = MySQLdb.connect(self.args.get('db_host'), self.args.get('db_user'), self.args.get('db_pass'), self.args.get('db_name'))
			self.cursor = self.dbc.cursor(MySQLdb.cursors.DictCursor)
		except Exception as e:
			return False
		return True

	def format(self, item):
		return '%s'