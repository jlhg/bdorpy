#!/usr/bin/env python3
#
# config.py -- Loading config files
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)

import configparser
import argparse


def get_configuration(root_dir):
    options = define_and_parse_options(root_dir + "/config/defaults.cfg")
    opt_others = process_configuration_files(options, root_dir)
    return (options, opt_others)


def define_and_parse_options(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source-directory', dest='source_directory', required=True,
                        help='the path MSA files stored')
    parser.add_argument('-o', '--output-directory', dest='output_directory', required=True,
                        help='the path output files stored')
    parser.add_argument('-Q', '--query-species', dest='assembly',
                        default=config.get('Group', 'assembly'),
                        help='the synonym of species name of aligned sequences. (e.g. For '
                        'Bactrocera dorsalis, the synonym is \'bdor\')')
    parser.add_argument('-H', '--hit-species', dest='reference',
                        default=config.get('Group', 'reference'),
                        help='the synonym of reference species name')
    parser.add_argument('-T', '--block-starred-percentage', dest='block_starpct', type=float,
                        default=0.9,
                        help='star percentage in block (default: 0.9)')
    parser.add_argument('-L', '--block-length', dest='block_length', type=int,
                        default=10,
                        help='block length (default: 10)')
    parser.add_argument('-C', '--star-checknumber', dest='star_check_number', type=int,
                        default=5,
                        help='the +- range for checking star number (default: 5)')
    parser.add_argument('-p', dest='process_num', type=int, default=1,
                        help='number of threads (CPUs) to use (default: 1)')
    return parser.parse_args()


def process_configuration_files(options, root_dir):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(root_dir + "/config/group.cfg")
    config.read(root_dir + "/config/defaults.cfg")
    opt_others = {'susplist': config.get('Susp', options.assembly).split(',')}
    opt_others.update({'reslist': config.get('Res', options.assembly).split(',')})
    opt_others.update({'reclist': config.get('Rec', options.assembly).split(',')})
    opt_others.update({'reference': dict(config.items('Source Name'))[options.reference]})
    opt_others.update({'source_name': dict(config.items('Source Name'))})
    opt_others.update({'output_files': dict(config.items('Output File'))})
    opt_others.update({'format': dict(config.items('Format'))})
    return opt_others
