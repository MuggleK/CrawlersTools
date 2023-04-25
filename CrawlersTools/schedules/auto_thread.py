# -*- coding: utf-8 -*-
# @Project : CrawlersTools
# @Time    : 2022/6/21 17:19
# @Author  : MuggleK
# @File    : auto_thread.py

import time
from threading import Lock, Thread, active_count
from traceback import format_exc

from loguru import logger
from tqdm import tqdm

thread_lock = Lock()


class ExcThread(Thread):
    """
    主动捕获子线程异常
    """

    def __init__(self, target, args=(), kwargs=None):
        super(ExcThread, self).__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs or dict()

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except:
            logger.error(f'self._target:{self._target} args：{self._args} kwargs：{self._kwargs}，{format_exc()}')


class AutoThread(object):
    """
    动态线程调度, 传入任务队列可为列表（初始化转换成生成器），也可为生成器
    usage:
        a_thread = AutoThread(20, fun, arg_list)
        a_thread.main_thread()

    ps: 支持两种并发方式：1.并发函数 2.并发传参 3.并发函数和传参
    """

    def __init__(self, thread_num: int, fun, arg_list=None):
        self.thread_num = thread_num
        if isinstance(fun, tuple): fun = list(fun)
        if isinstance(arg_list, tuple): arg_list = list(arg_list)
        self.fun_list = fun if callable(fun) else list(fun)     # 待带调用对象只能是方法或方法列表，元组
        self.arg_list = arg_list
        self.os_threads = active_count()

    def process_task(self):
        if callable(self.fun_list):
            # 1.并发函数
            tasks = [{'fun': self.fun_list, 'args': arg} for arg in self.arg_list]
        elif isinstance(self.fun_list, list) and not isinstance(self.arg_list, list):
            # 2.并发传参
            tasks = [{'fun': fun, 'args': self.arg_list} for fun in self.fun_list]
        else:
            assert len(self.fun_list) == len(self.arg_list), '并发函数和传参长度不一致'
            # 3.并发函数和传参
            tasks = [{'fun': fun, 'args': arg} for fun, arg in zip(self.fun_list, self.arg_list)]
        return tasks

    def wait(self):
        """
        等待所有线程结束, 比较 当前存活线程和(主线程 + tqdm线程)
        """
        while active_count() > self.os_threads + 1:
            time.sleep(.25)

    def main_thread(self):
        loop_flag = True
        tasks = self.process_task()
        with tqdm(total=len(tasks)) as pbar:
            while loop_flag:
                active_thread = active_count()
                if active_thread >= self.thread_num:
                    time.sleep(.25)
                    continue
                for _ in range(self.thread_num - active_thread + self.os_threads):
                    thread_lock.acquire()
                    task = tasks.pop() if tasks else None
                    thread_lock.release()
                    if task is None:
                        loop_flag = False
                        break
                    child_thread = ExcThread(target=task["fun"]) if task["args"] is None else ExcThread(
                        target=task["fun"], args=(task["args"],))

                    child_thread.start()
                    pbar.update(1)
