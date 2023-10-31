import json
from logging import Formatter
from typing import Tuple, List, Optional, Union

EXTRA_IGNORE_FIELDS_DEFAULT = (
    "name",
    "msg",
    "args",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
)


class JsonFormatter(Formatter):
    """格式化日志到Json，并删除某些字段"""

    def __init__(
        self,
        extra_ignore_keys: Optional[Union[List[str], Tuple[str]]] = EXTRA_IGNORE_FIELDS_DEFAULT,
        with_timestamp: bool = True,
        **kwargs
    ):
        """
        :param ignore_fields: 需要从 record[extra] 里忽略(排除)的字段
        :param kwargs: 这里的 key:val 会添加到格式化后的消息中 eg: app=explore
        """
        super(JsonFormatter, self).__init__()
        self.extra_ignore_keys = extra_ignore_keys
        self.with_timestamp = with_timestamp
        self.kwargs = kwargs

    def formatException(self, exc_info):
        exc_text = super(JsonFormatter, self).formatException(exc_info)
        return repr(exc_text)

    def format(self, record):
        message = {
            **self.kwargs,
            **self.get_extra_info(record),
        }
        if self.with_timestamp:
            message.update({"timestamp": self.format_timestamp(record.created)})

        if record.exc_info:
            message["message"] = self.formatException(record.exc_info)
            message["stack_trace"] = "".join(record.getMessage().split("\n"))
        else:
            message["message"] = record.getMessage()

        return json.dumps(message)

    @classmethod
    def format_timestamp(cls, time):
        return int(time * 1000)

    def get_extra_info(self, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in self.extra_ignore_keys
        }
