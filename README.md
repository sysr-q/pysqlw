pysql-wrapper
=============

A Python based sqlite wrapper class. (Incase you care: pysql is pronounced: _py-skew-el_)

Requirements
---
+ Python 2.7.3 (this is what I test with, should work with 2.6.x, 3.x not guaranteed)
+ sqlite3 module (comes with Python installs)
+ [MySQLdb](http://sourceforge.net/projects/mysql-python/) (Only if you want MySQL support)
	+ To install MySQLdb:
	+ If you're using a Debian-like distro (Ubuntu, Debian, Crunchbang, etc), install the package __python-mysqldb__
		+ `sudo apt-get install python-mysqldb`
	+ There is no pip package (someone get on this)
	+ If that didn't work, or you're not using a Debian-like distro:
		+ Build and install the MySQLdb module from source.
		+ [This link](http://blog.mysqlboy.com/2010/08/installing-mysqldb-python-module.html) explains better than I could.
	+ Verify it's installed: `python -c 'import MySQLdb'`
		+ If nothing shows up, you're good!
		+ If you get an ImportError, think, do you __really__ need MySQL? If yes, this is a problem. :(
+ 


Usage
---
+ Place __pysql_wrapper.py__ into your project's folder somewhere.
+ Import pysql-wrapper:
	+ `from pysql_wrapper import pysql_wrapper`
+ Create a new instance:
	+ `pysql = pysql_wrapper(db_type='sqlite', db_path='some/file.db')` (uses sqlite3 default, so db_type is optional here)
	+ If you want to use MySQL you need to supply more details:
	+ `pysql = pysql_wrapper(db_type='mysql', db_host='localhost', db_user='username', db_pass='password', db_name='database_name')`
+ Documentation is found in the [Usage](https://github.com/plausibility/pysql-wrapper/wiki/Usage) wiki page.
