# -*- coding: utf-8 -*-
class pysql_wrapper:
	_instance = None

	def __init__(self, **kwargs):
		# The internal database connection.
		# Can be either MySQL or sqlite, it doesnt matter.
		self._dbc = None

		# The database cursor. We'll use this to actually query stuff.
		self._cursor = None
		
		# Is this a MySQL database? We'll need to tweak some stuff depending.
		self._is_mysql = False
		
		# The finalised query string to send to the dbc.
		self._query = ""
		
		# A dictionary of 'field' => 'value' which are used in the WHERE clause.
		self._where = {}
		
		# An internal counter of modified rows from the last statement.
		self._affected_rows = 0
		
		# Stuff we won't need unless we're using MySQL.
		self._db_host = None
		self._db_user = None
		self._db_pass = None
		self._db_name = None
		# Stuff we won't need unless we're using sqlite3
		self._db_path = None

		# Just so we know stuff worked after the connection.
		self._db_version = "SOMETHING WENT WRONG!"

		# Do some checks depending on what we're doing.
		if 'db_type' in kwargs:
			_db_type = kwargs['db_type']
			if _db_type.lower() is 'mysql':
				for db in ('db_host', 'db_user', 'db_pass', 'db_name'):
					if db not in kwargs:
						# If they miss something, we can't connect to MySQL.
						raise ValueError('No {0} was passed to pysql_wrapper.'.format(db))
					else:
						# We only want strings!
						if type(kwargs.get(db)) != str:
							raise TypeError('{0} was passed, but it isn\'t a string.')
				self._db_host = kwargs.get('db_host')
				self._db_user = kwargs.get('db_user')
				self._db_pass = kwargs.get('db_pass')
				self._db_name = kwargs.get('db_name')
				self._is_mysql = True
			elif _db_type.lower() in ('sqlite', 'sqlite3'):
				self._is_mysql = False

		if self._is_mysql == False and 'db_path' not in kwargs:
			# How will we know what database file to use otherwise?
			raise ValueError('sqlite was selected, but db_path was not given.')
		else:
			self._db_path = kwargs.get('db_path')
			if type(self._db_path) is not str:
				raise TypeError('db_path was passed, but it isn\'t a string.')

		if self._is_mysql:
			self._connect_mysql()
		else:
			self._connect_sqlite()

	def __del__(self):
		# If this isn't called, it shouldn't really matter anyway.
		# If it is, let's tear down our connections.
		if self._dbc:
			self._dbc.close()

	def _sqlite_dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def _connect_sqlite(self, force=False):
		'''Connect to the sqlite database.

			This function also grabs the cursor and updates the _db_version
		'''
		import sqlite3
		self._dbc = sqlite3.connect(self._db_path)
		self._dbc.row_factory = self._sqlite_dict_factory
		self._cursor = self._dbc.cursor()
		self._cursor.execute('SELECT SQLITE_VERSION()')
		self._db_version = self._cursor.fetchone()

	def _connect_mysql(self, force=False):
		'''Connect to the MySQL database.

			This function also grabs the cursor and updates the _db_version 
		'''
		import MySQLdb
		self._dbc = MySQLdb.connect(self._db_host, self._db_user, self._db_pass, self._db_name)
		self._cursor = self._dbc.cursor(MySQLdb.cursors.DictCursor)
		self._cursor.execute('SELECT VERSION()')
		self._db_version = self._cursor.fetchone()

	def _reset(self):
		'''Reset the given bits and pieces after each query.
		'''
		self._where = {}
		self._query = ""
		return self

	def where(self, field, value):
		'''Add a conditional WHERE statement. You can chain multiple where() calls together.

			Example: pysql.where('id', 1).where('foo', 'bar')
			Param: 'field' The name of the database field.
			Param: 'value' The value of the database field.
			Return: Instance of self for chaining where() calls
		'''
		self._where[field] = value
		return self

	def get(self, table_name, num_rows = False):
		'''SELECT some data from a table.

			Example: pysql.get('table', 1) - Select one row
			Param: 'table_name' The name of the table to SELECT from.
			Param: 'num_rows' The (optional) amount of rows to LIMIT to.
			Return: The results of the SELECT.
		'''
		self._query = "SELECT * FROM `{0}`".format(table_name)
		stmt = self._build_query(num_rows=num_rows)
		res  = self._execute(stmt)
		self._reset()
		return res

	def insert(self, table_name, table_data):
		'''INSERT data into a table.

			Example: pysql.insert('table', {'id': 1, 'foo': 'bar'})
			Param: 'table_name' The table to INSERT into.
			Param: 'table_data' A dictionary of key/value pairs to insert.
			Return: The results of the query.
		'''
		self._query = "INSERT INTO `{0}`".format(table_name)
		stmt = self._build_query(table_data=table_data)
		res  = self._execute(stmt)
		self._reset()
		return res

	def update(self, table_name, table_data, num_rows = False):
		'''UPDATE a table. where() must be called first.

			Example: pysql.where('id', 1).update('table', {'foo': 'baz'})
			Param: 'table_name' The name of the table to UPDATE.
			Param: 'table_data' The key/value pairs to update. (SET `KEY` = 'VALUE')
			Param: 'num_rows' The (optional) amount of rows to LIMIT to.
			return True/False, indicating success.
		'''
		if len(self._where) == 0:
			return False
		self._query = "UPDATE `{0}` SET ".format(table_name)
		stmt = self._build_query(num_rows=num_rows, table_data=table_data)
		res  = self._execute(stmt)
		if self._affected_rows > 0:
			res = True
		else:
			res = False
		self._reset()
		return res

	def delete(self, table_name, num_rows = False):
		'''DELETE from a table. where() must be called first.

			Example: pysql.where('id', 1).delete('table')
			Param: 'table_name' The table to DELETE from.
			Param: 'num_rows' The (optional) amount of rows to LIMIT to.
			return True/False, indicating success.
		'''
		if len(self._where) == 0:
			return False
		self._query = "DELETE FROM `{0}`".format(table_name)
		stmt = self._build_query(num_rows=num_rows)
		res  = self._execute(stmt)
		if self._affected_rows > 0:
			res = True
		else:
			res = False
		self._reset()
		return res

	def escape(self, string):
		return self._dbc.escape_string(string)

	def query(self, q):
		'''Execute a raw query directly.

			Example: pysql.query('SELECT * FROM `posts` LIMIT 0, 15')
			Param: 'q' The query to execute.
			Return: The result of the query. Could be an array, True, False, anything, really.
		'''
		self._query = q
		res = self._execute(self._query)
		self._reset()
		return res

	def affected_rows(self):
		'''Grab the amount of rows affected by the last query.

			Return: The amount of rows modified.
		'''
		return self._cursor.rowcount

	def _execute(self, query):
		self._cursor.execute(query)
		if not self._is_mysql:
			self._dbc.commit()
		res = self._cursor.fetchall()
		self._affected_rows = int(self._cursor.rowcount)
		return res

	def _build_query(self, num_rows = False, table_data = False):
		'''Abstracted method which builds the SQL query, including the WHERE cause when required.

				Param: 'num_rows' The (optional) number of rows to LIMIT to.
				Param: 'table_data' The (optional) data to use if INSERTing.
				Return: The query statement string.
		'''
		has_where = False
		if len(self._where) > 0:
			has_where = True
		has_table_data = False
		if type(table_data) == dict:
			has_table_data = True

		if has_where:
			if 'UPDATE' in self._query:
				i = 1
				for key, val in table_data.iteritems():
					if not isinstance(val, int):
						# Wrap non-integers in single quotes.
						val = "'{0}'".format(val)
					if i == len(table_data):
						self._query += "`{0}` = {1}".format(key, val)
					else:
						self._query += "`{0}` = {1}, ".format(key, val)
					i += 1
			# Setup our WHERE clause.
			self._query += " WHERE "
			where_clause = []
			for key, val in self._where.iteritems():
				if not isinstance(val, int):
					# Wrap non-integers in single quotes.
					val = "'{0}'".format(val)
				where_clause.append("`{0}` = {1}".format(key, val))
			self._query += ' AND '.join(where_clause)

		if has_table_data:
			if 'INSERT' in self._query:
				keys = table_data.keys()
				vals = table_data.values()
				num  = len(table_data)
				for count, key in enumerate(keys):
					# Wrap column names in backticks.
					keys[count] = "`{0}`".format(key)
				for count, val in enumerate(vals):
					# Wrap non-integers in single quotes.
					if not isinstance(val, int):
						vals[count] = "'{0}'".format(val)
				self._query += " ({0}) VALUES ({1})".format(
					', '.join(str(x) for x in keys),
					', '.join(str(x) for x in vals)
				)

		if num_rows:
			self._query += " LIMIT {0}".format(num_rows)

		return self._query