from setuptools import setup


def long_desc():
    with open('README.rst', 'rb') as f:
        return f.read()

kw = {
    "name": "pysqlw",
    "version": "1.2.0",
    "description": "Python wrapper to make interacting with SQL databases easy",
    "long_description": long_desc(),
    "url": "https://github.com/plausibility/pysqlw",
    "author": "plausibility",
    "author_email": "chris@gibsonsec.org",
    "license": "MIT",
    "packages": ['pysqlw'],
    "zip_safe": False,
    "keywords": "sql sqlite mysql wrapper",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Database"
    ]
}

if __name__ == "__main__":
    setup(**kw)
