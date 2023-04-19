# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 16:59
# @Author  : MuggleK
# @File    : transfer_js.py

import ctypes
import difflib


def int_overflow(val: int):
    """
    Process JavaScript nums Overflow
    :param val:
    :return:
    """
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def right_shift(n, i):
    """
    Python Operator ">>"
    :param n:
    :param i:
    :return:
    """
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    if i != 0:
        return int_overflow(n >> i)
    else:
        return n


def string_similar(s1: str, s2: str):
    """
    Compare Strings Similar Percentage
    :param s1:
    :param s2:
    :return: :float: percentage
    """
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
