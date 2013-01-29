#!/usr/bin/env python3
#
# msastats.py
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Version: 0.3
# Created: 2012.1.7
#
# Usage: msapstats.py <msap-simple> <output_dir>
#
# Columns:
# 0	msa_method
# 1	hit_name
# 2	aln_hspno
# 3	query_names
# 4	res_like_susp
# 5	rec_like_susp
# 6	rec_like_res
# 7	hit_src_name
# 8	query_src_names
# 9	block_positions

import sys
import os


def main():
    outdir = os.path.abspath(sys.argv[2])

    if (os.path.exists(outdir)):
        sys.exit("Directory '" + outdir + "' exists")
    else:
        os.mkdir(outdir)

    fin = open(sys.argv[1], 'r')
    fstats = open(outdir + '/msap.stats', 'w')
    fidm_s_rs = open(outdir + '/susp-reseqsusp.idmap', 'w')
    fidm_s_rs_s = open(outdir + '/susp-reseqsusp-sole.idmap', 'w')
    fidm_r_rs = open(outdir + '/res-reseqsusp.idmap', 'w')
    fidm_r_rs_s = open(outdir + '/res-reseqsusp-sole.idmap', 'w')
    fidm_c_rs = open(outdir + '/rec-reseqsusp.idmap', 'w')
    fidm_c_rs_s = open(outdir + '/rec-reseqsusp-sole.idmap', 'w')
    fidm_s_cs = open(outdir + '/susp-receqsusp.idmap', 'w')
    fidm_s_cs_s = open(outdir + '/susp-receqsusp-sole.idmap', 'w')
    fidm_r_cs = open(outdir + '/res-receqsusp.idmap', 'w')
    fidm_r_cs_s = open(outdir + '/res-receqsusp-sole.idmap', 'w')
    fidm_c_cs = open(outdir + '/rec-receqsusp.idmap', 'w')
    fidm_c_cs_s = open(outdir + '/rec-receqsusp-sole.idmap', 'w')
    fidm_s_cr = open(outdir + '/susp-receqres.idmap', 'w')
    fidm_s_cr_s = open(outdir + '/susp-receqres-sole.idmap', 'w')
    fidm_r_cr = open(outdir + '/res-receqres.idmap', 'w')
    fidm_r_cr_s = open(outdir + '/res-receqres-sole.idmap', 'w')
    fidm_c_cr = open(outdir + '/rec-receqres.idmap', 'w')
    fidm_c_cr_s = open(outdir + '/rec-receqres-sole.idmap', 'w')
    fidm_s = open(outdir + '/susp-all.idmap', 'w')
    fidm_r = open(outdir + '/res-all.idmap', 'w')
    fidm_c = open(outdir + '/rec-all.idmap', 'w')

    fin.readline()  # remove first line
    res_eq_susp = rec_eq_susp = rec_eq_res = 0
    res_eq_susp_only = rec_eq_susp_only = rec_eq_res_only = 0
    res_eq_susp_a = rec_eq_susp_a = rec_eq_res_a = 0
    res_eq_susp_only_a = rec_eq_susp_only_a = rec_eq_res_only_a = 0
    susp_like = res_like = rec_like = union_all = 0

    for line in fin:
        data = line.split('\t')

        if int(data[4]) > 0:
            res_eq_susp += int(data[4])
            res_eq_susp_a += 1
            fidm_s_rs.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_rs.write(data[1] + '\n')
            fidm_s_rs.flush()
            fidm_r_rs.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_rs.write(data[1] + '\n')
            fidm_r_rs.flush()
            fidm_c_rs.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_rs.write(data[1] + '\n')
            fidm_c_rs.flush()

        if int(data[5]) > 0:
            rec_eq_susp += int(data[5])
            rec_eq_susp_a += 1
            fidm_s_cs.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_cs.write(data[1] + '\n')
            fidm_s_cs.flush
            fidm_r_cs.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_cs.write(data[1] + '\n')
            fidm_r_cs.flush()
            fidm_c_cs.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_cs.write(data[1] + '\n')
            fidm_c_cs.flush()

        if int(data[6]) > 0:
            rec_eq_res += int(data[6])
            rec_eq_res_a += 1
            fidm_s_cr.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_cr.write(data[1] + '\n')
            fidm_s_cr.flush()
            fidm_r_cr.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_cr.write(data[1] + '\n')
            fidm_r_cr.flush()
            fidm_c_cr.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_cr.write(data[1] + '\n')
            fidm_c_cr.flush()

        if int(data[4]) > 0 and int(data[5]) == 0 and int(data[6]) == 0:
            res_eq_susp_only += int(data[4])
            res_eq_susp_only_a += 1
            fidm_s_rs_s.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_rs_s.write(data[1] + '\n')
            fidm_s_rs_s.flush()
            fidm_r_rs_s.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_rs_s.write(data[1] + '\n')
            fidm_r_rs_s.flush()
            fidm_c_rs_s.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_rs_s.write(data[1] + '\n')
            fidm_c_rs_s.flush()

        if int(data[4]) == 0 and int(data[5]) > 0 and int(data[6]) == 0:
            rec_eq_susp_only += int(data[5])
            rec_eq_susp_only_a += 1
            fidm_s_cs_s.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_cs_s.write(data[1] + '\n')
            fidm_s_cs_s.flush
            fidm_r_cs_s.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_cs_s.write(data[1] + '\n')
            fidm_r_cs_s.flush()
            fidm_c_cs_s.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_cs_s.write(data[1] + '\n')
            fidm_c_cs_s.flush()

        if int(data[4]) == 0 and int(data[5]) == 0 and int(data[6]) > 0:
            rec_eq_res_only += int(data[6])
            rec_eq_res_only_a += 1
            fidm_s_cr_s.write(data[3].split('|')[0].split('(')[0] + '\t')
            fidm_s_cr_s.write(data[1] + '\n')
            fidm_s_cr_s.flush()
            fidm_r_cr_s.write(data[3].split('|')[1].split('(')[0] + '\t')
            fidm_r_cr_s.write(data[1] + '\n')
            fidm_r_cr_s.flush()
            fidm_c_cr_s.write(data[3].split('|')[2].split('(')[0] + '\t')
            fidm_c_cr_s.write(data[1] + '\n')
            fidm_c_cr_s.flush()

        if int(data[4]) > 0 or int(data[5]) > 0:
            susp_like += 1

        if int(data[5]) > 0 or int(data[6]) > 0:
            rec_like += 1

        if int(data[6]) > 0 or int(data[4]) > 0:
            res_like += 1

        if int(data[4]) > 0 or int(data[5]) > 0 or int(data[6]) > 0:
            union_all += 1

        fidm_s.write(data[3].split('|')[0].split('(')[0] + '\t')
        fidm_s.write(data[1] + '\n')
        fidm_s.flush()
        fidm_r.write(data[3].split('|')[1].split('(')[0] + '\t')
        fidm_r.write(data[1] + '\n')
        fidm_r.flush()
        fidm_c.write(data[3].split('|')[2].split('(')[0] + '\t')
        fidm_c.write(data[1] + '\n')
        fidm_c.flush()

    fstats.write('The number of variated amino acid:\n'
                 '- Res eq Susp: ' + str(res_eq_susp) + '\n'
                 '- Rec eq Susp: ' + str(rec_eq_susp) + '\n'
                 '- Rec eq Res : ' + str(rec_eq_res) + '\n'
                 '- Res eq Susp (sole): ' + str(res_eq_susp_only) + '\n'
                 '- Rec eq Susp (sole): ' + str(rec_eq_susp_only) + '\n'
                 '- Rec eq Res (sole):' + str(rec_eq_res_only) + '\n\n'
                 'The number of protein:\n'
                 '- Res eq Susp: ' + str(res_eq_susp_a) + '\n'
                 '- Rec eq Susp: ' + str(rec_eq_susp_a) + '\n'
                 '- Rec eq Res : ' + str(rec_eq_res_a) + '\n'
                 '- Res eq Susp (sole): ' + str(res_eq_susp_only_a) + '\n'
                 '- Rec eq Susp (sole): ' + str(rec_eq_susp_only_a) + '\n'
                 '- Rec eq Res (sole): ' + str(rec_eq_res_only_a) + '\n'
                 '- Res eq Susp or Rec eq Susp: ' + str(susp_like) + '\n'
                 '- Rec eq Susp or Rec eq Res : ' + str(rec_like) + '\n'
                 '- Rec eq Res  or Res eq Susp: ' + str(res_like) + '\n'
                 '- Res eq Susp or Rec eq Susp or Rec eq Res: ' + str(union_all) + '\n')
    fstats.flush()

    fin.close()
    fstats.close()
    fidm_s_rs.close()
    fidm_s_rs_s.close()
    fidm_r_rs.close()
    fidm_r_rs_s.close()
    fidm_c_rs.close()
    fidm_c_rs_s.close()
    fidm_s_cs.close()
    fidm_s_cs_s.close()
    fidm_r_cs.close()
    fidm_r_cs_s.close()
    fidm_c_cs.close()
    fidm_c_cs_s.close()
    fidm_s_cr.close()
    fidm_s_cr_s.close()
    fidm_r_cr.close()
    fidm_r_cr_s.close()
    fidm_c_cr.close()
    fidm_c_cr_s.close()

    sys.exit()

if __name__ == "__main__":
    main()
