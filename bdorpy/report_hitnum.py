#!/usr/bin/env python3
#
# report_hitnum - Count the number of hit sequences
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.2
# Created: 2013.1.23
#
# Usage: report_hitnum <input.tsv>
#
# Options:
# -e, --evalue NUM: evalue thresh (default: 0.01)
#
# File formats:
# * input.tsv: blast-list

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='report_hitnum - Count the number of hit sequences')
    parser.add_argument('input_file')
    parser.add_argument('-e', '--evalue', dest='ev_thresh', type=float, defualt=0.01,
                        help='evalue thresh (default: 0.01)')
    args = parser.parse_args()

    with open(args.input_file, 'r') as fin:
        old_rank = 0
        ranks = []

        for line in fin:
            if line.lstrip(' ')[0] in ('#', '\n'):
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

        print('Count >= 0: ' + str(count_1))
        print('Count >= 10: ' + str(count_10))
        print('Count >= 50: ' + str(count_50))
        print('Count >= 100: ' + str(count_100))
        print('Count >= 200: ' + str(count_200))
        print('Count >= 250: ' + str(count_250))
