#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 15:32
# @Author  : xc
# @File    : kafka_operate
# @Software: PyCharm


import json
from kafka import KafkaProducer
from loguru import logger


class KProducer:
    def __init__(self, bootstrap_servers, topic):
        """
        kafka 生产者
        :param bootstrap_servers: 地址
        :param topic:  topic
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda m: json.dumps(m).encode('ascii'), )  # json 格式化发送的内容
        self.topic = topic

    def sync_producer(self, data_li: list):
        """
        同步发送 数据
        :param data_li:  发送数据
        :return:
        """
        for data in data_li:
            future = self.producer.send(self.topic, data)
            record_metadata = future.get(timeout=10)  # 同步确认消费
            partition = record_metadata.partition  # 数据所在的分区
            offset = record_metadata.offset  # 数据所在分区的位置
            logger.success('save success, partition: {}, offset: {}'.format(partition, offset))
