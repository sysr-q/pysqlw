# -*- coding: utf-8 -*-
# Example for the pysql-wrapper class using sqlite3.

from pysql_wrapper import pysql_wrapper
import random # To populate the table.

# Create your pysql-wrapper instance!
pysql = pysql_wrapper(db_type='sqlite3', db_path='example.db')

# For good measure, let's just quickly make a test table.
# This is a simple .query() because this is just an example.
pysql.query('DROP TABLE IF EXISTS `test`')
pysql.query('CREATE TABLE `test` (`id` INTEGER PRIMARY KEY, `foo` text NOT NULL, `bar` text NOT NULL)')

# Insert some random vals!
for x in range(10):
	vals = ('this', 'that', 'other', 'foo', 'bar', 1, 2, 3, 'hey, listen!')
	data = {
		'foo': random.choice(vals),
		'bar': random.choice(vals)
	}
	pysql.insert('test', data)

# Let's pull ALL the rows
all_rows = pysql.get('test')
print 'All rows:', all_rows # Print, log, modify, etc.

# Let's just pull them where 'foo' == 'this' (which it might not, they are, after all, random)
foo_rows = pysql.where('foo', 'this').get('test')
print 'Foo rows:', foo_rows # Print, log, modify, etc

# Now let's delete entries where 'id' == 1.
delete_rows = pysql.where('id', 1).delete('test')
print 'Delete rows:', delete_rows # Will be True or False.

# Let's delete entries where 'foo' == 'bar', but only up to TWO rows.
delete_foo_bar = pysql.where('foo', 'bar').delete('test', 2)
print 'Delete foo bar:', delete_foo_bar # Will be True or False

# How many rows did we hit?
print 'Affected rows:',pysql.affected_rows()