# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 9:12
# @Author  : MuggleK
# @File    : mysql_pipeline.py

import time
from typing import Tuple, Optional

import pymysql
from DBUtils.PooledDB import PooledDB
from loguru import logger
from pymysql import ProgrammingError
from pymysql.converters import escape_string


def cursor_handler(func):
    def wrapper(self, *args, **kwargs):
        sql_conn, cursor = self.ping()
        if not (sql_conn and cursor):
            logger.warning(f"Mysql Connection occur Error，args：{args}, kwargs: {kwargs}")
            return

        try:
            kwargs.update({'cursor': cursor})
            result = func(self, *args, **kwargs)
            sql_conn.commit()
            return result
        finally:
            cursor.close()
            sql_conn.close()

    return wrapper


class MysqlPipeline(object):
    """
    A Mysql Pipeline to Create or Insert or Update or Delete Table

    Usage::

        # >>>
        # >>> mysql_pool = MysqlPipeline(host='127.0.0.1', username='root', password='mysql', db='test')
        # >>> mysql_pool.insert(item, 'test_table')
        # >>>

    """

    table_columns_map = dict()  # 缓存每个table的结构，避免每次都要查询数据库

    def __init__(self, host: str = '127.0.0.1', username: str = 'root',
                 password: str = '', db: str = 'test', port: int = 3306,
                 drop_column: Optional[Tuple] = ('id', 'crawl_time'),
                 pool_num: int = 10
                 ):
        """
        :param host:
        :param username:
        :param password:
        :param db:
        :param port:
        :param drop_column: type:list 插入数据中不需要手动添加的字段,例如自增主键id,自增时间戳等
        :param pool_num:
        """
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.port = port
        self.drop_column = drop_column
        self.pool_num = pool_num

        self.sql_pool = PooledDB(
            pymysql, self.pool_num, host=self.host,
            user=self.username, passwd=self.password, db=self.db,
            port=self.port, charset='utf8', use_unicode=True
        )

    def ping(self):
        """
        重写pymysql中的ping函数并新增重试机制,以保持conn和cursor

        :return:
        """
        for _ in range(5):
            try:
                sql_conn = self.sql_pool.connection()
                cursor = sql_conn.cursor()
                return sql_conn, cursor
            except Exception as e:
                logger.debug(f"Mysql Lost Connection for Host : {self.host} Retrying, Error: {e}")

            try:
                self.sql_pool = PooledDB(
                    pymysql, self.pool_num, host=self.host, user=self.username,
                    passwd=self.password, db=self.db, port=self.port,
                    charset='utf8', use_unicode=True
                )
                sql_conn = self.sql_pool.connection()
                cursor = sql_conn.cursor()
                return sql_conn, cursor
            except Exception as err:
                logger.debug(f"Waiting for 5s to Connect, Error: {err}")
                time.sleep(5)
                continue

        logger.error(f"Mysql Connects for Host : {self.host} Over Max Retries")
        return None, None

    def add_columns_map(self, table_name):
        sql = f"select column_name from information_schema.columns " \
              f"where table_name='{table_name}' and table_schema='{self.db}'"
        column_list = self.execute_sql(sql)
        columns = [i[0] for i in column_list if i[0] not in self.drop_column]
        self.table_columns_map[table_name] = columns
        return columns

    @cursor_handler
    def execute_sql(self, sql, mode='fetch', cursor=None):
        if mode == 'fetch':
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        cursor.execute(sql)

    def insert(self, item, table_name):

        if not item:
            logger.error("item is Empty")
            return

        table_columns = self.table_columns_map.get(table_name) or self.add_columns_map(table_name)
        if not table_columns:
            raise ProgrammingError(f"Table '{self.db}.{table_name}' doesn't exist")

        # 格式化sql语句 处理"None" -> NULL
        format_str = ','.join(["%s" for _ in table_columns])
        insert_sql = 'INSERT IGNORE INTO %s (%s) VALUES (%s)' % (table_name, ','.join(table_columns), format_str)
        item_values = [None if item.get(key) == "None" else item.get(key) for key in table_columns]
        execute_data = tuple([escape_string('%r') % str(i) if i else "NULL" for i in item_values])

        self.execute_sql(insert_sql % execute_data)
        logger.info(f"Insert Ignore Successfully：{table_name} -> {item}")
