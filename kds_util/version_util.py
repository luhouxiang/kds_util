# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用来显示版本号的内容
"""
import sys
import subprocess


def show_version():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            git_v = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            git_v = git_v.decode('utf-8')
            print("git_version: " + git_v)
            sys.exit()
