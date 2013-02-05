#!/usr/bin/env python
#
# commonfa - Generate fasta files of sequences with common hit
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 1.0
# Created: 2013.1.31
#
# Requirement:
# * Biopython: http://biopython.org
#
# Usage: -b <blastlist> -f <fasta> [options]
#
# Options:
# -b, --blastlist        STR: blastlist files (required)
# -f, --fasta            STR: fasta files (required)
# -o, --output-directory STR: output directory. If this option is not specified, the script will generate
#                             one with unique identifier at current directory.
# -p, --process          NUM: number of threads (CPUs) to use (default: 1)
#
# File formats:
# <blastlist>: blastlist
# <fasta>: fasta
#
# -b and -f options support multiple input files and Unix style pathname pattern.
# For example:
# * commonfa -b <a.blastlist> <b.blastlist> ... -b <a.fa> <b.fa> ..
# * commonfa -b <a*.blastlist> -b <a*.fa>
#
# This script is written for MSA.

import os
import re
import sys
import argparse
import ConfigParser
from subprocess import Popen, PIPE
from multiprocessing import Pool
from Bio import SeqIO
from fhandle import name, logmsg


def main():
    proglog = logmsg.message(prog='commonfa', cmd=' '.join(sys.argv))

    parser = argparse.ArgumentParser(description='commonfa - Generate fasta files of sequences with common hit')
    parser.add_argument('-b', '--blastlist', dest='input_files_blastlist', nargs='*', required=True,
                        help='blastlist files (required)')
    parser.add_argument('-f', '--fasta', nargs='*', dest='input_files_fasta', required=True,
                        help='fasta files (required)')
    parser.add_argument('-o', '--output-directory', dest='output', default='commonfa_out_' + name.genid(),
                        help='output directory. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    parser.add_argument('-p', '--process', dest='process_num', type=int, default=1,
                        help='number of threads (CPUs) to use')
    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(__file__)) + '/config/group.cfg')

    if not os.path.exists(args.output.rstrip('/') + '/msainput'):
        os.makedirs(args.output.rstrip('/') + '/msainput')

    fwlog = open(args.output.rstrip('.') + '/commonfa.log', 'w')

    for i in proglog.start_message():
        fwlog.write(i)

    fwlog.flush()

    awk_cmd = "awk -F'\t' '$5 ~ /ref/ { print $0 }' " + ' '.join(args.input_files_blastlist)
    sort_cmd = "sort -t$'\t' -k5d,5 -k18g,18 -k22gr,22 -k19gr,19 -k26gr,26 -k6gr"

    fwsort = open(args.output.rstrip('/') + '/sort.temp', 'w')
    awk_proc = Popen(awk_cmd, stdout=PIPE, executable='/bin/bash', shell=True)
    sort_proc = Popen(sort_cmd, stdin=awk_proc.stdout, stdout=fwsort, executable='/bin/bash', shell=True)
    sort_proc.communicate()
    fwsort.close()

    fasta = {}

    for filename in args.input_files_fasta:
        fasta.update(dict(SeqIO.index(filename, 'fasta')))

    susp_names = config.get('Susp', 'bdor').split(',')
    res_names = config.get('Res', 'bdor').split(',')
    rec_names = config.get('Rec', 'bdor').split(',')
    has_susp = has_res = has_rec = False
    commonhit = {}

    hitname = re.compile('.*gi\|\d*?\|(.*?)\|(.*?)\|.*')

    with open(args.output.rstrip('/') + '/sort.temp', 'r') as fin:
        for line in fin:
            data = line.split('\t')
            match = hitname.match(data[4])

            query_name = data[3]
            hit_name = match.group(2)
            query_frame = int(data[9])

            if hit_name in commonhit:
                if any(i in query_name for i in susp_names):
                    if has_susp is True:
                        continue
                    else:
                        has_susp = True

                if any(i in query_name for i in res_names):
                    if has_res is True:
                        continue
                    else:
                        has_res = True

                if any(i in query_name for i in rec_names):
                    if has_rec is True:
                        continue
                    else:
                        has_rec = True

                commonhit[hit_name].append((query_name, query_frame))
            else:
                commonhit[hit_name] = [(query_name, query_frame)]
                has_susp = has_res = has_rec = False

                if any(i in query_name for i in susp_names):
                    has_susp = True

                if any(i in query_name for i in res_names):
                    has_res = True

                if any(i in query_name for i in rec_names):
                    has_rec = True

    tasks = []
    parsed_num = 0

    for hit in commonhit:
        if len(commonhit[hit]) == len(args.input_files_blastlist):
            tasks.append((hit, commonhit[hit], fasta, args))
            parsed_num += 1

    pool = Pool(processes=args.process_num)
    pool.map(do_parsing, tasks)

    fwlog.write('# Parsed hits: ' + str(parsed_num) + '\n')

    for i in proglog.end_message():
        fwlog.write(i)

    fwlog.flush()


def do_parsing(tasks):
    hit, seqs, fasta, args = tasks
    with open(args.output.rstrip('/') + '/msainput/' + hit, 'w') as fw:
        for seq in seqs:
            query_name, frame = seq

            if frame < 0:
                fw.write('>' + query_name + '(' + str(frame) + ')\n')
                fw.write(fasta[query_name].seq.reverse_complement()[-frame - 1:].translate().tostring() + '\n\n')
            else:
                fw.write('>' + query_name + '(+' + str(frame) + ')\n')
                fw.write(fasta[query_name].seq[frame - 1:].translate().tostring() + '\n\n')

            fw.flush()

if __name__ == '__main__':
    main()
