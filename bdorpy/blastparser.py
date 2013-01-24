#!/usr/bin/env python
#
# blastparser - Parse the blast output file
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.22
#
# Required :
# * Biopython: http://biopython.org
#
# Usage: blastparser <blast.xml> [<output>] [options]
#
# Options:
# -e NUM: evalue thresh (default: 0.01)
# -r NUM: alignment rank (default: 250)
#
# Output format:
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

from __future__ import division
import argparse
from Bio.Blast import NCBIXML
from fhandle import name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_blast')
    parser.add_argument('file_output', nargs='?', default='bp_output_' + name.genid() + '.tsv')
    parser.add_argument('-e', dest='ev_thresh', type=float, default=0.01)
    parser.add_argument('-r', dest='aln_rank', type=int, default=250)
    args = parser.parse_args()

    with open(args.file_blast, 'r') as result_handle, open(args.file_output, 'w') as fw:
        blast_records = NCBIXML.parse(result_handle)
        fw.write('aln_rank\t' + 'aln_hspno\t' + 'aln_method\t' + 'query_name\t' +
                 'hit_name\t' + 'query_length\t' + 'query_hsp_start\t' + 'query_hsp_end\t' +
                 'query_strand\t' + 'query_frame\t' + 'hit_length\t' + 'hit_hsp_start\t' +
                 'hit_hsp_end\t' + 'hit_strand\t' + 'hit_frame\t' + 'hsp_score\t' +
                 'hsp_bits\t' + 'hsp_evalue\t' + 'hsp_length\t' + 'hsp_gaps\t' +
                 'hsp_identities\t' + 'hsp_identity_percent\t' + 'hsp_positives\t' + 'hsp_positive_percent\t' +
                 'query_coverage\t' + 'hit_coverage\t' + 'hit_description\n')
        fw.flush()

        for blast_record in blast_records:
            aln_rank = 0
            for alignment in blast_record.alignments:
                aln_hspno = 0
                aln_rank += 1
                if aln_rank <= args.aln_rank:
                    for hsp in alignment.hsps:
                        aln_hspno += 1
                        if hsp.expect <= args.ev_thresh:
                            fw.write(str(aln_rank) + '\t')
                            fw.write(str(aln_hspno) + '\t')
                            fw.write(blast_record.application + '\t')
                            fw.write(blast_record.query + '\t')
                            fw.write(alignment.hit_id + '\t')
                            fw.write(str(blast_record.query_length) + '\t')
                            fw.write(str(hsp.query_start) + '\t')
                            fw.write(str(hsp.query_end) + '\t')
                            if hsp.strand[0] is None:
                                fw.write('NA\t')
                            else:
                                fw.write(str(hsp.strand[0]) + '\t')
                            fw.write(str(str(hsp.frame[0]) + '\t'))
                            fw.write(str(alignment.length) + '\t')
                            fw.write(str(hsp.sbjct_start) + '\t')
                            fw.write(str(hsp.sbjct_end) + '\t')
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
                            fw.write(str(round((hsp.query_end - hsp.query_start + 1) / blast_record.query_length * 100, 2)) + '\t')
                            fw.write(str(round((hsp.sbjct_end - hsp.sbjct_start + 1) / alignment.length * 100, 2)) + '\t')
                            fw.write(alignment.title + '\n')
                            fw.flush()
