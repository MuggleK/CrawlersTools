# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/11/15 9:18
# @Author  : MuggleK
# @File    : content_extractor.py

import re

import numpy as np
from lxml.html import fromstring

from extractors.schemas.element import Element
from extractors.utils.preprocess import preprocess4content_extractor
from extractors.base import BaseExtractor
from extractors.utils.element import descendants_of_body
from extractors.utils.settings import ERROR_NAV_LIST 


SPECIAL_SYMBOL = [
    (re.compile(r'&quot;', re.I | re.S), '\"'),
    (re.compile(r'&amp;', re.I | re.S), '&'),
    (re.compile(r'&lt;', re.I | re.S), '<'),
    (re.compile(r'&gt;', re.I | re.S), '>'),
    (re.compile(r'&nbsp;', re.I | re.S), ' '),
    (re.compile(r'&#34;', re.I | re.S), '\"'),
    (re.compile(r'&#38;', re.I | re.S), '&'),
    (re.compile(r'&#60;', re.I | re.S), '<'),
    (re.compile(r'&#62;', re.I | re.S), '>'),
    (re.compile(r'&#160;', re.I | re.S), ' '),
]


class ContentExtractor(BaseExtractor):
    """
    extract content from detail page
    """
    
    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        # preprocess
        preprocess4content_extractor(element)

        # start to evaluate every child element
        descendants = descendants_of_body(element)

        # get std of density_of_text among all elements
        density_of_text = [descendant.density_of_text for descendant in descendants]
        density_of_text_std = np.std(density_of_text, ddof=1)

        # get density_score of every element
        for descendant in descendants:
            score = np.log(density_of_text_std) * \
                    descendant.density_of_text * \
                    np.log10(descendant.number_of_p_descendants + 2) * \
                    np.log(descendant.density_of_punctuation)
            descendant.density_score = score

        # sort element info by density_score
        descendants = sorted(descendants, key=lambda x: x.density_score, reverse=True)
        descendant_first = descendants[0] if descendants else None
        if descendant_first is None:
            return None

        paragraphs = descendant_first.xpath(".//text()")
        paragraphs = [paragraph.strip() if paragraph else '' for paragraph in paragraphs]
        paragraphs = list(filter(lambda x: x, paragraphs))
        text = '\n'.join(paragraphs)
        text = text.strip()
        return text, density_of_text_std
    
    def extract(self, html, **kwargs):
        """
        base extract method, firstly, it will convert html to WebElement, then it call
        process method that child class implements
        :param html:
        :return:
        """
        self.kwargs = kwargs
        element = fromstring(html=html)  # html有多个，fromstring默认取第一个 TODO 解析不了非规范html
        descendants_list = list(element.iterdescendants())

        # remove error navgate tags
        remove_index_list = list()
        for index, descendant in enumerate(descendants_list):
            if descendant.text is None:
                continue
            nav_error_list = [i for i in ERROR_NAV_LIST if i in descendant.text]
            if nav_error_list: remove_index_list.append(index)

        for i in remove_index_list:
            parent_element = descendants_list[i].getparent()
            if parent_element is not None: parent_element.remove(descendants_list[i])

        element.__class__ = Element
        return self.process(element)