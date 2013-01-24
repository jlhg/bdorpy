#!/usr/bin/env python3
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.20


def to_hash(filename):
    seqs = {}

    with open(filename, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                header = line.rstrip().lstrip('>')
                seqs[header] = ''
            else:
                seqs[header] += line.rstrip()

    return seqs
