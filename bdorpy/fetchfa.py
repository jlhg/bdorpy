#!/usr/bin/env python
#
# fetchfa - Fetch fasta files from Entrez
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.24
#
# Required:
# * Biopython: http://biopython.org
#
# Usage: batchgfa <term.list> [options]
# -d, --db     STR: database (default: protein)
# -q, --query  STR: accessions. If this option is specifid, the script will use the values
#                   to fetch data, and no input file required to be handled.
#                   Support multiple accession. (comma-separated)
# -o, --output STR: output directory or file (defualt: fetchfa_xxx) xxx: Random strings
#
# Input format (tab-separated):
# col #    title
# 0        filename
# 1        accession_1,accession_2, ...

import os
import argparse
from Bio import Entrez
from fhandle import name

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_list', nargs='?')
    parser.add_argument('-d', '--db', dest='ent_database', default='protein')
    parser.add_argument('-q', '--query', dest='query_id')
    parser.add_argument('-o', '--output', dest='file_output', default='fetchfa_out_' + name.genid())
    args = parser.parse_args()

    if args.query_id is not None:
        handle = Entrez.efetch(db=args.database, id=args.query_id, rettype='fasta', retmode='text')

        with open(args.file_output, 'w') as fw:
            fw.write(handle.read())
            fw.flush()
    else:
        if not os.path.exists(args.file_output):
            os.makedirs(args.file_output)

        with open(args.file_list, 'r') as fin:
            for line in fin:
                if line[0] == '#':
                    continue
                with open(os.path.abspath(args.file_output) + '/' + line.split('\t')[0], 'w') as fw:
                    handle = Entrez.efetch(db=args.database, id=line.split('\t')[1].rstrip(),
                                           rettype='fasta', retmode='text')
                    fw.write(handle.read())
