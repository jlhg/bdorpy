#!/usr/bin/env python3
#
# name.py
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.20

import string
import random


def genid(size=6, chars=string.ascii_uppercase + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for i in range(size))
