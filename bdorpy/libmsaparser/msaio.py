#!/usr/bin/env python3
#
# msaio.py -- Loading MSA files
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)

import os


class FileInput:
    """ Input MSA file"""

    def __init__(self, dirpath):
        self.files = []
        for root, dirs, files in os.walk(dirpath):
            for filename in files:
                self.files.append((root, filename))

    def get_files(self):
        return self.files
