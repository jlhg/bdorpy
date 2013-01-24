#!/usr/bin/env python3
#
# bliststats
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.23
#
# Usage: bliststats <blast.tsv>
#
# Input format:
# col #  title
# 0      aln_rank
# 1      aln_hspno
# 2      aln_method
# 3      query_name
# 4      hit_name
# 5      query_length
# 6      query_hsp_start
# 7      query_hsp_end
# 8      query_strand
# 9      query_frame
# 10     hit_length
# 11     hit_hsp_start
# 12     hit_hsp_end
# 13     hit_strand
# 14     hit_frame
# 15     hsp_score
# 16     hsp_bits
# 17     hsp_evalue
# 18     hsp_length
# 19     hsp_gaps
# 20     hsp_identities
# 21     hsp_identity_percent
# 22     hsp_positives
# 23     hsp_positive_percent
# 24     query_coverage
# 25     hit_coverage
# 26     hit_description

import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fin:
        EV_THRESH = 1e-5
        old_rank = 0
        ranks = []

        for line in fin:
            if line[0] == 'a':
                continue
            if float(line.split('\t')[17]) <= EV_THRESH:
                new_rank = int(line.split('\t')[0])
                if new_rank < old_rank:
                    ranks.append(old_rank)
                old_rank = new_rank

        ranks.append(new_rank)

        count_0 = 0
        count_10 = 0
        count_50 = 0
        count_100 = 0
        count_200 = 0
        count_250 = 0

        for i in ranks:
            if i >= 0:
                count_0 += 1
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

        print('Count >= 0: ' + str(count_0))
        print('Count >= 10: ' + str(count_10))
        print('Count >= 50: ' + str(count_50))
        print('Count >= 100: ' + str(count_100))
        print('Count >= 200: ' + str(count_200))
        print('Count >= 250: ' + str(count_250))
