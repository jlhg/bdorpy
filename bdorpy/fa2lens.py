#!/usr/bin/env python
#
# fa2lens - Extract length data from a fasta file
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.26
#
# Required:
# * Biopython: http://biopython.org
#
# Usage: fa2lens <input.fa> [options]
#
# Options:
# -s, --sep    STR: seperator (default: newline)
# -o, --output STR: output file name. If this option is not specified, the script will generate
#                   one with unique identifier at current directory.
#
# File formats:
# * <input.fa>: fasta

import argparse
from Bio import SeqIO
from fhandle import name

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fa2lens - Extract length data from a fasta file')
    parser.add_argument('input_file')
    parser.add_argument('-s', '--sep', dest='sep', default='\n',
                        help='seperator (default: newline)')
    parser.add_argument('-o', '--output', dest='output_file', default='fa2lens_output_' + name.genid() + '.txt',
                        help='output file name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    args = parser.parse_args()

    with open(args.input_file, 'r') as fin, open(args.output_file, 'w') as fw:
        records = map(str, map(len, list(SeqIO.parse(fin, 'fasta'))))
        fw.write(args.sep.join(records))
        fw.flush()
