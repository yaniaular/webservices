#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# PYTHON_ARGCOMPLETE_OK

from distutils.core import setup
try:
    # 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # 2.x
    from distutils.command.build_py import build_py

try:
    import os
    import argparse
    import argcomplete
    import pprint
    import sys
except ImportError, e:
    raise Exception("{}. You must install the missed python module to use odoopartner module.".format(e)) 

cmdclass = {'build_py': build_py}
command_options = {}

setup(
    name='odoopartner',
    version='0.0.1',
    author='Katherine Zaoral',
    author_email='kathy@vauxoo.com',
    packages=['odoopartner'],
    scripts=[
        'bin/odoopartner',
    ],
    #~ license='LICENSE.txt',
    description='search / create partner',
    #~ keywords= define keywords,
    long_description=open('README').read(),
    #~ install_requires=[],
    cmdclass=cmdclass,
    command_options=command_options,
)
