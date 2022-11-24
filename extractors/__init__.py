# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/15 11:29
# @Author  : MuggleK
# @File    : __init__.py

from extractors.title_extractor import TitleExtractor
from extractors.time_extractor import TimeExtractor
from extractors.content_extractor import ContentExtractor


class PolicyExtractor(object):

    def __init__(self, title_xpath: str = "", publish_time_xpath: str = "", content_xpath: str = ""):
        self.title_xpath = title_xpath
        self.publish_time_xpath = publish_time_xpath
        self.content_xpath = content_xpath

    def extract(self, html) -> dict:
        title = TitleExtractor().extract(html, title_xpath=self.title_xpath)
        publish_time = TimeExtractor().extract(html, publish_time_xpath=self.publish_time_xpath)
        content = ContentExtractor().extract(html, content_xpath=self.content_xpath)

        return {
            "title": title,
            "publish_time": publish_time,
            "content": content,
        }
