#!/usr/bin/env python3
#
# parser.py
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)

import re
import sys
from libmsaparser import sequence
from libmsaparser import converter


def writeheader(handle):
    handle.write('\t'.join(['msa_method',
                            'hit_name',
                            'query_names',
                            'res_eq_susp_num',
                            'rec_eq_susp_num',
                            'rec_eq_res_num',
                            'res_eq_susp_profile',
                            'rec_eq_susp_profile',
                            'rec_eq_res_profile',
                            'block_positions']) +
                 '\n')

    handle.flush()


class Parser:

    def __init__(self,
                 root,
                 filename,
                 susplist,
                 reslist,
                 reclist,
                 reference):
        self.order = []
        self.clutitle = sequence.Clutitle()
        self.space = sequence.Space()
        self.susp = sequence.Susp()
        self.res = sequence.Res()
        self.rec = sequence.Rec()
        self.star = sequence.Star()
        self.groups = [self.susp, self.res, self.rec]
        self.hit_src_name = reference
        match = re.match(r'(.+).clu', filename)
        if match is None:
            sys.exit("Error! The filename '" + filename + "' is not correct.")
        else:
            self.hit_name = match.group(1)

        for line in open(root + "/" + filename, 'r'):
            if re.search(r'CLUSTAL', line):
                self.clutitle.read(line)
                self.order.append(self.clutitle)
                if re.search(r'MAFFT', line):
                    self.msa_method = 'MAFFT'
                else:
                    self.msa_method = 'CLUSTAL'
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

    def analyze(self,
                block_starpct,
                block_length,
                source_name,
                formats,
                star_check_number):
        self.res_eq_susp_num = 0
        self.rec_eq_susp_num = 0
        self.rec_eq_res_num = 0
        self.res_eq_susp_profile = []
        self.rec_eq_susp_profile = []
        self.rec_eq_res_profile = []
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
            real_block_length = i[1] - i[0] + 1
            real_starpct = self.star.get_starnum(i[0], i[1]) / real_block_length

            if block_length > real_block_length:
                continue

            if block_starpct > real_starpct:
                continue

            self.block_poslist.append(str(i[0]) + '..' + str(i[1]) +
                                      ' L=' + str(i[1] - i[0] + 1) +
                                      ' SP=' + str(round(real_starpct, 2)))

            for j in range(i[0], i[1] + 1):
                rsd_susp = self.susp.get_residue(j)
                rsd_res = self.res.get_residue(j)
                rsd_rec = self.rec.get_residue(j)

                if rsd_susp == 'X' or rsd_res == 'X' or rsd_rec == 'X':
                    continue

                if rsd_res == rsd_susp and rsd_res != rsd_rec:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.res_eq_susp_num += 1
                        self.res_eq_susp_profile.append(self.res.get_residues(j - 2, j + 2) +
                                                        ':' +
                                                        self.rec.get_residues(j - 2, j + 2))
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_res_eq_susp'])
                    continue

                if rsd_rec == rsd_susp and rsd_rec != rsd_res:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.rec_eq_susp_num += 1
                        self.rec_eq_susp_profile.append(self.rec.get_residues(j - 2, j + 2) +
                                                        ':' +
                                                        self.res.get_residues(j - 2, j + 2))
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_rec_eq_susp'])
                    continue

                if rsd_rec == rsd_res and rsd_rec != rsd_susp:
                    if self.star.neighbor_star_check(j, star_check_number):
                        self.rec_eq_res_num += 1
                        self.rec_eq_res_profile.append(self.rec.get_residues(j - 2, j + 2) +
                                                        ':' +
                                                        self.susp.get_residues(j - 2, j + 2))
                        for g in self.groups:
                            g.set_htmltag(j, formats['class_rec_eq_res'])
                    continue

    def get_data(self):
        if not self.res_eq_susp_profile:
            res_eq_susp_profile = ['NA']
        else:
            res_eq_susp_profile = self.res_eq_susp_profile
        if not self.rec_eq_susp_profile:
            rec_eq_susp_profile = ['NA']
        else:
            rec_eq_susp_profile = self.rec_eq_susp_profile
        if not self.rec_eq_res_profile:
            rec_eq_res_profile = ['NA']
        else:
            rec_eq_res_profile = self.rec_eq_res_profile
        if not self.block_poslist:
            block_poslist = ['NA']
        else:
            block_poslist = self.block_poslist
        main = ('\t'.join([self.msa_method,
                           self.hit_name,
                           ','.join(self.query_names),
                           str(self.res_eq_susp_num),
                           str(self.rec_eq_susp_num),
                           str(self.rec_eq_res_num),
                           ','.join(res_eq_susp_profile),
                           ','.join(rec_eq_susp_profile),
                           ','.join(rec_eq_res_profile),
                           ','.join(block_poslist)]) +
                '\n')

        html = []
        for i in self.order:
            for s in i.get_html():
                html.append(s)

        return {'main': main, 'html_fname': self.hit_name, 'html': html}
