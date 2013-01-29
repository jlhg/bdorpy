#!/usr/bin/env python3
#
# converter.py
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)


def group_continuous_number(list):
    if not list:
        yield 0, 0
    else:
        """Yield a list of tuple of continuous numbers"""
        first = last = list[0]
        for n in list[1:]:
            if n - 1 == last:
                """Part of the group"""
                last = n
            else:
                """Not part of the group"""
                yield first, last
                first = last = n
        """Yield the last group"""
        yield first, last
