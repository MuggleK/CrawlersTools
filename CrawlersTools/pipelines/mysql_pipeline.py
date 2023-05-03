# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/8/12 9:12
# @Author  : MuggleK
# @File    : mysql_pipeline.py

import time

import pymysql
from DBUtils.PooledDB import PooledDB
from loguru import logger


class MysqlPipeline(object):
    """
    A Mysql Pipeline to Create or Insert or Update or Delete Table

    Usage::

        # >>>
        # >>> mysql_pool = MysqlPipeline(host='127.0.0.1', username='root', password='mysql', db='test', pool_db=True)
        # >>> mysql_pool.insert_one(item, 'test_table')
        # >>>

    """
    def __init__(self, host='127.0.0.1', username='root', password='', db='test', port=3306, drop_column=None, pool_num=10):
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
        self.drop_column = drop_column if drop_column else ['id', 'crawl_time']
        self.pool_num = pool_num
        self.sql_pool = PooledDB(pymysql, self.pool_num, host=self.host, user=self.username, passwd=self.password,
                                 db=self.db, port=self.port, charset='utf8', use_unicode=True)
        self.conn = self.sql_pool.connection()
        self.cursor = self.conn.cursor()

        self.table_name_list = self.get_db_name()

    def get_db_name(self):
        sql = "select table_name from information_schema.tables where table_schema='{}'".format(self.db)
        self.cursor.execute(sql)
        db_list = self.cursor.fetchall()
        db_list = [i[0] for i in db_list]
        return db_list

    def get_columns(self, cursor):
        item = {}
        for table_name in self.table_name_list:
            sql = "select column_name from information_schema.columns where table_name=%r and table_schema=%r" % (table_name, self.db)
            cursor.execute(sql)
            column_list = cursor.fetchall()
            column_list = [i[0] for i in column_list]
            insert_columns = [i for i in column_list if i not in self.drop_column]
            item[table_name] = insert_columns
        return item

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
                logger.debug("Mysql Lost Connection for Host : {} Retrying, Error: {}".format(self.host, e))
                try:
                    self.sql_pool = PooledDB(pymysql, self.pool_num, host=self.host, user=self.username,
                                             passwd=self.password,
                                             db=self.db,
                                             port=self.port,
                                             charset='utf8', use_unicode=True)
                    sql_conn = self.sql_pool.connection()
                    cursor = sql_conn.cursor()
                    return sql_conn, cursor
                except Exception as err:
                    logger.debug("Waiting for 5s to Connect, Error: {}".format(err))
                    time.sleep(5)
                    continue

        logger.error("Mysql Connects for Host : {} Over Max Retries".format(self.host))
        return None, None

    def execute_sql(self, sql, mode='fetch'):
        sql_conn, cursor = self.ping()
        if not (sql_conn and cursor):
            logger.warning(f"Mysql Connection occur Error，sql：{sql}")
            return
        if mode == 'fetch':
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            sql_conn.close()
            return result
        else:
            cursor.execute(sql)
        sql_conn.commit()
        cursor.close()
        sql_conn.close()

    def insert(self, item, table_name):
        """
        Mysql Auto Insert data

        :param item:
        :param table_name:
        :return:
        """
        if not item:
            logger.error("item is Empty")
            return

        sql_conn, cursor = self.ping()
        if not (sql_conn and cursor):
            logger.warning(f"Mysql Connection occur Error，Item：{item}")
            return

        insert_tables_key = self.get_columns(cursor)
        item_key = insert_tables_key.get(table_name)
        if not item_key:
            raise ValueError("table_name: {} does not exist".format(table_name))

        format_str = ','.join(["%s" for _, ind in enumerate(item_key)])
        insert = 'INSERT IGNORE INTO %s (%s) VALUES (%s)' % (table_name, ','.join(item_key), format_str)

        if isinstance(item, dict):
            # 插入单条数据
            item_values = [item.get(i) for i in item_key]
            data_one = f"({','.join([pymysql.escape_string('%r') % str(i) for i in item_values])})"
            data_list = []
            for i in eval(data_one):
                if i == 'None':
                    i = None
                data_list.append(i)
            execute_data = tuple(data_list)

            cursor.execute(insert, execute_data)
            sql_conn.commit()
        elif isinstance(item, list):
            # 批量插入
            item_values = tuple([tuple([i.get(key) for key in item_key]) for i in item])
            cursor.executemany(insert, item_values)
        else:
            raise ValueError(f"Unknown Type for Item：{item}")

        logger.success(f"Success: Insert {item} -> {table_name}")

        cursor.close()
        sql_conn.close()
