# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:08
# @Author  : MuggleK
# @File    : base_requests.py

import json
import random
import re
import time

from chardet import detect
from httpx import Client, Response
from loguru import logger

from CrawlersTools.requests.proxy import get_proxies
from CrawlersTools.requests.random_ua import UserAgent


class BaseRequests(object):
    """
    A Rquests Class base on httpx

    Usage:

    ```python
    >>> base_requests = BaseRequests().base_requests
    >>> response = base_requests('https://example.org')
    ```
    """

    def base_requests(
        self,
        url: str,
        session: object = None,
        headers=UserAgent(),
        method: str = "get",
        proxies: dict = None,
        proxy_url: str = None,
        http2: bool = False,
        encoding: str = None,
        retry: int = 3,
        **kwargs
    ) -> Response:
        """
        内置ali_waf & 加速乐解密

        :param url: 请求链接
        :param session: 维持session可从外部传入
        :param headers: 请求头
        :param method:  具体请求方式
        :param proxies: ip代理，配合proxy_url可失效自动切换
        :param proxy_url:  获取代理链接
        :param http2:   是否使用http2.0协议
        :param retry:   请求重试次数，默认3次
        :param encoding:   指定编码，默认detect解析，效果同requests的apparent_encoding
        :param kwargs:  请求时需携带的其他参数
        :return: Response
        :exception: 1.代理失效&超过重试次数返回None 2.waf或加速乐解密失败返回None
        """
        for _ in range(retry):
            try:
                proxies = proxies if proxies else get_proxies(proxy_url, http2=True)
                session = session or Client(
                    http2=http2,
                    headers=headers,
                    proxies=proxies,
                    timeout=kwargs.get("timeout", 20),
                    verify=kwargs.get("verify", True),
                    follow_redirects=kwargs.get("allow_redirects", False)
                )
                response = session.request(
                    method=method.lower(),
                    url=url,
                    headers=headers,
                    content=kwargs.get("content"),
                    data=kwargs.get("data"),
                    files=kwargs.get("files"),
                    json=kwargs.get("json"),
                    params=kwargs.get("params"),
                    timeout=kwargs.get("timeout", 20),
                    follow_redirects=kwargs.get("allow_redirects", False)
                )
                response.encoding = encoding if encoding else detect(response.content)['encoding']  # chardet 更准确
                if 200 <= response.status_code < 300 or response.status_code == 412:
                    if 'arg1=' in response.text:
                        acw_tc_cookie = f'acw_tc={session.cookies.get("acw_tc")};'
                        headers["Cookie"] = headers["Cookie"] + acw_tc_cookie if headers.get("Cookie") else acw_tc_cookie
                        reg_arg1 = re.findall("var arg1='(.*)';", response.text)[0]
                        arg2 = self.ali_waf(reg_arg1)
                        headers['cookie'] += f'acw_sc__v2={arg2}'
                        continue
                    return response
                elif response.status_code == 521:
                    if 'document.cookie' in response.text:
                        cookie_key = [key for key in list(session.cookies.keys()) if key.startswith("__jsluid")][0]
                        headers["Cookie"] = headers["Cookie"] if headers.get("Cookie") else f'{cookie_key}={session.cookies.get(cookie_key)};'
                        headers["Cookie"] += f'{self.process_fuck_js(response.text)};'
                        continue
                    elif 'chars' in response.text:
                        __jsl_clearance_s = self.process_clearance(response.text)
                        headers["Cookie"] = '='.join(headers["Cookie"].split('=')[:-1]) + f'={__jsl_clearance_s};'
                        continue
                else:
                    proxies = None
                    time.sleep(random.uniform(0, 1))
                    continue
            except Exception as err:
                logger.error(f'url：{url} error：{err} proxies：{proxies}')
                proxies = None
                time.sleep(random.uniform(0, 1))
                continue

    @staticmethod
    def ali_waf(arg1):
        """
        acw_sc__v2算法
        :param arg1:
        :return:
        """
        list1 = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32,
                 26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
        dict1 = {}
        for i in range(len(arg1)):
            string = arg1[i]
            for j in range(len(list1)):
                if list1[j] == i + 1:
                    dict1[j] = string
        str1 = ''.join([dict1.get(i) for i in range(40)])

        str1_list = list(str1)
        str2 = "3000176000856006061501533003690027800375"
        str2_list = list(str2)
        str4 = ''
        for m in range(0, len(str1_list), 2):
            int1 = int(''.join(str1_list[m:m + 2]), 16)
            int2 = int(''.join(str2_list[m:m + 2]), 16)
            str3 = str(hex(int1 ^ int2))[2:]
            if len(str3) == 1:
                str3 = '0' + str3
            str4 += str3
        return str4

    @staticmethod
    def process_fuck_js(js_text):
        import execjs

        js_text = js_text.split(';location.href=loc')[0].split('document.cookie=')[-1]
        r = execjs.eval(js_text).split(';')[0]
        return r

    @staticmethod
    def process_clearance(html):
        import hashlib

        data = json.loads(re.findall(r'go\((.*?)\)', html)[1])
        chars_length = len(data.get('chars'))
        for i in range(chars_length):
            for j in range(chars_length):
                result = data.get('bts')[0] + data.get('chars')[i] + data.get('chars')[j] + data.get('bts')[1]
                b = eval('hashlib.{}()'.format(data.get('ha')))
                b.update(result.encode(encoding='utf-8'))
                res = b.hexdigest()
                if res == data.get('ct'):
                    return result
