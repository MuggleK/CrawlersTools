# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:08
# @Author  : MuggleK
# @File    : logs.py

import time

from loguru import logger

time_format = time.strftime("%Y_%m_%d")
log_format = "{time:YYYY-MM-DD HH:mm:ss}|{level}| {name}:{function}:{line}| {message}"


class Logging(object):
    """
    Usage::

        # >>>
        # >>> logger = Logging('logs')
        # >>> logger.info('Logging Example')
        # 2022-01-20 17:27:32.194 | INFO     | __main__:info:149 - Logging Example
        # >>>
    """

    __instance = None

    def __new__(cls, log_path, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logging, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self, log_path, expire_date="10 days"):
        logger.add(f"{log_path}/log_{time_format}_info.log", encoding="utf-8", enqueue=True, retention="1 months", level="INFO", format=log_format)
        logger.add(f"{log_path}/log_{time_format}_error.log", encoding="utf-8", enqueue=True, retention=expire_date, level="ERROR", format=log_format)
        logger.add(f"{log_path}/log_{time_format}_debug.log", encoding="utf-8", enqueue=True, retention=expire_date, level="DEBUG", format=log_format)
        logger.add(f"{log_path}/log_{time_format}_waring.log", encoding="utf-8", enqueue=True, retention=expire_date, level="WARNING", format=log_format)

    @staticmethod
    def info(msg):
        return logger.info(msg)

    @staticmethod
    def debug(msg):
        return logger.debug(msg)

    @staticmethod
    def warning(msg):
        return logger.warning(msg)

    @staticmethod
    def error(msg):
        return logger.error(msg)

    @staticmethod
    def success(msg):
        return logger.success(msg)
