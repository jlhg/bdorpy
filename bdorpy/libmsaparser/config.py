#!/usr/bin/env python3
#
# config.py -- Loading config files
#
# Copyright (C) 2012-2013, Jian-Long Huang
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
    parser.add_argument("-s", "--source-directory", dest="source_directory",
                        help="where MSA files stored", required=True)
    parser.add_argument("-o", "--output-directory", dest="output_directory",
                        help="where output files stored", required=True)
    parser.add_argument("-Q", "--query-species", dest="assembly",
                        default=config['Group']['assembly'],
                        help="query species")
    parser.add_argument("-H", "--hit-species", dest="reference",
                        default=config['Group']['reference'],
                        help="hit species")
    parser.add_argument("-T", "--block-starred-percentage", dest="block_starpct",
                        type=float, default=config['Rule']['block_starpct'],
                        help="the percentage of star in block")
    parser.add_argument("-L", "--block-length", dest="block_length", type=int,
                        default=config['Rule']['block_length'],
                        help="block length")
    parser.add_argument("-C", "--star-checknumber", dest="star_check_number",
                        type=int, default=config['Rule']['star_check_number'],
                        help="star check number")
    parser.add_argument("-p", dest="process_num", type=int, default=1,
                        help="multi-threads")
    return parser.parse_args()


def process_configuration_files(options, root_dir):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(root_dir + "/config/group.cfg")
    config.read(root_dir + "/config/defaults.cfg")
    opt_others = {'susplist': config['Susp'][options.assembly].split(',')}
    opt_others.update({'reslist': config['Res'][options.assembly].split(',')})
    opt_others.update({'reclist': config['Rec'][options.assembly].split(',')})
    opt_others.update({'reference': dict(config.items('Source Name'))[options.reference]})
    opt_others.update({'source_name': dict(config.items('Source Name'))})
    opt_others.update({'output_files': dict(config.items('Output File'))})
    opt_others.update({'format': dict(config.items('Format'))})
    return opt_others
