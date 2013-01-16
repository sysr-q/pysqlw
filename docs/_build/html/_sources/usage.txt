Usage
=====

.. _pypi: https://pypi.python.org/pypi/pysqlw
.. |br| raw:: html
	
	<br />

Install & setup
---------------

What good is pysqlw if you can't actually use it, right? Thankfully, pysqlw is a breeze to install and setup!

pysqlw is on `pypi`_, so you just have to ``pip install pysqlw``, and pip does the rest! |br|
Then you just have to ``import pysqlw``, and you're set.

Setup
^^^^^
Generally, you'll simply create a pysqlw object by making an instance of ``pysqlw.pysqlw``. |br|
The actual things you pass to the initialisation will differ based on what type of database you want to work with.

.. code-block:: python

	import pysqlw
	p = pysqlw.pysqlw(...)

Setup for sqlite
^^^^^^^^^^^^^^^^

.. code-block:: python
	:linenos:

	import pysqlw

	# Pass in an absolute path to your sqlite3 database file.
	p = pysqlw.pysqlw(db_type="sqlite", db_path="/home/user/pysqlw.db")

Setup for MySQL
^^^^^^^^^^^^^^^

.. code-block:: python
	:linenos:

	import pysqlw

	# Since we're using MySQL, we have to pass in relevant information; host, user, pass, database
	conf = {
		"db_type": "mysql",
		"db_host": "localhost",
		"db_user": "foo",
		"db_pass": "bar",
		"db_name": "example"
	}
	p = pysqlw.pysqlw(**conf)

Querying your database
----------------------
For reference, the ``p`` object we're working with is from ``p = pysqlw.pysqlw(...)``. |br|
``table_name`` is just a fictional table in a non-existant database. Swap it out for your tables real name.

SELECT
^^^^^^

.. code-block:: python
	:linenos:

	# SELECT all rows from the table
	rows = p.get('table_name')

	# SELECT only the first five rows
	rows = p.get('table_name', 5)

	# SELECT only the rows where: `foo` = 'bar'
	rows = p.where('foo', 'bar').get('table_name')

INSERT
^^^^^^

.. code-block:: python
	:linenos:

	# This is the data we're going to INSERT into the table.
	# Keys relate to table column names, values are what we're inserting there.
	data = {
		"foo": "bar",
		"baz": "qux",
		"moo": 1
	}
	if p.insert('table_name', data):
		# Success!

UPDATE
^^^^^^
You **must** call ``where()`` before you can update.

.. code-block:: python
	:linenos:

	# k/v relates to column-name/value, as above
	data = {
		"foo": "baz",
		"moo": 7
	}

	# UPDATE all rows where: `name` = 'John'
	if p.where('name', 'John').update('table_name', data):
		# Success!

	# UPDATE only a single row where: `name` = 'Pete'
	if p.where('name', 'Pete').update('table_name', data, 1):
		# Success!

DELETE
^^^^^^
You **must** call ``where()`` before you can delete.

.. code-block:: python
	:linenos:

	# DELETE any row where: `name` = 'John'
	if p.where('name', 'Pete').delete('table_name'):
		# Success!

	# DELETE only a single row where: `id` = 1
	if p.where('id', 1).delete('table_name'):
		# Success!

WHERE
^^^^^
This adds a WHERE query to your SQL. You can dictate what rows and columns to operate on with this. |br|
There are two ways to work with your ``where()`` call.

.. code-block:: python
	
	# On separate lines:
	p.where('id', 1)
	p.where('foo', 'bar')
	rows = p.get('table_name')

.. code-block:: python
	
	# Chained together
	rows = p.where('id', 1).where('foo', 'bar').get('table_name')

Affected rows
^^^^^^^^^^^^^
Want to know how many rows you modified with the last executed query? This will show you just that.

.. code-block:: python
	
	data = {
		"surname": "Smith"
	}
	if p.where('name', 'John').update('table_name', data):
		# Success!
		print 'Affected rows:', p.affected_rows()

Escape unsafe data
^^^^^^^^^^^^^^^^^^
Due to how bound queries work, the data you pass in is actually transparently escaped for you; you don't have to do anything to be safe.
If for some reason you still want to escape data, use the ``escape(var)`` method. It passes through your information to the database's escape method, so we can't guarantee that it's secure.

.. code-block:: python
	
	# OH NO, THIS PERSON HAS SOME SCARY QUOTES!
	user = "Some'Dangerous'Username"
	# Not today, hacker scum!
	safe_user = p.escape(user)
	# Now you're safe from the menaces of society.
	print safe_user

Your own query
^^^^^^^^^^^^^^
.. warning::
	This doesn't do any behind-the-scenes binding, escaping, or anything of the sort. It's **your** job to keep it safe.

If for some reason, you wish to execute a manual query (joins, union selects, other query wizardry), you'll have to use the ``query(q)`` method. Poor you!

.. code-block:: python
	
	data = p.query('SELECT `this` FROM `that` UNION SELECT `this` FROM `other`')
	# Data is whatever your query might return.