#!/usr/bin/env python3
#
# cquery - Count the number of queries with its hit rank greater than some value
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 1.0
# Created: 2013.1.23
#
# Usage: cquery <input.tsv>
#
# Options:
# -e, --evalue NUM: evalue thresh (default: 0.01)
#
# File formats:
# * input.tsv: blast-list
#
# Support multiple input files and Unix style pathname pattern.
#
# For example:
# * cquery <file_1> <file_2> <file_3> ... [-e NUM]
# * cquery intput_* [-e NUM]

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Count the number of queries with its hit rank greater than some value')
    parser.add_argument('input_file', nargs='*')
    parser.add_argument('-e', '--evalue', dest='ev_thresh', type=float, default=0.01,
                        help='evalue thresh (default: 0.01)')
    args = parser.parse_args()

    ranks = []

    for f in args.input_file:
        with open(f, 'r') as fin:
            old_rank = 0
            new_rank = 0

            for line in fin:
                if line.lstrip() == '' or line.lstrip()[0] in ('#', 'a'):
                    continue

                if float(line.split('\t')[17]) <= args.ev_thresh:
                    new_rank = int(line.split('\t')[0])

                    if new_rank < old_rank:
                        ranks.append(old_rank)
                    old_rank = new_rank

        ranks.append(new_rank)

    count_1 = 0
    count_10 = 0
    count_50 = 0
    count_100 = 0
    count_200 = 0
    count_250 = 0

    for i in ranks:
        if i >= 1:
            count_1 += 1
        if i >= 10:
            count_10 += 1
        if i >= 50:
            count_50 += 1
        if i >= 100:
            count_100 += 1
        if i >= 200:
            count_200 += 1
        if i >= 250:
            count_250 += 1

    print("Results:")
    print('E-value threshold: ' + str(args.ev_thresh))
    print('Total queries: ' + str(count_1))
    print('Rank number >= 10: ' + str(count_10))
    print('Rank number >= 50: ' + str(count_50))
    print('Rank number >= 100: ' + str(count_100))
    print('Rank number >= 200: ' + str(count_200))
    print('Rank number >= 250: ' + str(count_250))
