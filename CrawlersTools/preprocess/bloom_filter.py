# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 14:35
# @Author  : MuggleK
# @File    : bloom_filter.py

import hashlib


def sha1(data):
    """
    BloomFilter fingerprint Function
    """
    hash_object = hashlib.sha1(data.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


class SimpleHash(object):
    """
    BloomFilter Hash Function
    """
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    """
    Usage::

      # >>> bf = BloomFilter(server, key, block_num=1)  # you can increase block_num if you are filtering too many urls
      # ... if is_contains(fp):
      # ...     print(f"{fp} 已存在")
      # ... else:
      # ...     bf.insert(fp)
      # >>>

    """
    def __init__(self, server, key, block_num=1, filter_level=0):
        """

        :param server: Redis Server
        :param key: Redis Key
        :param block_num:
        :param filter_level: Filter data Magnitude 0：total data less than 100W. 1: Exceed 100W
        """
        self.bit_size = 1 << 31 if filter_level else 1 << 29
        self.seeds = [5, 7, 11, 13, 31] if filter_level else [5, 7, 11, 13, 31, 37, 61]
        self.server = server
        self.key = key
        self.block_num = block_num
        self.hash_func = []
        for seed in self.seeds:
            self.hash_func.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, str_input) -> bool:
        """
        param str_input: source string
        :return:
        """
        if not str_input:
            return False
        ret = True

        fp = sha1(str_input)
        name = f"{self.key}{str(int(fp[0:2], 16) % self.block_num)}"
        for f in self.hash_func:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return bool(ret)

    def insert(self, str_input):
        """
        param str_input: source string
        :return:
        """
        fp = sha1(str_input)
        name = f"{self.key}{str(int(fp[0:2], 16) % self.block_num)}"
        for f in self.hash_func:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)
