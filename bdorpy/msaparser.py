#!/usr/bin/env python3.3
#
# msaparser - Parse MSA results
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 2.0
#
# Requirement:
# * Python >= 3.3
#
# Usage: msaparser -s <source_dir> -o <output_dir> [options]
#
# Options:
# -s, --source-directory      STR: the path MSA files stored (required)
# -o, --output-directory      STR: the path output files sotred (required)
# -Q, --query-species         STR: the synonym of species name of aligned sequences
#                                  (e.g. For Bactrocera dorsalis, the synonym is 'bdor')
# -H, --hit-species           STR: the synonym of reference species name
# -T, --block-star-percentage NUM: star percentage in block (default: 0.9)
# -L, --block-length          NUM: block length (default: 10)
# -C, --star-checknumber      NUM: the +- range for checking star number (default: 5)
# -p, --process               NUM: number of threads (CPUs) to use (default: 1)
#
# Formats:
# files in <source_dir>: clustal
# output: msap, html


import sys
import os
from multiprocessing import queues, pool, Manager
from libmsaparser import config, msaio, parser
from fhandle import logmsg


def begin_parse(root, filename, options, opt_others, q_write):
    parse = parser.Parser(root,
                          filename,
                          opt_others['susplist'],
                          opt_others['reslist'],
                          opt_others['reclist'],
                          opt_others['reference'])
    parse.analyze(options.block_starpct,
                  options.block_length,
                  opt_others['source_name'],
                  opt_others['format'],
                  options.star_check_number)
    q_write.put(parse.get_data())


def write_result(queue_write, output_dir, output_main):
    while True:
        try:
            data = queue_write.get(block=False)
            with open(output_main, 'a') as fw_main:
                fw_main.write(data['main'])
                fw_main.flush()
            with open(output_dir + '/html/' + data['html_fname'] + '.html', 'w') as fw_html:
                fw_html.write(''.join(data['html']))
                fw_html.flush()
        except queues.Empty:
            break


def main():
    # Check version
    if sys.version < '3.3':
        your_version = sys.version.split(' ')[0]
        print('* Your Python version (%s) is too old! Please upgrade to 3.3+!' % your_version)
        sys.exit()

    proglog = logmsg.message(prog='msaparser', cmd=' '.join(sys.argv))

    options, opt_others = config.get_configuration(os.path.dirname(os.path.abspath(__file__)))
    options.output_directory = options.output_directory.rstrip('/')
    options.source_directory = options.source_directory.rstrip('/')

    if not os.path.exists(options.output_directory + '/html'):
        os.makedirs(options.output_directory + '/html')

    mainfile = options.output_directory + '/' + opt_others.get('output_files').get('main')

    with open(mainfile, 'w') as fw:
        for msg in proglog.start_message():
            fw.write(msg)
        fw.write('\n')
        fw.flush()
        parser.writeheader(fw)

    cluinput = msaio.FileInput(options.source_directory)

    proc_manager = Manager()
    q_write = proc_manager.Queue()
    proc = pool.Pool(processes=options.process_num)

    while cluinput.files:
        if len(cluinput.files) / 100 >= 1:
            files = cluinput.files[0:100]
            cluinput.files = cluinput.files[100:]
        else:
            files = cluinput.files[0:len(cluinput.files)]
            cluinput.files = cluinput.files[len(cluinput.files):]

        tasks = []

        for root, filename in files:
            tasks.append((root, filename, options, opt_others, q_write))

        proc.starmap(begin_parse, tasks)
        write_result(q_write, options.output_directory, mainfile)

    with open(mainfile, 'a') as fw:
        fw.write('\n')
        for msg in proglog.end_message():
            fw.write(msg)
        fw.flush()

if __name__ == '__main__':
    main()
