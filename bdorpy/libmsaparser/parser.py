#!/usr/bin/env python3
#
# parser.py
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)

import re
import sys

from libmsaparser import sequence
from libmsaparser import converter


def writeheader(output_directory, output_files):
    fw_main = open(output_directory + '/' + output_files['main'], 'a')
    fw_simple = open(output_directory + '/' + output_files['simple'], 'a')
    fw_main.write("msa_method\t" + "hit_name\t" +
                  "aln_hspno\t" + "query_names\t" +
                  "clu_html\t" + "res_like_susp\t" +
                  "rec_like_susp\t" + "rec_like_res\t" +
                  "hit_src_name\t" + "query_src_names\t" +
                  "block_positions\n")
    fw_main.flush()
    fw_simple.write("msa_method\t" + "hit_name\t" +
                    "aln_hspno\t" + "query_names\t" +
                    "res_like_susp\t" + "rec_like_susp\t" +
                    "rec_like_res\t" + "hit_src_name\t" +
                    "query_src_names\t" + "block_positions\n")
    fw_simple.flush()
    fw_main.close()
    fw_simple.close()


class Parser:

    def __init__(self, root, filename, susplist, reslist, reclist, reference):
        self.order = []
        self.clutitle = sequence.Clutitle()
        self.space = sequence.Space()
        self.susp = sequence.Susp()
        self.res = sequence.Res()
        self.rec = sequence.Rec()
        self.star = sequence.Star()
        self.groups = [self.susp, self.res, self.rec]
        self.hit_src_name = reference
        match = re.match(r'(.+)-(\d+).clu', filename)
        if match is None:
            sys.exit("Error! The filename '" + filename + "' is not correct.")
        else:
            self.hit_name = match.group(1)
            self.aln_hspno = match.group(2)

        for line in open(root + "/" + filename, 'r'):
            if re.search(r'CLUSTAL O', line):
                self.clutitle.read(line)
                self.order.append(self.clutitle)
                self.msa_method = "CLUSTALO"
            elif re.search(r'^\n', line):
                self.space.read(line)
                self.order.append(self.space)
            elif any(re.search(grpsusp, line) for grpsusp in susplist):
                self.susp.read(line)
                self.order.append(self.susp)
            elif any(re.search(grpres, line) for grpres in reslist):
                self.res.read(line)
                self.order.append(self.res)
            elif any(re.search(grprec, line) for grprec in reclist):
                self.rec.read(line)
                self.order.append(self.rec)
            elif re.search(r'^\s', line):
                self.star.read(line)
                self.order.append(self.star)
            else:
                sys.exit('Error! please check groups.')

        self.block = []
        for i in range(self.susp.get_sequence_length()):
            if any(g.get_residue(i) == '-' for g in self.groups):
                continue
            else:
                self.block.append(i)
        self.block = converter.group_continuous_number(self.block)

    def analyze(self, block_starpct, block_length, source_name, formats, star_check_number):
        self.res_eq_susp = 0
        self.rec_eq_susp = 0
        self.rec_eq_res = 0
        self.clutitle.set_htmltag(formats['class_clutitle'])
        self.space.set_htmltag()
        self.star.set_htmltag()
        for g in self.groups:
            g.set_source(source_name)
        self.query_src_names = []
        self.query_names = []
        for g in self.groups:
            self.query_src_names.append(g.get_source())
            self.query_names.append(g.get_name())
        self.block_poslist = []

        for i in self.block:
            if (block_length > i[1] - i[0] + 1):
                continue
            if (block_starpct > self.star.get_star_percentage(i)):
                continue
            self.block_poslist.append(str(i[0]) + ".." + str(i[1]) +
                                      " L=" + str(i[1] - i[0] + 1) +
                                      " SP=" + str(round(self.star.get_star_percentage(i), 2)))
            for j in range(i[0], i[1]):
                rsd_susp = self.susp.get_residue(j)
                rsd_res = self.res.get_residue(j)
                rsd_rec = self.rec.get_residue(j)
                if rsd_susp == 'X' or rsd_res == 'X' or rsd_rec == 'X':
                    continue
                if rsd_res == rsd_susp and rsd_res != rsd_rec:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.res_eq_susp += 1
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_res_eq_susp'])
                    continue
                if rsd_rec == rsd_susp and rsd_rec != rsd_res:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.rec_eq_susp += 1
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_rec_eq_susp'])
                    continue
                if rsd_rec == rsd_res and rsd_rec != rsd_susp:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.rec_eq_res += 1
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_rec_eq_res'])
                    continue

    def get_data(self):
        main = []
        main.append(self.msa_method + "\t" + self.hit_name + "\t" +
                    self.aln_hspno + "\t" + '|'.join(self.query_names) + "\t")

        for i in self.order:
            for s in i.get_html():
                main.append(s)

        main.append("\t")
        main.append(str(self.res_eq_susp) + "\t" + str(self.rec_eq_susp) + "\t" +
                    str(self.rec_eq_res) + "\t" + self.hit_src_name + "\t" +
                    '|'.join(self.query_src_names) + "\t" + ', '.join(self.block_poslist) + "\n")

        simple = []
        simple.append(self.msa_method + "\t" + self.hit_name + "\t" +
                      self.aln_hspno + "\t" + '|'.join(self.query_names) + "\t" +
                      str(self.res_eq_susp) + "\t" + str(self.rec_eq_susp) + "\t" +
                      str(self.rec_eq_res) + "\t" + self.hit_src_name + "\t" +
                      '|'.join(self.query_src_names) + "\t" + ', '.join(self.block_poslist) + "\n")

        return {'main': main, 'simple': simple}
