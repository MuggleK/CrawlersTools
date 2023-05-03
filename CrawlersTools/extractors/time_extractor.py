# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/11/3 9:55
# @Author  : MuggleK
# @File    : time_extractor.py

import re

from lxml.html import etree

from CrawlersTools.extractors.base import BaseExtractor
from CrawlersTools.extractors.schemas.element import Element
from CrawlersTools.extractors.utils.settings import DATETIME_PATTERN, PUBLISH_TIME_META, TITLE_EXTRACTOR_USELESS_TAGS
from CrawlersTools.preprocess import TimeProcessor

format_time = TimeProcessor().format


class TimeExtractor(BaseExtractor):

    @staticmethod
    def extract_from_xpath(element: Element, publish_time_xpath: str) -> str:
        if publish_time_xpath:
            publish_time = ''.join(element.xpath(publish_time_xpath))
            return format_time(publish_time)
        return ''

    @staticmethod
    def extract_from_text(element: Element) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in DATETIME_PATTERN:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return format_time(dt_obj.group(1))
        else:
            return ''

    @staticmethod
    def extract_from_meta(element: Element) -> str:
        """
        优先匹配 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return format_time(''.join(publish_time))
        return ''
    
    def process(self, element: Element):
        # remove tag and its content
        etree.strip_elements(element, *TITLE_EXTRACTOR_USELESS_TAGS)

        publish_time = (self.extract_from_xpath(element, publish_time_xpath=self.kwargs.get("publish_time_xpath"))
                        or self.extract_from_meta(element)
                        or self.extract_from_text(element))

        return publish_time
