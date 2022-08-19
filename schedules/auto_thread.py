# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:19
# @Author  : MuggleK
# @File    : auto_thread.py

import time
import random

from loguru import logger
import threading
import traceback


class ExcThread(threading.Thread):
    """
    主动捕获子线程异常
    """
    def __init__(self, target, args=(), kwargs=None):
        super(ExcThread, self).__init__()
        self.function = target
        self.args = args
        self.kwargs = kwargs if kwargs else {}
        self.exit_code = 0
        self.exception = None
        self.exc_traceback = ''

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exit_code = 1
            self.exception = e
            self.exc_traceback = traceback.format_exc()

    def _run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except Exception as e:
            logger.error(f'args：{self.args} kwargs：{self.kwargs}，{traceback.format_exc(limit=3)}')
            raise e


class AutoThread(object):
    """
    动态创建线程
    usage:
        a_thread = AutoThread(20, fun, arg_list)
        a_thread.main_thread()

    ps: 支持两种并发方式：1.并发函数 2.并发传参
    """
    def __init__(self, thread_num: int, fun, arg_list=None):
        self.thread_num = thread_num
        self.fun = fun
        self.arg_list = arg_list
        self.thread_lock = threading.Lock()
        self.loop_counter = 0

    def fun_thread(self):
        """
        并发函数，为每个函数动态创建线程
        :return:
        """
        while 1:
            active_thread = threading.active_count()
            # logger.debug(f'当前主线程循环次数：{self.loop_counter}  限制线程总数：{self.thread_num} 当前存活线程数：{active_thread}')
            if active_thread < self.thread_num:
                for _ in range(self.thread_num - active_thread):
                    self.thread_lock.acquire()
                    task_fun = self.fun.pop() if self.fun else None
                    self.thread_lock.release()
                    if task_fun:
                        t = ExcThread(target=task_fun, args=(self.arg_list,)) if self.arg_list else ExcThread(target=task_fun)  # 注意传入的参数一定是一个元组!
                        t.start()
                        if t.exit_code:
                            logger.error(t.exc_traceback)

            self.loop_counter += 1
            time.sleep(random.uniform(0, 2))
            if not self.fun:
                # logger.info("Main Thread Done")
                return

    def arg_thread(self):
        """
        并发传参，为每个参数动态创建线程
        :return:
        """
        while 1:
            active_thread = threading.active_count()
            # logger.debug(f'当前主线程循环次数：{self.loop_counter}  限制线程总数：{self.thread_num} 当前存活线程数：{active_thread}')
            if active_thread < self.thread_num:
                for _ in range(self.thread_num - active_thread):
                    self.thread_lock.acquire()
                    task_arg = self.arg_list.pop() if self.arg_list else None
                    self.thread_lock.release()
                    if task_arg:
                        t = ExcThread(target=self.fun, args=(task_arg, ))  # 注意传入的参数一定是一个元组!
                        t.start()
                        if t.exit_code:
                            logger.error(t.exc_traceback)

            self.loop_counter += 1
            time.sleep(random.uniform(0, 2))
            if not self.arg_list:
                # logger.info("Main Thread Done")
                return

    def main_thread(self):
        """

        :return:
        """
        if isinstance(self.fun, list):
            self.fun_thread()
        else:
            self.arg_thread()
