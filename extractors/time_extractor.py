# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/11/3 9:55
# @Author  : MuggleK
# @File    : time_extractor.py

import re

from lxml.html import HtmlElement

from extractors.utils.settings import DATETIME_PATTERN, PUBLISH_TIME_META
from preprocess import format_time


class TimeExtractor:
    def __init__(self):
        self.time_pattern = DATETIME_PATTERN

    def extractor(self, element: HtmlElement, publish_time_xpath: str = '') -> tuple:
        publish_time = (self.extract_from_user_xpath(publish_time_xpath, element)  # 用户指定的 Xpath 是第一优先级
                        or self.extract_from_meta(element)   # 第二优先级从 Meta 中提取
                        or self.extract_from_text(element))  # 最坏的情况从正文中提取

        return format_time(publish_time)

    @staticmethod
    def extract_from_user_xpath(publish_time_xpath: str, element: HtmlElement) -> str:
        if publish_time_xpath:
            publish_time = ''.join(element.xpath(publish_time_xpath))
            return publish_time
        return ''

    def extract_from_text(self, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return ''

    @staticmethod
    def extract_from_meta(element: HtmlElement) -> str:
        """
        优先匹配 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return ''

