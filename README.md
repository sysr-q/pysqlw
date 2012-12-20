pysql-wrapper
=============

A Python based sqlite wrapper class. (Incase you care: pysql is pronounced: _py-skew-el_)

Requirements
--
+ Python 2.7.3 (this is what I test with, should work with 2.6.x, 3.x not guaranteed)
+ sqlite3 module (comes with Python installs)
+ [MySQLdb](http://sourceforge.net/projects/mysql-python/) (Only if you want MySQL support)
	+ To install MySQLdb:
	+ If you're using a Debian-like distro (Ubuntu, Debian, Crunchbang, etc), install the package __python-mysqldb__
		+ `sudo apt-get install python-mysqldb`
	+ If that didn't work, or you're not using a Debian-like distro:
		+ Build and install the MySQLdb module from source.
		+ [This link](http://blog.mysqlboy.com/2010/08/installing-mysqldb-python-module.html) explains better than I could.
	+ Verify it's installed: `python -c 'import MySQLdb'`
		+ If nothing shows up, you're good!
		+ If you get an ImportError, think, do you __really__ need MySQL? If yes, this is a problem. :(
+ 


Usage
--
+ Place __pysql_wrapper.py__ into your project's folder somewhere.
+ Import pysql-wrapper:
	+ `from pysql_wrapper import pysql_wrapper`
+ Create a new instance:
	+ `pysql = pysql_wrapper(db_type='sqlite', db_path='some/file.db')` (uses sqlite3 default, so db_type is optional here)
	+ If you want to use MySQL you need to supply more details:
	+ `pysql = pysql_wrapper(db_type='mysql', db_host='localhost', db_user='username', db_pass='password', db_name='database_name')`
+ Use it!

Example usage can be found in the _example_ folder, those are a good start if you're interested.

Documentation
--
Documentation for pysql-wrapper can be found at the [wiki](https://github.com/PigBacon/pysql-wrapper/wiki/)

License
--
(This is also provided in the LICENSE file)
```
Copyright (C) 2012 Christopher Carter <chris@gibsonsec.org>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```