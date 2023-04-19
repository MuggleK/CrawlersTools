# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 9:12
# @Author  : MuggleK
# @File    : redis_pipeline.py

import redis


class RedisPipeline(object):
    def __init__(self, name, namespace, **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get_wait(self, timeout=None):
        item = self.__db.blpop(self.key, timeout=timeout)
        return item

    def get_nowait(self):
        item = self.__db.lpop(self.key)
        return item
