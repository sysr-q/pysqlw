# -*- coding: utf-8 -*-
# Copyright (C) 2012 Christopher Carter <chris@gibsonsec.org>
# Licensed under the MIT License.


class pysqlw:
    """ pysqlw is a meta-wrapper to sqlite and mysql (+ others) modules,
        allowing for easy interaction with these modules, and a clean
        front-end for building SQL queries, without needing perfect
        knowledge of how SQL pulls together.
    """

    def __init__(self, debug=False, **kwargs):
        """ Create required instance objects, and attempt to connect to
            the database by importing the wrapper.

            :param debug: allows debug messages to print to stdout
            :type debug: boolean
            :param **kwargs: keyword args, passed along to the wrappers
        """
        # Are we gonna print various debugging messages?
        self.debug = debug

        # The wrapper and wrapper instance we're using. sqlitew, mysqlw, etc.
        # Imported at runtime and used to make objects.
        self._wrapper = None
        self.wrapper = None

        # The finalised query string to send to the dbc.
        self._query = ""
        self._query_type = ""

        # A dictionary of 'field' => 'value' which are used in the WHERE clause.
        self._where = {}

        # An internal counter of modified rows from the last statement.
        self._affected_rows = 0

        # Do some checks depending on what we're doing.
        if 'db_type' not in kwargs:
            raise ValueError("'db_type' not passed when required")
        kwargs['db_type'] = kwargs['db_type'].lower()
        self._db_type = kwargs.get('db_type')

        try:
            # We're already in the pysqlw package, so just: import wrapperw
            self._wrapper = __import__('{0}w'.format(kwargs.get('db_type')), globals(), locals())
            # Pull out the wrapper class
            self._wrapper = getattr(self._wrapper, '{0}w'.format(kwargs.get('db_type')))
        except ImportError as e:
            raise ImportError('Database wrapper "{0}" does not exist or is incorrectly packaged'.format(kwargs.get('db_type')))
        except AttributeError as e:
            raise AttributeError('Database wrapper "{0}" exists but is incorrectly written'.format(kwargs.get('db_type')))

        self._connect(**kwargs)

        if not self.wrapper.connect():
            raise Exception('Unable to connect to database. ({0})'.format(self._db_type))

    def _debug(self, *stuff):
        """Print debugging messages, if enabled"""
        if not self.debug:
            return
        print '[ ? ]', ' '.join([str(s) for s in stuff])

    def _connect(self, **kwargs):
        """Instanciate a new wrapper instance"""
        self.wrapper = self._wrapper(**kwargs)

    def __del__(self):
        """Simply calls self.close()"""
        self.close()

    def __enter__(self):
        """Does nothing, the connection is already made"""
        return self

    def __exit__(self, type_, value_, traceback_):
        """Simply calls self.close()"""
        self.close()

    def close(self):
        """Tear down the database connection and assign None to unneeded references"""
        if not self.wrapper:
            return

        if self.wrapper.dbc:
            self.wrapper.dbc.close()
        self.wrapper.dbc = None
        self.wrapper.cursor = None
        self.wrapper = None

    def _reset(self):
        """Reset the query variables after each query"""
        self._where = {}
        self._query = ""
        self._query_type = ""
        return self

    def where(self, field, value):
        """ Add a conditional WHERE statement. You can chain multiple where() calls together.

            :example: p.where('id', 1).where('foo', 'bar')
            :param field: The name of the database field
            :param value: The value of the database field
            :return: Instance of self for chaining where() calls
        """
        self._where[field] = value
        return self

    def get(self, table_name, num_rows=False):
        """ SELECT some data from a table.

            :example: p.get('table') - Select all rows
            :example: p.get('table', 1) - Select one row
            :param table_name: The name of the table to SELECT from
            :param num_rows: The amount of rows to LIMIT to
            :type num_rows: integer or None
            :return: The results of the SELECT
        """
        self._query_type = 'select'
        self._query = "SELECT * FROM `{0}`".format(table_name)
        stmt, data = self._build_query(num_rows=num_rows)
        res = self._execute(stmt, data)
        self._reset()
        return res

    def insert(self, table_name, table_data):
        """ INSERT data into a table.

            :example: p.insert('table', {'id': 1, 'foo': 'bar'})
            :param table_name: The table to INSERT into
            :param table_data: A dictionary of key/value pairs to insert
            :return: True/False, indicating success
        """
        self._query_type = 'insert'
        self._query = "INSERT INTO `{0}`".format(table_name)
        stmt, data = self._build_query(table_data=table_data)
        res = self._execute(stmt, data)
        if self._affected_rows > 0:
            res = True
        else:
            res = False
        self._reset()
        return res

    def update(self, table_name, table_data, num_rows=False):
        """ UPDATE a table. where() must be called first.

            :example: p.where('id', 1).update('table', {'foo': 'baz'})
            :param table_name: The name of the table to UPDATE
            :param table_data: The key/value pairs to update. (SET `KEY` = 'VALUE')
            :param num_rows: The amount of rows to LIMIT to
            :type num_rows: integer or False
            :return: True/False, indicating success
        """
        if len(self._where) == 0:
            return False
        self._query_type = 'update'
        self._query = "UPDATE `{0}` SET ".format(table_name)
        stmt, data = self._build_query(num_rows=num_rows, table_data=table_data)
        res = self._execute(stmt, data)
        if self._affected_rows > 0:
            res = True
        else:
            res = False
        self._reset()
        return res

    def delete(self, table_name, num_rows=False):
        """ DELETE from a table. where() must be called first.

            :example: p.where('id', 1).delete('table')
            :param table_name: The table to DELETE from
            :param num_rows: The amount of rows to LIMIT to
            :type num_rows: integer or False
            :return: True/False, indicating success
        """
        if len(self._where) == 0:
            return False
        self._query_type = 'delete'
        self._query = "DELETE FROM `{0}`".format(table_name)
        stmt, data = self._build_query(num_rows=num_rows)
        res = self._execute(stmt, data)
        if self._affected_rows > 0:
            res = True
        else:
            res = False
        self._reset()
        return res

    def escape(self, string):
        """Escape deadly characters from a string"""
        return self.wrapper.dbc.escape_string(string)

    def query(self, q):
        """ Execute a raw query directly.

            :example: p.query('SELECT * FROM `posts` LIMIT 10, 15')
            :param q: The query to execute
            :return: The result of the query. Could be an array, True, False, anything, really
        """
        self._query_type = 'manual'
        self._query = q
        res = self._execute(self._query, data=None)
        self._reset()
        return res

    def affected_rows(self):
        """ Grab the amount of rows affected by the last query.

            :return: The amount of rows modified
            :rtype: int
        """
        return self.wrapper.cursor.rowcount

    def _execute(self, query, data=None):
        """ Internally pass through a query to the wrapped database

            :param query: The SQL query to execute
            :param data: List to pass to execution for binding
            :type data: list or None
            :return: The results of the query
        """
        if data is not None:
            self.wrapper.cursor.execute(query, data)
        else:
            self.wrapper.cursor.execute(query)
        if self._db_type == 'sqlite':
            self.wrapper.dbc.commit()
        res = self.wrapper.cursor.fetchall()
        self._affected_rows = int(self.wrapper.cursor.rowcount)
        return res

    def _build_query(self, num_rows=False, table_data=False):
        """ Build an SQL query from given query type, table data and where clauses.

            :param num_rows: The number of rows to LIMIT to
            :type num_rows: integer or False
            :param table_data: The key/value data to insert into a table
            :type table_data: dictionary or False
            :return: The built SQL query and the data to bind to the query
            :rtype: tuple
        """
        return_data = ()

        # e.g. -> UPDATE `table` SET `this` = ?, `that` = ?, `foo` = ? WHERE `id` = ?;

        # If they've supplied where() statements
        if len(self._where) > 0:
            keys = self._where.keys()
            # If they've supplied table data:
            if isinstance(table_data, dict):
                # We have to use our own counter because enumerate()
                # doesn't play nicely with iteritems()
                count = 1
                # If we're calling an UPDATE
                if self._query_type == 'update':
                    for key, val in table_data.iteritems():
                        format = self.wrapper.format(val)
                        if count == len(table_data):
                            self._query += "`{0}` = {1}".format(key, format)
                        else:
                            self._query += "`{0}` = {1}, ".format(key, format)
                        return_data = return_data + (val,)
                        count += 1
            self._query += " WHERE "
            where_clause = []
            for key, val in self._where.iteritems():
                format = self.wrapper.format(val)
                where_clause.append("`{0}` = {1}".format(key, format))
                return_data = return_data + (val,)
            self._query += ' AND '.join(where_clause)

        # If they've supplied table data.
        if isinstance(table_data, dict) and self._query_type == 'insert':
            keys = table_data.keys()
            vals = table_data.values()
            num = len(table_data)
            for count, key in enumerate(keys):
                # Wrap column names in backticks.
                keys[count] = "`{0}`".format(key)
            self._query += " ({0}) ".format(', '.join(keys))
            # Append VALUES (?,?,?) however many we need.
            format = ""
            for count, val in enumerate(vals):
                format += '{0},'.format(self.wrapper.format(val))
            format = format[:-1]

            self._query += "VALUES ({0})".format(format)
            for val in vals:
                return_data = return_data + (val,)

        # Do you want LIMIT with that, baby?!
        if num_rows:
            self._query += " LIMIT {0}".format(num_rows)
        return (self._query, return_data,)
