# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 14:48
# @Author  : MuggleK
# @File    : time_process.py

import re
from datetime import datetime, timedelta

from cn2an import cn2an


class TimeProcessor:

    datetime_pattern = r"([0-9]{4}).*?([0-1]{0,1}[0-9]).*?([0-3]{0,1}[0-9])"

    def __init__(self, fmt="%Y-%m-%d"):
        self.fmt = fmt

    def format(self, string, struct=False):
        try:
            return self.process_timestamp(string, struct)
        except ValueError:
            print(f"非时间戳格式：{string}")
        try:
            return self.process_cn(string, struct)
        except (ValueError, TypeError):
            print(f"非特殊中文时间格式：{string}")

        re_res = re.search(self.datetime_pattern, string)
        date = f"{re_res.group(1)}-{re_res.group(2)}-{re_res.group(3)}"
        if struct:
            return datetime.strptime(date, self.fmt)
        return date

    def process_timestamp(self, timestamp, struct):
        timestamp = int(str(timestamp)[:10])
        source_time = datetime(1970, 1, 1)
        struct_time = datetime.fromtimestamp(timestamp) if timestamp >= 0 else source_time + timedelta(seconds=timestamp)
        if struct:
            return struct_time
        return struct_time.strftime(self.fmt)

    def process_cn(self, string, struct):
        if "分钟前" in string:
            num_time = cn2an(string.split("分钟")[0], "smart")
            cut_time = timedelta(minutes=-int(num_time))
        elif "小时前" in string:
            num_time = cn2an(string.split("小时")[0], "smart")
            cut_time = timedelta(hours=-int(num_time))
        elif "天前" in string:
            num_time = cn2an(string.split("天")[0], "smart")
            cut_time = timedelta(days=-int(num_time))
        else:
            raise ValueError(f"无法转换的中文时间类型：{string}")

        struct_time = datetime.today() + cut_time
        if struct:
            return struct_time
        return struct_time.strftime(self.fmt)

    def compare_date(self, time_min, time_max):
        time_min_format = time_min if isinstance(time_min, datetime) else self.format(time_min, struct=True)
        time_max_format = time_max if isinstance(time_max, datetime) else self.format(time_max, struct=True)
        if time_min_format < time_max_format:
            return True
