#!/usr/bin/env python3
#
# sequence.py
#
# Copyright (C) 2012-2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)

import re
import sys

CLU_ALIGN_LENGTH_PER_LINE = 60


class Clutitle:

    def __init__(self):
        self.line = None

    def read(self, line):
        self.line = line

    def set_htmltag(self, classname):
        self.line = r'<span class="' + classname + r'">' + self.line.strip('\n') + r'</span><br>'

    def get_html(self):
        return self.line


class Space:

    def __init__(self):
        self.line = None

    def read(self, line):
        self.line = line

    def set_htmltag(self):
        self.line = "<br>"

    def get_html(self):
        return self.line


class Sequence:

    def __init__(self):
        self.name = None
        self.space = None
        self.sequence = []
        self.sequence_html = []
        self.source = None
        self.pattern = re.compile('(\S+?)(\s+?)(\S+?)\s')

    def read(self, line):
        match = self.pattern.match(line)
        if self.name is not None and self.name != match.group(1):
            sys.exit("Error! Too many sources in Susp group.")
        self.name = match.group(1)
        self.space = match.group(2)
        self.sequence = self.sequence + list(match.group(3))
        self.sequence_html = self.sequence_html + list(match.group(3))
        self.space = re.sub('\s', '&nbsp;', self.space)

    def get_sequence_length(self):
        return len(self.sequence)

    def get_residue(self, position):
        return self.sequence[position]

    def get_residues(self, start_pos, stop_pos):
        return ''.join(self.sequence[start_pos:stop_pos + 1])

    def set_htmltag(self, position, classname):
        self.sequence_html[position] = '<span class="' + classname + '">' + self.sequence[position] + '</span>'

    def get_html(self):
        yield self.name
        yield self.space
        for i in range(0, CLU_ALIGN_LENGTH_PER_LINE):
            if not self.sequence_html:
                break
            yield self.sequence_html[0]
            del self.sequence_html[0]
        yield "<br>"

    def get_name(self):
        return self.name

    def set_source(self, source_name):
        for srcname in source_name.keys():
            if re.search(srcname, self.name):
                self.source = source_name[srcname]
                break
        if self.source is None:
            print(self.name)
            print(source_name)
            sys.exit("Error! Please check source names.")

    def get_source(self):
        return self.source

    def get_raw_position(self, position):
        return len(''.join(self.sequence[0:position + 1]).replace('-', ''))


class Star:

    def __init__(self):
        self.line = []
        self.inalign = []
        self.rsdnum = 0
        self.inalign = ''

    def read(self, line):
        line = line.rstrip('\n')
        self.inalign = self.inalign + line[-CLU_ALIGN_LENGTH_PER_LINE:]
        self.line.append(re.sub(r'\s', '&nbsp;', line))

    def get_starnum(self, start, end):
        star_num = 0
        for i in range(start, end + 1):
            if self.inalign[i] == '*':
                star_num += 1
        return star_num

    def set_htmltag(self):
        pass

    def get_html(self):
        self.rsdnum += CLU_ALIGN_LENGTH_PER_LINE
        yield self.line[0]
        del self.line[0]
        yield "&nbsp;" + str(self.rsdnum) + "<br>"

    def neighbor_star_check(self, position, star_check_number):
        if position < star_check_number or position + star_check_number > len(self.inalign) - 1:
            """Mutation position is on sides, return False."""
            return False

        # if position < star_check_number:
        #     """Only check right side"""
        #     for i in range(position + 1, position + 1 + star_check_number):
        #         if self.inalign[i] == '*':
        #             star_num += 1
        #     if star_num >= star_check_number * 0.8:
        #         return True
        #     else:
        #         return False

        # if position + star_check_number > len(self.inalign) - 1:
        #     """Only check left side"""
        #     for i in range(position - star_check_number, position):
        #         if self.inalign[i] == '*':
        #             star_num += 1
        #     if star_num >= star_check_number * 0.8:
        #         return True
        #     else:
        #         return False

        # Check two sides
        star_num = 0

        for i in range(position + 1, position + 1 + star_check_number):
            if self.inalign[i] == '*':
                star_num += 1

        if star_num < star_check_number * 0.8:
            return False

        star_num = 0

        for i in range(position - star_check_number, position):
            if self.inalign[i] == '*':
                star_num += 1

        if star_num >= star_check_number * 0.8:
            return True
        else:
            return False
