#!/usr/bin/env python3
#
# msaparser.py
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.3.0

import sys
import os
from multiprocessing import Queue, Process

# Check version
if sys.version < '3.0':
    your_version = sys.version.split(' ')[0]
    print('* Your Python version (%s) is too old! Please upgrade to 3.0+!' % your_version)
    sys.exit(1)

from libmsaparser import config, msaio, parser


def begin_parse(queue_work, queue_write):
    while True:
        (root, filename) = queue_work.get(block=False)
        parse = parser.Parser(root, filename, opt_others['susplist'], opt_others['reslist'],
                              opt_others['reclist'], opt_others['reference'])
        parse.analyze(options.block_starpct, options.block_length, opt_others['source_name'],
                      opt_others['format'], options.star_check_number)
        queue_write.put(parse.get_data())


def write_result(queue_write, output_dir, files):
    while True:
        data = queue_write.get(timeout=20)
        fw_main = open(output_dir + '/' + files['main'], 'a')
        fw_main.write(''.join(data['main']))
        fw_main.flush()
        fw_main.close()
        fw_simple = open(output_dir + '/' + files['simple'], 'a')
        fw_simple.write(''.join(data['simple']))
        fw_simple.flush()
        fw_simple.close()

if __name__ == '__main__':
    (options, opt_others) = config.get_configuration(os.path.dirname(os.path.abspath(__file__)))

    """Check if output files exist or not"""
    if os.path.exists(options.output_directory.rstrip('/') + '/' + opt_others['output_files']['main']):
        sys.exit("Error! The file '" + opt_others['output_files']['main'] + "' exists.")
    if os.path.exists(options.output_directory.rstrip('/') + '/' + opt_others['output_files']['simple']):
        sys.exit("Error! The file '" + opt_others['output_files']['simple'] + "' exists.")

    parser.writeheader(options.output_directory.rstrip('/'), opt_others['output_files'])

    msainput = msaio.FileInput(options.source_directory)
    q_work = Queue()

    for i in msainput.files:
        q_work.put(i)

    q_write = Queue()

    proc_work = []
    for i in range(0, options.process_num):
        proc_work.append(Process(target=begin_parse, args=(q_work, q_write)))

    proc_write = Process(target=write_result, args=(q_write, options.output_directory.rstrip('/'),
                                                    opt_others['output_files']))

    for proc in proc_work:
        proc.start()

    proc_write.start()

    for proc in proc_work:
        proc.join()

    proc_write.join()
