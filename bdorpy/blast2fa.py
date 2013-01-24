#!/usr/bin/env python
#
# blast2fa - Extract sequeneces from the blast result
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.19
#
# Required:
# * Biopython: http://biopython.org
#
# Usage: blast2fa <blast.xml> <output_dir> [options]
#
# Options:
# -e NUM: evalue thresh (default: 0.01)
# -n STR: a list of query IDs for selected parsing
# -h NUM: minimun number of hit sequences (default: 1)
#
# This script will output fasta files in where the first sequence is query, and the
# others are HSP sequences. They can be used for WildSpan or other purposes.

import os
import argparse
from Bio.Blast import NCBIXML
from fhandle import name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_blast')
    parser.add_argument('dir_output', nargs='?', default='blast2fa_outdir_' + name.genid())
    parser.add_argument('-e', dest='ev_thresh', type=float, default=0.01)
    parser.add_argument('-n', dest='file_id')
    parser.add_argument('-h', dest='min_hit_num', type=int, default=1)
    args = parser.parse_args()

    if not os.path.exists(args.dir_output):
            os.makedirs(args.dir_output)

    with open(args.file_blast, 'r') as result_handle:
        blast_records = NCBIXML.parse(result_handle)

        if args.file_id is not None:
            id_list = []
            with open(args.file_id, 'r') as fid:
                for line in fid:
                    id_list.append(line.rstrip())

        parsed_count = 0

        for blast_record in blast_records:
            if args.file_id is not None and blast_record.query not in id_list:
                continue

            if len(blast_record.alignments) < args.min_hit_num:
                continue

            with open(os.path.abspath(args.dir_output) + '/' + blast_record.query + '-wsinput.fa', 'w') as fw:
                fw.write('>' + blast_record.query + '\n')
                fw.flush()

                for alignment in blast_record.alignments:
                    for hsp in alignment.hsps:
                        # if blast_record.query in alignment.title:
                        #     continue

                        fw.write(hsp.query.replace('-', '') + '\n')

                        if hsp.expect <= args.ev_thresh:
                            fw.write('>' + alignment.title + '\n')
                            fw.write(hsp.sbjct.replace('-', '') + '\n')
                            fw.flush()
                        training_count += 1

            if training_count == 0:
                os.remove(os.path.abspath(args.dir_output) + '/' + blast_record.query + '-wsinput.fa')
                remove_count += 1

            print('Training set: ' + blast_record.query + '\t' + str(training_count))

        print('Removed: ' + str(remove_count))
