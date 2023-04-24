# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 14:48
# @Author  : MuggleK
# @File    : time_process.py

import re
from datetime import datetime, timedelta

from sinan import Sinan

from CrawlersTools.projects.filters import empty_text


class TimeProcessor:

    datetime_pattern = r"([0-9]{4}).*?([0-1]{0,1}[0-9]).*?([0-3]{0,1}[0-9])"

    def __init__(self):
        self.fmt = "%Y-%m-%d"  # 暂时只处理年月日

    def format(self, string, struct=False):
        string = empty_text(string)
        try:
            return self.process_timestamp(string, struct)
        except ValueError:
            # print(f"非时间戳格式：{string}")
            pass

        date = Sinan(string).parse(display_status=False).get("datetime", [""])[0].split(' ')[0]  # 错误的时分秒
        if not date:
            re_res = re.search(self.datetime_pattern, string)
            if re_res is not None:
                date = f"{re_res.group(1)}-{re_res.group(2)}-{re_res.group(3)}"
            else:
                # 提取不出时间或者格式不满足 datetime_pattern的直接返回
                return

        if struct:
            return datetime.strptime(date, self.fmt)
        return date

    def process_timestamp(self, timestamp, struct):
        timestamp = int(str(timestamp)[:10])
        source_time = datetime(1970, 1, 1)
        struct_time = (
            datetime.fromtimestamp(timestamp) if timestamp >= 0 else source_time + timedelta(seconds=timestamp)
        )
        if struct:
            return struct_time
        return struct_time.strftime(self.fmt)

    def compare_date(self, time_min, time_max) -> bool:
        if not (time_min and time_max):
            return False

        time_min_format = time_min if isinstance(time_min, datetime) else self.format(time_min, struct=True)
        time_max_format = time_max if isinstance(time_max, datetime) else self.format(time_max, struct=True)
        if not (time_min_format and time_max_format):
            return False

        if time_min_format.date() <= time_max_format.date():
            return True
        return False
