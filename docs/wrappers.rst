pysqlw wrappers
===============

.. |br| raw:: html
	
	<br />

.. note::
	These wrappers are more like *meta-wrappers*. They're just an easy way to create and connect to a wrapped database.
	The sqlite meta-wrapper just wraps the ``sqlite3`` module, the mysql wrapper just wraps (if you have it) the ``MySQLdb`` module.

Currently, there are only two supported meta-wrappers, and these are ``sqlite`` and ``mysql``.

Wrapper structure
-----------------

Meta-wrappers are fairly easy to implement yourself, they have three functions/properties. |br|
These are ``required``, ``connect()`` and ``format(item)``. They're fairly self explanatory, but will be documented regardless.

All meta-wrappers should subclass the ``sqltype`` class of pysqlw.

Naming
^^^^^^
A meta-wrapper is required to be in a file called ``<wrapper>w.py``, with a class by the same name inside. *e.g.*, ``sqlitew.py`` -> ``class sqlitew`` |br|
This simply allows the wrapper types to be imported dynamically at runtime, without any hardcoding or hackery.

When a script creates a pysqlw object, they pass in the ``db_type``, which is the meta-wrapper name, minus the trailing ``w``. |br|
You have the file ``sqlitew.py``, and the inner-class ``class sqlitew``, so you create the object like: ``pysqlw.pysqlw(db_type="sqlite")``; easy!

required()
^^^^^^^^^^
This property returns a list of variables the meta-wrapper needs to be passed in with the kwargs.

For example, if this returned: ``['db_host', 'db_port']``, the script would have to specify: ``pysqlw.pysqlw(db_type="...", db_host="..." db_port="...")``

connect()
^^^^^^^^^
This connects to the database, and stores the database connection object, aswell as the database cursor, to execute queries.

It should return a boolean value based on the success of the connection. Connected to the database? ``True``; something went wrong? ``False``.

format()
^^^^^^^^
This returns a string value, which the database uses to bind queries to; for example sqlite uses ``?``, MySQL uses ``%s``


Wrapper example
---------------

This is the mysql meta-wrapper that pysqlw provides.

.. code-block:: python
	:linenos:

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

See how easy it is to meta-wrap?

Notes
^^^^^
* Arguments passed in are stored in the ``self.args`` dictionary. Use this to access params given to ``pysqlw.pysqlw(...)``.