# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/15 11:29
# @Author  : MuggleK
# @File    : __init__.py

from CrawlersTools.extractors.attachment_extractor import AttachmentExtractor
from CrawlersTools.extractors.content_extractor import ContentExtractor
from CrawlersTools.extractors.list_extractor import ListExtractor
from CrawlersTools.extractors.time_extractor import TimeExtractor
from CrawlersTools.extractors.title_extractor import TitleExtractor


class PolicyExtractor(object):

    @staticmethod
    def extract(
            html,
            title_xpath: str = "",
            publish_time_xpath: str = "",
            content_xpath: str = "",
            attachment_xpath: str = "",
            attachment_regx: str = ""
    ) -> dict:
        title = TitleExtractor().extract(html, title_xpath=title_xpath)
        publish_time = TimeExtractor().extract(html, publish_time_xpath=publish_time_xpath)
        content, content_with_tag, images = ContentExtractor().extract(html, content_xpath=content_xpath)
        attachments = AttachmentExtractor().extract(html, attachment_xpath=attachment_xpath, attachment_regx=attachment_regx)

        return {
            "title": title,
            "publish_time": publish_time,
            "content": content,
            "content_with_tag": content_with_tag,
            "images": images,
            "attachment": attachments
        }
