# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:19
# @Author  : MuggleK
# @File    : auto_thread.py

import time
from inspect import isgenerator
from threading import Thread, active_count, Lock
from traceback import format_exc

import vthread as vthread
from loguru import logger


thread_lock = Lock()


class ExcThread(Thread):
    """
    主动捕获子线程异常
    """

    def __init__(self, target, args=None, kwargs=None):
        super(ExcThread, self).__init__()
        self._target = target
        self._args = tuple() if args is None else (args, )
        self._kwargs = kwargs or dict()

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except:
            logger.error(f'target：{self._target} args：{self._args} kwargs：{self._kwargs}，{format_exc()}')


class AutoThread(object):
    """
    动态线程调度, 传入任务队列可为列表（初始化转换成生成器），也可为生成器
    usage:
        a_thread = AutoThread(20, fun, arg_list)
        a_thread.main_thread()

    ps: 支持三种并发方式：1.并发函数 2.并发传参 3.函数和参数按顺序组合
    """

    def __init__(self, thread_num: int, fun, arg_list=None):
        self.thread_num = thread_num
        self.fun = (f for f in fun) if isinstance(fun, list) else fun
        self.args = (a for a in arg_list) if isinstance(arg_list, list) else arg_list
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
        while True:
            with thread_lock:
                active_thread = active_count()
                if active_thread >= self.thread_num:
                    time.sleep(.5)
                    continue

            fun = self.next_task(self.fun) if isgenerator(self.fun) else self.fun
            if fun is None:
                break
            args = self.next_task(self.args) if isgenerator(self.args) else self.args
            if args is None:
                break

            t = ExcThread(target=fun, args=args)
            t.start()
