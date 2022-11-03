# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/19 20:23
# @Author  : MuggleK
# @File    : title_extractor.py

import re
from itertools import combinations

from lxml.html import HtmlElement

from extractors.util.utils import get_longest_common_sub_string
from extractors.util.settings import TITLE_HTAG_XPATH, TITLE_META_XPATH, TITLE_META_XPATH_BAK


class TitleExtractor:

    @staticmethod
    def extract_by_xpath(element, title_xpath):
        if title_xpath:
            title_list = element.xpath(title_xpath)
            if title_list:
                return title_list[0]
        return ''

    @staticmethod
    def extract_by_title(element):
        title_list = element.xpath(TITLE_META_XPATH) or element.xpath(TITLE_META_XPATH_BAK)
        if title_list:
            return max(title_list, key=len)
        else:
            return ''

    @staticmethod
    def extract_by_htag(element):
        title_list = element.xpath(TITLE_HTAG_XPATH)
        if not title_list:
            return ''
        index_string = [(index, ''.join(filter(str.isalnum, string))) for index, string in enumerate(title_list)]
        string_list = [i[1] for i in index_string]
        max_string = max(string_list, key=len)
        return title_list[string_list.index(max_string)]

    @staticmethod
    def extract_common_str(element: HtmlElement) -> str:
        h_tag_texts_list = element.xpath(TITLE_HTAG_XPATH)
        new_title_list = list(combinations(h_tag_texts_list, 2))
        if len(new_title_list) == 1:
            new_title = str(max(list(new_title_list[0]), key=len))
            return new_title

        common_title_list = [get_longest_common_sub_string(i[0], i[1]).strip() for i in new_title_list]
        if common_title_list:
            new_title = max(common_title_list, key=len)
            sub_string = re.sub(r'\d+', '', ''.join(filter(str.isalnum, new_title)))
            return new_title if len(new_title) > 4 and sub_string else ''
        return ''

    def extract(self, element: HtmlElement, title_xpath: str = '') -> str:
        title = (self.extract_by_xpath(element, title_xpath)
                 or self.extract_by_title(element)
                 or self.extract_common_str(element)
                 or self.extract_by_htag(element)
                 )
        return title.strip()
