#!/usr/bin/env python3
#
# calc
#
# Copyright (C) 2013, Jian-Long Huang
# Licensed under The MIT License
# http://opensource.org/licenses/MIT
#
# Author: Jian-Long Huang (jianlong@ntu.edu.tw)
# Created: 2013.2.8


def get_overlap(first_position_tuple, second_position_tuple):
    first_start, first_end = first_position_tuple
    second_start, second_end = second_position_tuple

    if first_start < second_start < first_end:
        if first_start < second_end < first_end:
            return first_start, first_end
        else:
            return first_start, second_end
    elif second_start < first_start < second_end:
        if second_start < first_end < second_end:
            return second_start, second_end
        else:
            return second_start, first_end
    else:
        return None


def get_non_overlap(first_position_tuple, second_position_tuple):
    first_start, first_end = first_position_tuple
    second_start, second_end = second_position_tuple

    if first_end < second_start:
        return first_start, second_end
    elif second_end < first_start:
        return second_start, first_end
    else:
        return None
