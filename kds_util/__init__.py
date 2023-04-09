# !/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import dirname, join


def get_version_string():
    with open(join(dirname(__file__), 'VERSION.txt'), 'rb') as f:
        return f.read().decode('ascii').strip()
    return ""


__version__ = version = VERSION = get_version_string()





