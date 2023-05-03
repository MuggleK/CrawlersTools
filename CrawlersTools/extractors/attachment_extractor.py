# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/12/21 10:54
# @Author  : MuggleK
# @File    : attachment_extractor.py

import re

from CrawlersTools.extractors.base import BaseExtractor
from CrawlersTools.extractors.schemas.element import Element
from CrawlersTools.extractors.utils.settings import ATTACHMENT_REGX


class AttachmentExtractor(BaseExtractor):
    """
    extract content from detail page
    """
    
    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        attachment_list = list()
        attachment_xpath = self.kwargs.get("attachment_xpath") or "//a"
        for attachment_element in element.xpath(attachment_xpath):
            url = [i.strip() for i in attachment_element.xpath("@href") or attachment_element.xpath("@src")]
            name = [i.strip() for i in attachment_element.xpath(".//text()")]
            if not (''.join(url).strip() and ''.join(name).strip()):
                continue
            suffix = self.filter_suffix(url[0], name[0])
            if not suffix: continue
            attachment_list.append({
                "file_url": url[0],
                "file_name": name[0]
            })
        return attachment_list

    def filter_suffix(self, url, name):
        """
        附件.xls.doc 可上传, 接口会默认取最后一个
        优先取 file_url 后缀
        """
        regx = self.kwargs.get("attachment_regx") or ATTACHMENT_REGX
        is_name_suffix = re.search(regx, name, re.I)
        is_url_suffix = re.search(regx, url, re.I)
        name_suffix = is_name_suffix.group(1) if is_name_suffix else ""
        url_suffix = is_url_suffix.group(1) if is_url_suffix else ""

        return name_suffix or url_suffix
