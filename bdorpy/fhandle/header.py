#!/usr/bin/env python3
#
# header.py - The header object for formats
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Created: 2013.2.20


class blastlist:
    def __init__(self):
        self.aln_rank = 'aln_rank'
        self.aln_hspno = 'aln_hspno'
        self.aln_method = 'aln_method'
        self.query_name = 'query_name'
        self.hit_name = 'hit_name'
        self.query_length = 'query_length'
        self.query_hsp_start = 'query_hsp_start'
        self.query_hsp_end = 'query_hsp_end'
        self.query_strand = 'query_strand'
        self.query_frame = 'query_frame'
        self.hit_length = 'hit_length'
        self.hit_hsp_start = 'hit_hsp_start'
        self.hit_hsp_end = 'hit_hsp_end'
        self.hit_strand = 'hit_strand'
        self.hit_frame = 'hit_frame'
        self.hsp_score = 'hsp_score'
        self.hsp_bits = 'hsp_bits'
        self.hsp_evalue = 'hsp_evalue'
        self.hsp_length = 'hsp_length'
        self.hsp_gaps = 'hsp_gaps'
        self.hsp_identities = 'hsp_identities'
        self.hsp_identity_percent = 'hsp_identity_percent'
        self.hsp_positives = 'hsp_positives'
        self.hsp_positive_percent = 'hsp_positive_percent'
        self.query_coverage = 'query_coverage'
        self.hit_coverage = 'hit_coverage'
        self.hit_description = 'hit_description'

    def get_all_tab(self):
        return '\t'.join([self.aln_rank,
                          self.aln_hspno,
                          self.aln_method,
                          self.query_name,
                          self.hit_name,
                          self.query_length,
                          self.query_hsp_start,
                          self.query_hsp_end,
                          self.query_strand,
                          self.query_frame,
                          self.hit_length,
                          self.hit_hsp_start,
                          self.hit_hsp_end,
                          self.hit_strand,
                          self.hit_frame,
                          self.hsp_score,
                          self.hsp_bits,
                          self.hsp_evalue,
                          self.hsp_length,
                          self.hsp_gaps,
                          self.hsp_identities,
                          self.hsp_identity_percent,
                          self.hsp_positives,
                          self.hsp_positive_percent,
                          self.query_coverage,
                          self.hit_coverage,
                          self.hit_description])
