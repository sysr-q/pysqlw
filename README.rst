======
pysqlw
======

.. _MySQLdb: http://sourceforge.net/projects/mysql-python/
.. _This link: http://blog.mysqlboy.com/2010/08/installing-mysqldb-python-module.html
.. _readthedocs: https://pysqlw.readthedocs.org
.. _pysqlw wrappers: https://pysqlw.readthedocs.org/en/latest/wrappers.html
.. _github repo: https://github.com/plausibility/pysqlw

A Python based wrapper (meta-wrapper, even) allowing easy MySQL and SQLite interactions.

Requirements
============

-  Python 2.7.3 (this is what I test with, should work with most 2.x, not sure about 3.x)
-  sqlite3 module (comes with Python installs)
-  Install `MySQLdb`_ if you want MySQL support

   -  If you’re using a Debian-like distro (Ubuntu, Debian, Crunchbang, etc), install the package **python-mysqldb**

      - ``$ sudo apt-get install python-mysqldb``

   -  There is no pypi package (someone get on this)
   -  If that didn’t work, or you’re not using a Debian-like distro:

      -  Build and install the MySQLdb module from source.
      -  `This link`_ explains better than I could.

   -  Verify it’s installed: ``$ python -c 'import MySQLdb'``

      -  If nothing shows up, you’re good!
      -  If you get an ImportError, think, do you **really** need MySQL?
      -  If yes, this is a problem, and I can't really help. :(
      -  If you don't, just use sqlite, it's much easier.

Usage
=====

-  Install pysqlw: ``$ pip install pysqlw``
-  Import pysqlw:

   - ``import pysqlw``

-  Create a new instance:

   -  ``p = pysqlw.pysqlw(db_type="sqlite", db_path="/home/user/example.db")``
   -  If you want to use MySQL you need to supply more details:
   -  ``p = pysqlw.pysqlw(db_type="mysql", db_host="localhost", db_user="username", db_pass="password", db_name="database_name")``

-  Documentation is now on the pysqlw `readthedocs`_ entry.

Contributing
============
If you're interested, you can write extra meta-wrappers for foreign database types.  
They're pretty simple, look at the `pysqlw wrappers`_ documentation page for an example.

If there's not a wrapper for a database type you'd like (that is, an actual wrapper, not just a meta-wrapper), you should make one of those and send in some pull requests with meta-wrappers! More coverage is great.

If you wish to help contribute to the base wrapper functions, feel free to fork the `github repo`_ and send in pull requests!
