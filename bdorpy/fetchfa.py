#!/usr/bin/env python
#
# fetchfa - Fetch fasta files from Entrez
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.3
# Created: 2013.1.24
#
# Required:
# * Biopython: http://biopython.org
#
# Usage: batchgfa <input.blastaccmap> [options]
# -d, --db     STR: database (default: protein)
# -q, --query  STR: accessions to be fetched. If this option is specifid, the script will use the values
#                   to fetch data, and no input file is required to be handled.
#                   Support multiple accession. (comma-separated).
# -o, --output STR: output directory or file name. If this option is not specified, the script will generate
#                   one with unique identifier at current directory.
# -l, --log    STR: log file name
#
# File formats:
# * input.blastaccmap: blastaccmap
# * output: fasta

import os
import sys
import argparse
from Bio import Entrez
from fhandle import name, logmsg


def main():
    proglog = logmsg.message(prog='fetchfa', cmd=' '.join(sys.argv))

    parser = argparse.ArgumentParser(description='fetchfa - Fetch fasta files from Entrez')
    parser.add_argument('input_file', nargs='?')
    parser.add_argument('-d', '--db', dest='database', default='protein',
                        help='database (default: protein)')
    parser.add_argument('-q', '--query', dest='query_id',
                        help='accessions to be fetched. If this option is specifid, the script will use the values '
                        'to fetch data, and no input file is required to be handled.')
    parser.add_argument('-o', '--output', dest='output', default='fetchfa_out_' + name.genid(),
                        help='output directory or file name. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    parser.add_argument('-l', '--log', dest='log_file',
                        help='log file name')
    args = parser.parse_args()

    if args.log_file is None:
        fwlog = open(args.output + '.log', 'w')
    else:
        fwlog = open(args.log_file, 'w')

    for i in proglog.start_message():
        fwlog.write(i)
    fwlog.flush()

    Entrez.email = 'fetchfa@example.com'

    if args.query_id is not None:
        with open(args.output + '.fa', 'w') as fw, open(args.output + '.log', 'w') as fwlog:
            handle = Entrez.efetch(db=args.database,
                                   id=args.query_id,
                                   rettype='fasta',
                                   retmode='text')

            fw.write(handle.read())
            fw.flush()

            fwlog.write('# Fetched sequences: ' + str(len(args.query_id.split(','))) + '\n')
            fwlog.write('#\n')

            for i in proglog.end_message():
                fwlog.write(i)
            fwlog.flush()
    else:
        if not os.path.exists(args.output):
            os.makedirs(args.output)

        with open(args.input_file, 'r') as fin:
            query_num = 0
            for line in fin:
                if line.lstrip() == '' or line.lstrip()[0] in ('#', 'a'):
                    continue

                query_num += 1

                with open(os.path.abspath(args.output) + '/' + line.split('\t')[0] + '.fa', 'w') as fw:
                    handle = Entrez.efetch(db=args.database,
                                           id=line.split('\t')[0] + ',' + line.split('\t')[1].rstrip(),
                                           rettype='fasta',
                                           retmode='text')
                    fw.write(handle.read())
            fwlog.write('# Fetched queries: ' + str(query_num) + '\n')
            fwlog.write('#\n')

            for i in proglog.end_message():
                fwlog.write(i)
            fwlog.flush()

    fwlog.close()

if __name__ == '__main__':
    main()
