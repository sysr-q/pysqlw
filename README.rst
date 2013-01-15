======
pysqlw
======

A Python based wrapper (meta-wrapper, even) allowing easy MySQL and SQLite interactions. (Incase you care: pysql is pronounced: *py-skew-el*)

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
        -  If yes, this is a problem. :(

Usage
=====

-  Install pysqlw: ``$ pip install pysqlw``
-  Import pysqlw:
    - ``import pysqlw``
-  Create a new instance:
    -  ``db_type`` defaults to sqlite, so you won't have to change it unless you want MySQL.
    -  ``pysql = pysqlw.pysqlw(db_type='sqlite', db_path='/home/user/example.db')``
    -  If you want to use MySQL you need to supply more details:
    -  ``pysql = pysqlw.pysqlw(db_type='mysql', db_host='localhost', db_user='username', db_pass='password', db_name='database_name')``
-  Documentation is found in the `usage`_ wiki page.

Contributing
============
If you're interested, you can write extra interaction wrappers for foreign database types.  
They're pretty simple, look at the ``sqlitew.py`` script for an example.

.. _MySQLdb: http://sourceforge.net/projects/mysql-python/
.. _This link: http://blog.mysqlboy.com/2010/08/installing-mysqldb-python-module.html
.. _usage: https://github.com/plausibility/pysqlw/wiki/Usage