#!/usr/bin/env python3
#
# expfa - Extract sequences by ID
#
# Copyright (C) 2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.1
# Created: 2013.1.20
#
# Usage: expfa <fasta> <id_list> <output> [options]
#
# Options:
# -f: Fuzzy mode. If this option is specified, any headers include the ID
#     will be extracted.
# -n: Use ID as header name

import argparse
from fhandle import fa, lists

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_fasta')
    parser.add_argument('file_id_list')
    parser.add_argument('file_output')
    parser.add_argument('-f', dest='fuzzy', action='store_true')
    parser.add_argument('-n', dest='idname', action='store_true')
    args = parser.parse_args()

    seqs = fa.to_hash(args.file_fasta)
    id_list = lists.to_list(args.file_id_list)
    count = 0

    with open(args.file_output, 'w') as fw:
        if args.fuzzy is True:
            for header in seqs:
                for line in id_list:
                    if line in header:
                        fw.write('>')
                        if args.idname is True:
                            fw.write(line + '\n')
                            fw.write(seqs[header] + '\n')
                        else:
                            fw.write(header + '\n')
                            fw.write(seqs[header] + '\n')
                        count += 1
                        fw.flush()
        else:
            for line in id_list:
                fw.write('>')
                if args.idname is True:
                    fw.write(line + '\n')
                    fw.write(seqs[header] + '\n')
                else:
                    fw.write(header + '\n')
                    fw.write(seqs[header] + '\n')
                count += 1
                fw.flush()

    print('# of sequence in fasta: %d' % (len(seqs)))
    print('# of sequence in list: %d' % (len(id_list)))
    print('Successfully extracted: %d' % (count))
