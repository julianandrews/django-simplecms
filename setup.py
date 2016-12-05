#!/usr/bin/env python

import os
from setuptools import setup, find_packages

__doc__ = """
A simple extensible CMS framework for Django.
"""


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-simplecms',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Apache Software License',
    description=__doc__,
    long_description=read('README.rst') + '\n\n' + read('CHANGELOG.rst'),
    url='http://github.com/julianandrews/simplecms',
    author='Julian Andrews',
    author_email='jandrews271@gmail.com',
    install_requires=[
        'django-treebeard',
        'Django>=1.8',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
    ],
)
