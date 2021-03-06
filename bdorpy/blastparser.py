#!/usr/bin/env python2.7
#
# blastparser - Parse the blast output file
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 2.4
# Created: 2013.1.22
#
# Required :
# * Biopython: http://biopython.org
#
# Usage: blastparser <blast.xml> [options]
#
# Options:
# -e, --evalue NUM: evalue thresh (default: 0.01)
# -r, --rank   NUM: alignment rank (default: 250)
# -o, --output STR: output file name. If this option is not specified, the script will generate
#                   one with unique identifier at current directory.
# -b, --best      : filter results with best selection. If this option is specified, the script
#                   will select one best hsp for each query with the following criteria. The -r,
#                   --rank option will be useless. (default: false)
#
#                   Criteria: (order by number)
#                    1. Lowest E-value
#                    2. Highest Identity percent
#                    3. Highest Hsp length
#                    4. The first hit
#
# -t, --title     : print header (default: false)
#
# File formats:
# * blast.xml: NCBI blast XML
# * output: blastlist
#
# Tested:
# * BLASTN 2.2.27+
# * BLASTX 2.2.27+
# * BLASTP 2.2.27+

from __future__ import division
import sys
import argparse
import string
import random
import time
import datetime
from Bio.Blast import NCBIXML


class message:
    def __init__(self, prog=None, cmd=None):
        self.prog = prog
        self.cmd = cmd
        self.stime = time.time()
        self.asctime = time.asctime()

    def start_message(self):
        yield '# This output was generated with ' + self.prog + '.\n'
        yield '# Command: ' + self.cmd + '\n'
        yield '# Starting time: ' + self.asctime + '\n'

    def end_message(self):
        yield '# Successfully executed.' + '\n'
        yield '# Elapsed time: ' + str(datetime.timedelta(seconds=round(time.time() - self.stime))) + '\n'


def genid(size=6, chars=string.ascii_uppercase + string.digits):
    random.seed()
    return ''.join(random.choice(chars) for i in range(size))


def main():
    proglog = message(prog='blastparser', cmd=' '.join(sys.argv))

    parser = argparse.ArgumentParser(description='blastparser - Parse the blast output file')
    parser.add_argument('input_file')
    parser.add_argument('-e', '--evalue', dest='ev_thresh', type=float, default=0.01,
                        help='evalue thresh (default: 0.01)')
    parser.add_argument('-r', '--rank', dest='aln_rank', type=int, default=250,
                        help='alignment rank (default: 250)')
    parser.add_argument('-o', '--output', dest='output_file',
                        help='output file name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    parser.add_argument('-b', '--best', dest='best_hit', action='store_true', default=False,
                        help='filter results with best selection. If this option is specified, the script '
                        'will select one best hsp for each query with the following criteria. The -r, '
                        '--rank option will be useless. (default: false) '
                        'Criteria: (order by number) '
                        ' 1. Lowest E-value '
                        ' 2. Highest Identity percent'
                        ' 3. Highest Hsp length'
                        ' 4. The first hit')
    parser.add_argument('-t', '--title', dest='title', action='store_true', default=False,
                        help='print header (default: false)')
    args = parser.parse_args()

    if args.best_hit is True:
        args.aln_rank = 1

    if args.output_file is None:
        args.output_file = args.input_file + '_out_' + genid() + '.blastlist'

    with open(args.input_file, 'r') as result_handle, open(args.output_file, 'w') as fw:
        for i in proglog.start_message():
            fw.write(i)

        header = ('aln_rank',
                  'aln_hspno',
                  'aln_method',
                  'query_name',
                  'hit_name',
                  'query_length',
                  'query_hsp_start',
                  'query_hsp_end',
                  'query_strand',
                  'query_frame',
                  'hit_length',
                  'hit_hsp_start',
                  'hit_hsp_end',
                  'hit_strand',
                  'hit_frame',
                  'hsp_score',
                  'hsp_bits',
                  'hsp_evalue',
                  'hsp_length',
                  'hsp_gaps',
                  'hsp_identities',
                  'hsp_identity_percent',
                  'hsp_positives',
                  'hsp_positive_percent',
                  'query_coverage',
                  'hit_coverage',
                  'hit_description')

        fw.write('#\n')
        fw.write('# E-value threshold: ' + str(args.ev_thresh) + '\n')
        fw.write('# Rank: ' + str(args.aln_rank) + '\n')

        if args.title is True:
            fw.write('\n')
            fw.write('\t'.join(header) + '\n')
        else:
            fw.write('#\n')
            fw.write('# ' + '    '.join(header) + '\n\n')

        fw.flush()

        blast_records = NCBIXML.parse(result_handle)
        query_set = set()
        hit_set = set()
        hsp_num = 0

        for blast_record in blast_records:
            aln_rank = 0

            if len(blast_record.alignments) == 0:
                continue

            alignments = blast_record.alignments

            if args.best_hit is True:
                hspmap = {}
                hsps = []

                for alignment in alignments:
                    for hsp in alignment.hsps:
                        hspmap.update({hsp: alignment})
                        hsps.append(hsp)

                hsps.sort(key=lambda s: (s.expect, -(s.identities / s.align_length), -s.align_length))
                hspmap[hsps[0]].hsps = [hsps[0]]
                alignments = [hspmap[hsps[0]]]

            for alignment in alignments:
                aln_hspno = 0
                aln_rank += 1

                if aln_rank <= args.aln_rank:
                    for hsp in alignment.hsps:
                        aln_hspno += 1
                        if hsp.expect <= args.ev_thresh:
                            hsp_num += 1
                            query_set.add(blast_record.query)
                            hit_set.add(alignment.title)

                            fw.write(str(aln_rank) + '\t')
                            fw.write(str(aln_hspno) + '\t')
                            fw.write(blast_record.application + '\t')
                            fw.write(blast_record.query + '\t')
                            fw.write(alignment.hit_id + '\t')
                            fw.write(str(blast_record.query_length) + '\t')
                            fw.write(str(hsp.query_start) + '\t')
                            fw.write(str(hsp.query_end) + '\t')

                            if blast_record.application in ('BLASTN'):
                                """Fix the missed value in XML output generated with BLASTN 2.2.27+"""
                                fw.write(str(hsp.frame[0]) + '\t')  # The strand
                                fw.write('NA\t')                    # The frame should be NA
                            else:
                                if hsp.strand[0] is None:
                                    fw.write('NA\t')
                                else:
                                    fw.write(str(hsp.strand[0]) + '\t')
                                fw.write(str(str(hsp.frame[0]) + '\t'))

                            fw.write(str(alignment.length) + '\t')
                            fw.write(str(hsp.sbjct_start) + '\t')
                            fw.write(str(hsp.sbjct_end) + '\t')

                            if blast_record.application in ('BLASTN'):
                                """Fix the missed value in XML output generated with BLASTN 2.2.27+"""
                                fw.write(str(hsp.frame[1]) + '\t')  # The strand
                                fw.write('NA\t')                    # The frame should be NA
                            else:
                                if hsp.strand[1] is None:
                                    fw.write('NA\t')
                                else:
                                    fw.write(str(hsp.strand[1] + '\t'))
                                fw.write(str(str(hsp.frame[1])) + '\t')

                            fw.write(str(hsp.score) + '\t')
                            fw.write(str(hsp.bits) + '\t')
                            fw.write(str(hsp.expect) + '\t')
                            fw.write(str(hsp.align_length) + '\t')
                            fw.write(str(hsp.gaps) + '\t')
                            fw.write(str(hsp.identities) + '\t')
                            fw.write(str(round(hsp.identities / hsp.align_length * 100, 2)) + '\t')
                            fw.write(str(hsp.positives) + '\t')
                            fw.write(str(round(hsp.positives / hsp.align_length * 100, 2)) + '\t')
                            fw.write(str(round((abs(hsp.query_end - hsp.query_start) + 1) / blast_record.query_length * 100, 2)) + '\t')
                            fw.write(str(round((abs(hsp.sbjct_end - hsp.sbjct_start) + 1) / alignment.length * 100, 2)) + '\t')
                            fw.write(alignment.title + '\n')
                            fw.flush()

        fw.write('\n')
        fw.write('# Parsed queries: ' + str(len(query_set)) + '\n')
        fw.write('# Non-redundant hits: ' + str(len(hit_set)) + '\n')
        fw.write('# Parsed HSPs: ' + str(hsp_num) + '\n')
        fw.write('#\n')

        for i in proglog.end_message():
            fw.write(i)

if __name__ == '__main__':
    main()
