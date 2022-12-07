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
from extractors.utils.settings import (
    SPECIAL_SYMBOL_MAP,
    ERROR_NAV_LIST,
    suffix_key,
    file_key_word,
)


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
            score = (
                np.log(density_of_text_std)
                * descendant.density_of_text
                * np.log10(descendant.number_of_p_descendants + 2)
                * np.log(descendant.density_of_punctuation)
            )
            descendant.density_score = score

        # sort element info by density_score
        descendants = sorted(descendants, key=lambda x: x.density_score, reverse=True)
        descendant_first = descendants[0] if descendants else None
        if descendant_first is None:
            return None
        # 默认从正文取,取不到全局扫一遍
        attachments = self.extract_attach(descendant_first)
        if not attachments:
            attachments = self.extract_attach(element)
        content_html = descendant_first.string
        paragraphs = descendant_first.xpath(".//text()")
        paragraphs = [
            paragraph.strip() if paragraph else "" for paragraph in paragraphs
        ]
        paragraphs = list(filter(lambda x: x, paragraphs))
        text = "\n".join(paragraphs)
        text = text.strip()
        return text, attachments, content_html

    def extract(self, html, **kwargs):
        """
        base extract method, firstly, it will convert html to WebElement, then it call
        process method that child class implements
        :param html:
        :return:
        """
        self.kwargs = kwargs
        for key, value in SPECIAL_SYMBOL_MAP.items():
            html = html.replace(key, value)

        element = fromstring(html=html)  # html有多个，fromstring默认取第一个 TODO 解析不了非规范html
        if self.kwargs.get("content_xpath"):
            return "".join(element.xpath(self.kwargs.get("content_xpath")))

        descendants_list = list(element.iterdescendants())

        # remove error navigate tags
        remove_index_list = list()
        for index, descendant in enumerate(descendants_list):
            if descendant.text is None:
                continue
            nav_error_list = [i for i in ERROR_NAV_LIST if i in descendant.text]
            if nav_error_list:
                remove_index_list.append(index)

        for i in remove_index_list:
            parent_element = descendants_list[i].getparent()
            if parent_element is not None:
                parent_element.remove(descendants_list[i])

        element.__class__ = Element
        return self.process(element)

    def extract_attach(self, element: Element, base_url=""):
        a_list = element.a_descendants
        img_list = element.img_descendants
        all_links = []
        cache_links = []
        for a in a_list:
            link = a.attrib.get("href", "")
            name = a.text or a.xpath("//text")

            if link in cache_links or "javascript" in link:
                continue
            if not re.search(suffix_key, link, re.I):
                continue
            if not name:
                name = link.split("/")[-1]
            cache_links.append(link)
            all_links.append({"file_name": name, "file_url": link})
            # 兼容那些没有后缀的链接
            for key in file_key_word:
                if key in link:
                    if link in cache_links:
                        continue
                    cache_links.append(link)
                    all_links.append({"file_name": name, "file_url": link})
                    break

        for img in img_list:
            src = img.attrib.get("src", "")
            name = img.text or img.attrib.get("alt", "") or img.xpath("//text")
            if src in cache_links or "javascript" in src:
                continue
            if not re.search(suffix_key, src, re.I):
                continue
            if not name:
                name = src.split("/")[-1]
            cache_links.append(src)
            all_links.append({"file_name": name, "file_url": src})
            # 兼容那些没有后缀的图片
            for key in file_key_word:
                if key in src:
                    if src in cache_links:
                        continue
                    cache_links.append(src)
                    all_links.append({"file_name": name, "file_url": src})
                    break
        return all_links
