#!/usr/bin/env python3
#
# idfix.py
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.7
#
# Usage: idfix.py <idmap> <fasta> <output>

import sys


def main():
    with open(sys.argv[1], 'r') as fin, open(sys.argv[2], 'r') as ffa, open(sys.argv[3], 'w') as fo:
        full_id = {}

        for line in ffa:
            if line[0] != '>':
                continue
            full_id.update({line.split()[0].split('|')[-2]: line.split()[0].split('>')[1]})

        for line in fin:
            if line.split('\t')[1].rstrip() in full_id:
                fo.write(line.split('\t')[0] + '\t' + full_id[line.split('\t')[1].rstrip()] + '\n')
                fo.flush()
            else:
                sys.exit('Id not found, stop!')

if __name__ == '__main__':
    main()
