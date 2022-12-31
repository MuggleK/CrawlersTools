# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:06
# @Author  : MuggleK
# @File    : proxy.py

import httpx

from loguru import logger


def get_proxies(proxy_url=None, http2=False):
    """
    默认httpx代理模式
    @param proxy_url: 代理请求链接
    @param http2: 默认http1.1规则
    @return:
    """
    if not proxy_url: return

    protocol = 'http://'
    try:
        proxy = httpx.get(proxy_url).text.strip()
        proxy = protocol + proxy
        if http2:
            return {protocol: proxy, 'https://': proxy}
        return {"http": proxy, "https": proxy}
    except Exception as err:
        logger.error(f'获取代理失败：{err}')
