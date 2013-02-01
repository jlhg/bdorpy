#!/usr/bin/env python3
#
# fixname - Fix hit name in the blastlist
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.30
#
# Usage: <input.blastlist> [options]
#
# Options:
# -o, --output STR: output file name. If this option is not specified, the script will generate
#                   one with unique identifier at current directory.
#
# This script replace the hit name generated with makeblastdb tool with NCBI accession name.

import sys
import argparse
import re
from fhandle import name


def main():
    parser = argparse.ArgumentParser(description='fixname - Fix hit name in the blastlist')
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output', dest='output_file',
                        help='output file name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = args.input_file + '_out_' + name.genid() + '.fix'

    hitname = re.compile('.*?(gi\|\d*?\|.*?\|.*?\|)(.*)')

    with open(args.input_file, 'r') as fin, open(args.output_file, 'w') as fw:
        for linum, line in enumerate(fin, start=1):
            if line.lstrip() == '' or line.lstrip()[0] in ('#', 'a'):
                fw.write(line)
                fw.flush()
            else:
                data = line.split('\t')
                match = hitname.match(data[26])

                if match is None:
                    print('No mathced name in line ' + str(linum) + '.')
                    print('Please have a check.')
                    sys.exit()
                else:
                    data[4] = match.group(1)
                    data[26] = match.group(1) + match.group(2) + '\n'
                    fw.write('\t'.join(data))
                    fw.flush()

if __name__ == '__main__':
    main()
