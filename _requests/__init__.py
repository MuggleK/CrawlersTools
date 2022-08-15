# -*- coding: utf-8 -*-
# @Project : qzd_crawler_tools
# @Time    : 2022/6/21 17:08
# @Author  : Changchuan.Pei
# @File    : base_requests.py

import os
from CrawlersTools._requests.base_requests import BaseRequests

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


base_requests = BaseRequests().base_requests
