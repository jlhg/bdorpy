#!/usr/bin/env python3
#
# commutate - Find the common mutation profile
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.3
# Created: 2012.2.5
#
# Usage: commutate <input.msap> [options]
#
# Options:
# -o, --output-directory STR: output directory. If this option is not specified, the script will generate
#                             one with unique identifier at current directory.
#
# Support multiple input files and Unix style pathname pattern.
# For example:
# * commutate <a.msap> <b.msap> ...
# * commutate <*.msap> ...

import os
import sys
import argparse
from fhandle import name


def get_common_hitname(source):
    """Return a set of common hitnames."""
    common_hitname = set()

    for i in source:
        if not common_hitname:
            common_hitname.update(set(source[i].keys()))
        else:
            common_hitname.intersection_update(set(source[i].keys()))

            if not common_hitname:
                print('No common hits.')
                sys.exit()

    return common_hitname


def get_common_mutate(source, common_hitname):
    """Return a dict of hitname and its set of common mutation profiles."""
    common_mutation_profile = {}

    for hitname in common_hitname:
        mutation_profile = set()

        for i in source:
            if not mutation_profile:
                mutation_profile.update(source[i][hitname])
            else:
                mutation_profile.intersection_update(source[i][hitname])

                if not mutation_profile:
                    common_mutation_profile.update({hitname: '-'})
                    break
        else:
            common_mutation_profile.update({hitname: mutation_profile})

    return common_mutation_profile


def writefile(output_file, common_mutation_profile):
    with open(output_file, 'w') as fw:
        hitnum = len(common_mutation_profile.keys())
        has_common_mutate_num = len(common_mutation_profile.values()) - list(common_mutation_profile.values()).count('-')
        has_common_mutate = filter(lambda a: a != '-', list(common_mutation_profile.values()))
        fw.write('# Total common hits: ' + str(hitnum) + '\n')
        fw.write('# Has common mutation profile(s): ' + str(has_common_mutate_num) + '\n')
        fw.write('# Total common mutation profiles: ' + str(sum(map(len, has_common_mutate))) + '\n\n')
        fw.write('\t'.join(['hitname',
                            'mutation_profile_num',
                            'mutation_rofiles']))
        fw.write('\n')

        for key, value in common_mutation_profile.items():
            if value == '-':
                profile_num = 0
            else:
                profile_num = len(value)

            fw.write('\t'.join([key,
                                str(profile_num),
                                ','.join(value)]))
            fw.write('\n')

        fw.flush()


def main():
    parser = argparse.ArgumentParser(description='commutate - Find the common mutation profile')
    parser.add_argument('input', nargs='*')
    parser.add_argument('-o', '--output-directory', dest='output', default='commutate_out_' + name.genid(),
                        help='output directory. If this option is not specified, the script will generate '
                        'one with unique identifier at current directory.')
    args = parser.parse_args()

    args.output = args.output.rstrip('/')

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    source = []
    source_res_eq_susp = {}
    source_rec_eq_susp = {}
    source_rec_eq_res = {}

    for afile in args.input:
        source.append(afile)
        source_res_eq_susp[afile] = {}
        source_rec_eq_susp[afile] = {}
        source_rec_eq_res[afile] = {}

        with open(afile, 'r') as fin:
            for line in fin:
                if line.lstrip() == '' or line.lstrip()[0] in ('#', 'm'):
                    continue
                data = line.rstrip().split('\t')
                if int(data[3]) > 0:
                    source_res_eq_susp[afile].update({data[1]: set(data[6].split(','))})
                if int(data[4]) > 0:
                    source_rec_eq_susp[afile].update({data[1]: set(data[7].split(','))})
                if int(data[5]) > 0:
                    source_rec_eq_res[afile].update({data[1]: set(data[8].split(','))})

    common_hitname_res_eq_susp = get_common_hitname(source_res_eq_susp)
    common_mutation_profile_res_eq_susp = get_common_mutate(source_res_eq_susp, common_hitname_res_eq_susp)

    common_hitname_rec_eq_susp = get_common_hitname(source_rec_eq_susp)
    common_mutation_profile_rec_eq_susp = get_common_mutate(source_rec_eq_susp, common_hitname_rec_eq_susp)

    common_hitname_rec_eq_res = get_common_hitname(source_rec_eq_res)
    common_mutation_profile_rec_eq_res = get_common_mutate(source_rec_eq_res, common_hitname_rec_eq_res)

    writefile(args.output + '/common_mutation_profile_res_eq_susp.txt', common_mutation_profile_res_eq_susp)
    writefile(args.output + '/common_mutation_profile_rec_eq_susp.txt', common_mutation_profile_rec_eq_susp)
    writefile(args.output + '/common_mutation_profile_rec_eq_res.txt', common_mutation_profile_rec_eq_res)

if __name__ == "__main__":
    main()
