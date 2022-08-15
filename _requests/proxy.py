# -*- coding: utf-8 -*-
# @Project : qzd_crawler_tools
# @Time    : 2022/6/21 17:06
# @Author  : Changchuan.Pei
# @File    : proxy.py

import requests

from loguru import logger


def get_proxies(proxy_type="random"):
    """
    qzd_proxy：亿牛云+星速云
    @param proxy_type: 默认取随机
    @return:
    """
    try:
        protocol = 'http://'
        proxy = requests.get(f"http://192.168.9.3:5555/{proxy_type.lower()}").text.strip()
        proxy = protocol + proxy
        return {protocol: proxy, 'https://': proxy}
    except Exception as err:
        logger.error(f'获取代理失败：{err}')
