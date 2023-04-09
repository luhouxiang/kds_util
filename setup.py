#!/usr/bin/env python

import sys
from setuptools import setup
from os.path import dirname, join
from setuptools import (
    find_packages,
    setup,
)


def read_file(file):
    with open(file, "rt") as f:
        return f.read()


with open(join(dirname(__file__), 'kds_util/VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='kds_util',
    version=version,
    description='A base tool',
    author='kds',
    author_email='kds@gmail.com',
    url='https://github.com/kds/kds_util',
    install_requires=read_file("requirements.txt").strip(),
    license='MIT',
    packages=find_packages(exclude=[]),
    package_data={'': ['*.*']},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)