#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import ipydoc


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'ipydoc',
    'ipydoc.ipython',
    'dispatcher',
    'dispatcher.dispatcher',
    'dispatcher.ipydispatch'
]

scripts=[
    'scripts/ipydoc_director',
    'scripts/ipydoc_dispatch'
]

package_data = {
}

requires = [
    'docker-py',
    'sh',
    'zerorpc',
    'redis',
    'ipython',
    'django',
    'python-social-auth'
]

classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='ipydoc',
    version=ipydoc.__version__,
    description='Contol interface for ipython notebook servers in docker',
    long_description=readme,
    packages=packages,
    include_package_data=True, #package_data=package_data,
    scripts=scripts,
    install_requires=requires,
    author=ipydoc.__author__,
    author_email='eric@sandiegodata.org',
    url='https://github.com/streeter/python-skeleton',
    license='MIT',
    classifiers=classifiers,
)
