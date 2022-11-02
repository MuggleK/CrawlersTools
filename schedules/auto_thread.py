# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:19
# @Author  : MuggleK
# @File    : auto_thread.py

import time
import random

from threading import Thread, active_count, Lock
from traceback import format_exc

from loguru import logger

thread_lock = Lock()


class ExcThread(Thread):
    """
    主动捕获子线程异常
    """
    def __init__(self, target, args=(), kwargs=None):
        super(ExcThread, self).__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs if kwargs else {}

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except:
            logger.error(f'args：{self._args} kwargs：{self._kwargs}，{format_exc()}')


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
        self.os_threads = active_count()

    def task_status(self):
        return self.fun if isinstance(self.fun, list) else self.arg_list

    def wait(self):
        while active_count() > self.os_threads:
            time.sleep(.25)

    def main_thread(self):
        while self.task_status():
            active_thread = active_count()
            if active_count() >= self.thread_num:
                time.sleep(random.uniform(0, 1))
                continue
            for _ in range(self.thread_num - active_thread + self.os_threads):
                thread_lock.acquire()
                if isinstance(self.fun, list):
                    task_fun = self.fun.pop() if self.fun else None
                    thread_lock.release()
                    if not task_fun:
                        break
                    child_thread = ExcThread(target=task_fun, args=(self.arg_list,)) if self.arg_list else ExcThread(
                        target=task_fun)  # 注意传入的参数一定是一个元组!
                else:
                    task_arg = self.arg_list.pop() if self.arg_list else None
                    thread_lock.release()
                    if not (task_arg or task_arg == 0):
                        break
                    child_thread = ExcThread(target=self.fun, args=(task_arg,))  # 注意传入的参数一定是一个元组!

                child_thread.start()
