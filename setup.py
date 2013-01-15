from setuptools import setup

def long_desc():
	with open('README.rst', 'rb') as f:
		return f.read()

kw = {
	"name": "pysqlw",
	"version": "1.0.0",
	"description": "Python wrapper to make MySQL and SQLite easy",
	"long_description": long_desc(),
	"url": "https://github.com/plausibility/pysqlw",
	"author": "plausibility",
	"author_email": "chris@gibsonsec.org",
	"license": "MIT",
	"packages": ['pysqlw'],
	"zip_safe": False
}

if __name__ == "__main__":
	setup(**kw)