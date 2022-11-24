# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/15 11:29
# @Author  : MuggleK
# @File    : __init__.py

from extractors.list_extractor import ListExtractor

from extractors.title_extractor import TitleExtractor
from extractors.time_extractor import TimeExtractor
from extractors.content_extractor import ContentExtractor


class PolicyExtractor(object):

    @staticmethod
    def extract(html, title_xpath: str = "", publish_time_xpath: str = "", content_xpath: str = "") -> dict:
        title = TitleExtractor().extract(html, title_xpath=title_xpath)
        publish_time = TimeExtractor().extract(html, publish_time_xpath=publish_time_xpath)
        content = ContentExtractor().extract(html, content_xpath=content_xpath)

        return {
            "title": title,
            "publish_time": publish_time,
            "content": content,
        }
