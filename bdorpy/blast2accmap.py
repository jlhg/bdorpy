#!/usr/bin/env python
#
# blast2accmap - Extract names of query and hit sequences
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.4
# Created: 2013.1.25
#
# Required:
# * Biopython: http://biopython.org
#
# Usage: blast2accmap <blast.xml> [options]
#
# Options:
# -e, --evalue      NUM: evalue thresh (default: 0.01)
# -t, --min_hit_num NUM: minimum number of hit sequences (default: 1)
# -o, --output      STR: output file name. If this option is not specified, the script will generate
#                        one with unique identifier at current directory.
#
# File Formats:
# * blast.xml: blast XML
# * output: blastaccmap
#
# This script is written for the sake of making training data for WildSpan.

import sys
import argparse
from Bio.Blast import NCBIXML
from fhandle import name, logmsg


def main():
    proglog = logmsg.message(prog='blast2accmap', cmd=' '.join(sys.argv))

    parser = argparse.ArgumentParser(description='blast2accmap - Extract names of query and hit sequences')
    parser.add_argument('input_file')
    parser.add_argument('-e', '--evalue', dest='ev_thresh', type=float, default=0.01,
                        help='evalue thresh (default: 0.01)')
    parser.add_argument('-t', '--min_hit_num', dest='min_hit_num', type=int, default=1,
                        help='minimum number of hit sequences (default: 1)')
    parser.add_argument('-o', '--output', dest='output_file',
                        help='output file name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = args.input_file + '_out_' + name.genid() + 'blastaccmap'

    total_query_num = 0
    parsed_query_num = 0

    with open(args.input_file, 'r') as result_handle, open(args.output_file, 'w') as fw:
        blast_records = NCBIXML.parse(result_handle)

        for i in proglog.start_message():
            fw.write(i)

        fw.write('#\n')
        fw.write('# E-value threshold: ' + str(args.ev_thresh) + '\n')
        fw.write('# min hit number: ' + str(args.min_hit_num) + '\n')
        fw.write('#\n')
        fw.write('# query_accession    hit_accession_1,hit_accession_2, ...\n\n')
        fw.flush()

        for blast_record in blast_records:
            total_query_num += 1

            if len(blast_record.alignments) < args.min_hit_num:
                continue

            hit_accs = []

            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    if alignment.accession in blast_record.query:
                        """If query hit itself, ignore it. """
                        continue

                    if hsp.expect <= args.ev_thresh:
                        hit_accs.append(alignment.accession)
                        break

            if len(hit_accs) >= args.min_hit_num:
                parsed_query_num += 1
                fw.write(blast_record.query + '\t' + blast_record.query + ',')
                fw.write(','.join(hit_accs) + '\n')
                fw.flush()

        fw.write('\n')
        fw.write('# Total queries: ' + str(total_query_num) + '\n')
        fw.write('# Parsed queries: ' + str(parsed_query_num) + '\n')
        fw.write('#\n')

        for i in proglog.end_message():
            fw.write(i)

        fw.flush()

if __name__ == '__main__':
    main()
