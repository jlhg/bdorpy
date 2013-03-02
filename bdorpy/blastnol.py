#!/usr/bin/env python
#
# blastnol - Find the non-overlapping hits in the blast result
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 1.0
# Created: 2013.2.7
#
# Requirement:
# * Biopython: http://biopython.org
#
# Usage: blastnol <input.blastlist> [options]
#
# Options:
# -o, --output-directory STR: output directory name. If this option is not specified, the script will generate
#                             one with unique identifier at current directory.
# -q, --query-sequence   STR: fasta file of query sequence. If this option is specified, the script will
#                             generate a new fasta file that contains truncated long sequences.

import os
import argparse
from subprocess import Popen, PIPE
from Bio import SeqIO
from alignment import calculate
from fhandle import name, header


def combine_hsps(hsps):
    """hsps: a list of tuples"""
    pos_start = None
    pos_end = None
    lines = []

    for hsp_start, hsp_end, line in hsps:
        if pos_start is None:
            pos_start = hsp_start
            pos_end = hsp_end
        else:
            pos_start = min(pos_start, hsp_start)
            pos_end = max(pos_end, hsp_end)
        lines = lines + line

    return pos_start, pos_end, lines


def get_start_pos(item):
    return item[1][0][0]


def main():
    parser = argparse.ArgumentParser(description='blastnol - Find the non-overlapping hits in the blast result')
    parser.add_argument('input_file')
    parser.add_argument('-o', '--output-directory', dest='output_dir',
                        help='output directory name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    parser.add_argument('-q', '--query-sequence', dest='query_fa',
                        help='fasta file of query sequence. If this option is specified, the script will '
                        'generate a new fasta file that contains truncated long sequences.')
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = args.input_file + '_out_' + name.genid()
    else:
        args.output_dir = args.output_dir.rstrip('/')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if args.query_fa is not None:
        query_fa = dict(SeqIO.index(args.query_fa, 'fasta'))
        fw_fa = open(args.output_dir + '/truncated.fa', 'w')

    with open(args.output_dir + '/sort.temp', 'w') as fwsort:
        awk_cmd = "awk -F'\t' 'int($1) { print $0 }' " + args.input_file
        sort_cmd = "sort -t$'\t' -k9g,9 -k4d,4 -k18g,18 -k22gr,22 -k19gr,19 -k26gr,26 -k6gr"
        awk_proc = Popen(awk_cmd, stdout=PIPE, executable='/bin/bash', shell=True)
        sort_proc = Popen(sort_cmd, stdin=awk_proc.stdout, stdout=fwsort, executable='/bin/bash', shell=True)
        sort_proc.communicate()

    seq = {}

    with open(args.output_dir + '/sort.temp', 'r') as fi:
        for line in fi:
            data = line.split('\t')
            query_name = data[3]
            hit_name = data[4]
            query_strand = int(data[8])

            if query_strand < 0:
                query_name = '-' + query_name
                query_hsp_start = int(data[7])
                query_hsp_end = int(data[6])
            else:
                query_hsp_start = int(data[6])
                query_hsp_end = int(data[7])

            if query_name in seq:
                for i in range(len(seq[query_name])):
                    if hit_name in seq[query_name][i][0]:
                        seq[query_name][i][1].append((query_hsp_start, query_hsp_end, [line]))
                        break
                else:
                    seq[query_name].append((hit_name, [(query_hsp_start, query_hsp_end, [line])]))
            else:
                seq.update({query_name: [(hit_name, [(query_hsp_start, query_hsp_end, [line])])]})

    # Combine hsps
    for query_name in seq:
        hit_rank = 1
        for i in range(len(seq[query_name])):
            hit = seq[query_name][i]
            if len(hit[1]) > 1:
                # Combine hsps
                pos_start, pos_end, lines = combine_hsps(hit[1])
                seq[query_name][i] = ([hit[0]], [(pos_start, pos_end)], [lines], [hit_rank])
            else:
                seq[query_name][i] = ([hit[0]], [(hit[1][0][0], hit[1][0][1])], [hit[1][0][2]], [hit_rank])
            hit_rank += 1

    # Sort hits by start position
    for query_name in seq:
        seq[query_name] = sorted(seq[query_name], key=get_start_pos)

    # Check overlap
    for query_name, hits in seq.items():
        while len(hits) > 1:
            position = calculate.get_non_overlap((hits[0][1][0][0], hits[0][1][-1][1]), (hits[1][1][0][0], hits[1][1][0][1]))
            if position is not None:
                # The two sequences are non-overlapping, combine them
                seq[query_name][0] = (hits[0][0] + hits[1][0], hits[0][1] + hits[1][1], hits[0][2] + hits[1][2], hits[0][3] + hits[1][3])
                seq[query_name].pop(1)
            else:
                # Compare the hit rank to determine which one is retained
                if seq[query_name][0][3][-1] < seq[query_name][1][3][0]:
                    # Discard the next hit
                    seq[query_name].pop(1)
                else:
                    # Discard the last hit, and join the next hit
                    seq[query_name][0][0].pop(-1)
                    seq[query_name][0][1].pop(-1)
                    seq[query_name][0][2].pop(-1)
                    seq[query_name][0][3].pop(-1)
                    seq[query_name][0] = (hits[0][0] + hits[1][0], hits[0][1] + hits[1][1], hits[0][2] + hits[1][2], hits[0][3] + hits[1][3])
                    seq[query_name].pop(1)

    # Write data
    with open(args.output_dir + '/hit_cover.tsv', 'w') as fw:
        query_num = 0
        query_num_cover_eq_two = 0
        query_num_cover_eq_three = 0
        query_num_cover_ge_four = 0

        hit_set = set()
        hr = header.blastlist()
        fw.write(hr.get_all_tab() + '\n')
        fw.flush()

        for query, hits in seq.items():
            query = query.split(' ')[0]

            if len(hits[0][0]) > 1:
                query_num += 1

                if len(hits[0][0]) == 2:
                    query_num_cover_eq_two += 1
                elif len(hits[0][0]) == 3:
                    query_num_cover_eq_three += 1
                else:
                    query_num_cover_ge_four += 1

                for lines in hits[0][2]:
                    for line in lines:
                        hit_set.add(line.split('\t')[4])
                        fw.write(line)
                    fw.flush()

                if args.query_fa is not None:
                    # Truncated queries
                    segment_num = 0
                    for pos_start, pos_end in hits[0][1]:
                        fw_fa.write('>' + query + '_s' + str(segment_num) + '\n')
                        fw_fa.write(query_fa[query].seq.tostring()[pos_start - 1:pos_end] + '\n')
                        fw_fa.flush()
                        segment_num += 1
                    query_fa.pop(query)
            else:
                if args.query_fa is not None:
                    # Full-sequece queries
                    fw_fa.write('>' + query + '\n')
                    fw_fa.write(query_fa[query].seq.tostring() + '\n')
                    query_fa.pop(query)

        if args.query_fa is not None:
            # No-hit queries
            for query in query_fa:
                fw_fa.write('>' + query + '\n')
                fw_fa.write(query_fa[query].seq.tostring() + '\n')
                fw_fa.flush()
            fw_fa.close()

        fw.write('\n')
        fw.write('# Number of queries that cover >= 2 hits: ' + str(query_num) + '\n')
        fw.write('#   Cover 2 hits: ' + str(query_num_cover_eq_two) + '\n')
        fw.write('#   Cover 3 hits: ' + str(query_num_cover_eq_three) + '\n')
        fw.write('#   Cover >= 4 hits: ' + str(query_num_cover_ge_four) + '\n')
        fw.write('# Number of covered hits: ' + str(len(hit_set)))

if __name__ == '__main__':
    main()
