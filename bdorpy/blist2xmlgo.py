#!/usr/bin/env python3
#
# blist2xmlgo.py
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1.0
# Created: 2013.1.6
#
# Usage: blist2xmlgo.py <blast_list> <map_ids> <output>
#
# Columns:
# 0	aln_rank
# 1	aln_hspno
# 2	aln_method
# 3	query_name
# 4	hit_name
# 5	query_length
# 6	query_hsp_start
# 7	query_hsp_end
# 8	query_strand
# 9	query_frame
# 10	hit_length
# 11	hit_hsp_start
# 12	hit_hsp_end
# 13	hsp_score
# 14	hsp_bits
# 15	hsp_evalue
# 16	hsp_length
# 17	hsp_gaps
# 18	hsp_identities
# 19	hsp_identity_percent
# 20	hsp_positives
# 21	hsp_positive_percent
# 22	query_coverage
# 23	hit_coverage
# 24	hit_description

import sys


def main():
    with open(sys.argv[1], 'r') as fin, open(sys.argv[2], 'r') as fmap, open(sys.argv[3], 'w') as fo:
        idm = {}

        for line in fmap:
            """Feed id data"""
            idm.update({line.split('\t')[0]: line.split('\t')[1].rstrip()})

        query_count = 0

        for line in fin:
            if line[0] == 'a':
                continue

            data = line.split('\t')

            if data[3] in idm and data[4] in idm[data[3]]:
                query_count += 1
                fo.write('<?xml versio="1.0"?>\n')
                fo.write('<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "NCBI_BlastOutput.dtd">\n')
                fo.write('<BlastOutput><BlastOutput_program>blast</BlastOutput_program>\n')
                fo.write('<BlastOutput_version>BLAST 2.2.27+</BlastOutput_version>\n')
                fo.write('<BlastOutput_db>db.fa</BlastOutput_db>\n')
                fo.flush()
                fo.write('<BlastOutput_query-ID>' + 'Query' + str(query_count) + '</BlastOutput_query-ID>\n')
                fo.write('<BlastOutput_query-def>' + data[3] + '</BlastOutput_query-def>\n')
                fo.write('<BlastOutput_query-len>' + str(data[5]) + '</BlastOutput_query-len>\n')
                fo.write('<BlastOutput_param>\n')
                fo.write('<Parameters>\n')
                fo.write('<Parameters_expect>10</Parameters_expect>\n')
                fo.write('<Parameters_filter>L;</Parameters_filter>\n')
                fo.write('</Parameters>\n')
                fo.write('</BlastOutput_param>\n')
                fo.write('<BlastOutput_iterations>\n')
                fo.write('<Iteration>\n')
                fo.write('<Iteration_iter-num>1</Iteration_iter-num>\n')
                fo.write('<Iteration_query-ID>' + str(query_count) + '</Iteration_query-ID>\n')
                fo.write('<Iteration_query-def>' + data[3] + '</Iteration_query-def>\n')
                fo.write('<Iteration_query-len>' + str(data[5]) + '</Iteration_query-len>\n')
                fo.write('<Iteration_hits>\n')
                fo.write('<Hit>\n')
                fo.write('<Hit_num>1</Hit_num>\n')
                fo.write('<Hit_id>' + idm[data[3]] + '</Hit_id>\n')
                fo.write('<Hit_def>' + data[24] + '</Hit_def>\n')
                fo.write('<Hit_accession>1</Hit_accession>\n')
                fo.write('<Hit_len>' + data[10] + '</Hit_len>\n')
                fo.write('<Hit_hsps>\n')
                fo.write('<Hsp>\n')
                fo.write('<Hsp_num>1</Hsp_num>\n')
                fo.write('<Hsp_bit-score>' + str(data[14]) + '</Hsp_bit-score>\n')
                fo.write('<Hsp_evalue>' + data[15] + '</Hsp_evalue>\n')
                fo.write('<Hsp_query-frame>' + str(data[9]) + '</Hsp_query-frame>\n')
                fo.write('<Hsp_hit-frame>1</Hsp_hit-frame>\n')
                fo.write('<Hsp_positive>' + str(data[20]) + '</Hsp_positive>\n')
                fo.write('<Hsp_align-len>' + str(data[16]) + '</Hsp_align-len>\n')
                fo.write('</Hsp>\n')
                fo.write('</Hit_hsps>\n')
                fo.write('</Hit>\n')
                fo.write('</Iteration_hits>\n')
                fo.write('</Iteration>\n')
                fo.write('</BlastOutput_iterations>\n')
                fo.write('</BlastOutput>\n\n\n')
                fo.flush()

        print('%d sequences have been parsed.' % (query_count))
    sys.exit()

if __name__ == "__main__":
    main()
