# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:08
# @Author  : MuggleK
# @File    : __init__.py

import os
from requests.base_requests import BaseRequests
from requests.proxy import get_proxies
from requests.random_ua import UserAgent

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


base_requests = BaseRequests().base_requests
