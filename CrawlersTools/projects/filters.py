# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 14:48
# @Author  : MuggleK
# @File    : filters.py

import re
from functools import reduce
from urllib.parse import urlparse

from loguru import logger


def empty_text(lis):
    word = ""
    for i in lis:
        word += i.strip()
    return word


def filter_title(title: str, remove_list: list):
    """

    :param title: 文章标题
    :param remove_list: 过滤关键词列表
    :return:
    """
    if not title:
        return False
    for r in remove_list:
        and_lists = r.split("and")
        if len(and_lists) == 1:
            if and_lists[0] in title:
                logger.debug(f"过滤标题: {title}  过滤词: {r}")
                return True
        else:
            total = [1 for a in and_lists if a in title]
            result = reduce(lambda x, y: x + y, total)
            if len(and_lists) != result:
                continue
            return True


def filter_text(text, removes: list):
    """
    :param text: 正文字段
    :param removes: 需要去掉的特殊字段：扫一扫，【关闭】，【打印】
    :return:
    """
    if removes:
        for remove in removes:
            text = text.replace(remove, '')
    return text


def filter_allowed_url(url, main_url, other_domains):
    other_domains = other_domains if other_domains else []
    main_url = main_url[0] if isinstance(main_url, list) else main_url
    allowed_domains = [urlparse(main_url).netloc] + other_domains if urlparse(main_url).netloc else other_domains + [main_url]
    for domain in allowed_domains:
        if (not domain) or re.search(domain, url):
            return True
