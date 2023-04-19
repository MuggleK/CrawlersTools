# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 14:48
# @Author  : MuggleK
# @File    : time_process.py

import datetime
import re
import time


def format_time(time_str, struct_return=False):
    """
    :param time_str:
    :param struct_return:
    :return:
    """

    struct_time = None
    time_format_str = "%Y-%m-%d"
    time_old_format = '%b %d %Y %I:%M%p'
    try:
        timestamp = time_str if isinstance(time_str, int) else int(time_str)
        if timestamp >= 0:
            time_array = time.localtime(timestamp)
            struct_time = time_array if struct_return else time.strftime(time_format_str, time_array)
        else:
            date_time = datetime.datetime(1970, 1, 2) + datetime.timedelta(seconds=timestamp)
            struct_time = time.strptime(time_str, time_format_str) if struct_return else date_time
    except ValueError:
        reg = r'(\d{4}).*?([0-1]?\d).*?([0-3]?\d)'
        time_str = re.search(reg, time_str)
        if time_str:
            year = time_str.group(1)
            month = time_str.group(2)
            day = time_str.group(3)
            time_str = year + "-" + month + "-" + day
            struct_time = time.strptime(time_str, time_format_str) if struct_return else time_str
    if not struct_time and time_str:
        struct_time = datetime.datetime.strptime(time_str, time_old_format)

    if struct_return:
        return struct_time
    if struct_time: return str(struct_time)


def compare_time(time_min, time_max):
    time_min_format = format_time(time_min, struct_return=True)
    time_max_format = format_time(time_max, struct_return=True)
    if time_min_format < time_max_format:
        return True
