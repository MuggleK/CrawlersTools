# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:19
# @Author  : MuggleK
# @File    : auto_thread.py

import time
import random
from inspect import isgenerator
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
    动态线程调度, 传入任务队列可为列表（初始化转换成生成器），也可为生成器
    usage:
        a_thread = AutoThread(20, fun, arg_list)
        a_thread.main_thread()

    ps: 支持两种并发方式：1.并发函数 2.并发传参
    """

    def __init__(self, thread_num: int, fun, arg_list=None):
        self.thread_num = thread_num
        self.arg = arg_list  # 并发函数需要入参
        self.fun = (f for f in fun) if isinstance(fun, list) else fun
        self.args = (arg for arg in arg_list) if isinstance(arg_list, list) else arg_list
        self.flag = True if isgenerator(self.fun) else False  # True 并发函数 False并发参数
        self.os_threads = active_count()

    def wait(self):
        while active_count() > self.os_threads:
            time.sleep(.25)

    @staticmethod
    def next_task(task):
        try:
            task_arg = next(task)
        except StopIteration:
            task_arg = None

        return task_arg

    def main_thread(self):
        loop_flag = True
        while loop_flag:
            active_thread = active_count()
            if active_count() >= self.thread_num:
                time.sleep(random.uniform(0, 1))
                continue
            for _ in range(self.thread_num - active_thread + self.os_threads):
                thread_lock.acquire()
                if self.flag:
                    task_fun = self.next_task(self.fun)
                    thread_lock.release()
                    if task_fun is None:
                        loop_flag = False
                        break
                    child_thread = ExcThread(target=task_fun) if self.arg is None else ExcThread(target=task_fun, args=(
                        self.arg,))
                else:
                    task_arg = self.next_task(self.args)
                    thread_lock.release()
                    if task_arg is None:
                        loop_flag = False
                        break
                    child_thread = ExcThread(target=self.fun, args=(task_arg,))

                child_thread.start()
