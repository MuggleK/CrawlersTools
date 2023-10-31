"""
- logging 日志拦截转发到 loguru
- 日志输出为json并精简&自定义字段
- 日志拦截与输出的 集成&单独 方法
"""
import time
from typing import List, Optional, Dict

from loguru import logger

from .handlers import default_handler, DEFAULT_HANDLER_FORMAT

TIME_FORMAT = time.strftime("%Y_%m_%d")


def init_logger(
        handlers: Optional[List[Dict]] = None,
        add_file_handler: bool = False,
        log_path: str = "./",
        file_handler_level: str = "INFO",
        **kwargs
):
    """
    一键配置 loguru ，所属程序本身的日志可直接 from loguru import logger ，即可正常处理

    :param handlers: 日志处理的 handlers ，参见 loguru.configure ，默认配置了 default_handler ，其他预置的可以从 .logger.handlers 导入
    :param add_file_handler: 开启后，会添加一个默认的文件输出 handler
    :param log_path: 日志文件的路径，默认当前目录
    :param file_handler_level: 文件输出 handler 的日志级别，默认 INFO
    :param kwargs: 其他要传递给 logger.configure 的参数
    """
    if handlers is None:
        handlers = [default_handler()]
    elif not isinstance(handlers, list):
        raise TypeError(
            "The 'handlers' parameter should be a list (or None), not: '%s'"
            % type(handlers).__name__
        )
    
    extra = kwargs.pop("extra", {})
    if not isinstance(extra, dict):
        raise TypeError(
            "The 'extra' parameter should be a dict (or None), not: '%s'"
            % type(extra).__name__
        )

    logger.configure(handlers=handlers, extra=extra, **kwargs)

    if add_file_handler:
        expire_date = kwargs.pop("expire_date", "1 days")
        logger.add(
            f"{log_path}/log_{TIME_FORMAT}_{file_handler_level.lower()}.log",
            encoding="UTF-8", enqueue=True, retention=expire_date,
            level=file_handler_level, format=DEFAULT_HANDLER_FORMAT
        )