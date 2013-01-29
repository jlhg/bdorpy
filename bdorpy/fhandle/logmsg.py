#!/usr/bin/env python3
#
# logmsg.py
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.25

import time
import datetime


class message:
    def __init__(self, prog=None, cmd=None):
        self.prog = prog
        self.cmd = cmd
        self.stime = time.time()
        self.asctime = time.asctime()

    def start_message(self):
        yield '# This output was generated with ' + self.prog + '.\n'
        yield '# Command: ' + self.cmd + '\n'
        yield '# Starting time: ' + self.asctime + '\n'

    def end_message(self):
        yield '# Successfully executed.' + '\n'
        yield '# Elapsed time: ' + str(datetime.timedelta(seconds=round(time.time() - self.stime))) + '\n'
