# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 9:12
# @Author  : MuggleK
# @File    : mongo_pipeline.py

from pymongo import MongoClient


class MongoPipeline:
    """
    A Mongo Pipeline to Create or Insert or Update or Delete Collection

    Usage:

    ```python
    >>> mongo_client = MongoPipeline()
    >>> record = mongo_client.find_one("test_collection", '{"company_name": "qzd"}')
    ```
    """

    collection = None
    conn = None

    def __init__(self, host="127.0.0.1", port="27017", username="root", password="root", database="crawl_data"):

        self.server = '''mongodb://%s:%s@%s:%s/%s''' % (username, password, host, port, database)
        self.client = MongoClient(host=self.server, readPreference="secondaryPreferred")
        self.db = self.client.get_database(database)

    def close(self):
        return self.client.close()

    def set_collection(self, name):
        self.collection = self.db.get_collection(name)

    def find(self, collection_name, query=None, ref_query=None):
        """
        from query phrase to find docs

        :param collection_name:
        :param query: query phrase
        :param ref_query: reserve phrase
        :return:
        """
        records = self.db.get_collection(collection_name).find(query, ref_query)
        return records

    def find_one(self, collection_name, query=None, ref_query=None):
        records = self.db.get_collection(collection_name).find_one(query, ref_query)
        return records

    def update(self, collection_name, query, update, many=False):
        if many:
            self.db.get_collection(collection_name).update_many(query, update, upsert=True)
            return
        self.db.get_collection(collection_name).update_one(query, update, upsert=True)

    def aggregate(self, collection_name, query):
        records = self.db.get_collection(collection_name).aggregate(query)
        for record in records:
            yield record
