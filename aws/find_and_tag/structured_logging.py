import json
import logging


class StructuredFormatter(logging.Formatter):
    """A custom logging formatter for logging messages using the
    StructuredMessage class

    Args:
        Formatter (class): the Python's logging package Formatter class.
            See more: https://github.com/python/cpython/blob/master/Lib/logging/__init__.py
    """
    default_format = json.dumps({
        'message': '%(message)s',
        'time': '%(asctime)s',
        'level': '%(levelname)s'
    }, sort_keys=True).replace('\\"', '\"') + '\n'

    debug_format = json.dumps({
        'message': '%(message)s',
        'time': '%(asctime)s',
        'src_function': '%(funcName)s',
        'src_module': '%(module)s',
        'src_line': '%(lineno)d',
        'src_path': '%(pathname)s',
        'level': '%(levelname)s'
    }, sort_keys=True).replace('\\"', '\"') + '\n'

    def __init__(self):
        super().__init__(fmt=StructuredFormatter.default_format)

    def format(self, record):
        self._style._fmt = StructuredFormatter.default_format

        if record.levelno == logging.DEBUG or record.levelno >= logging.ERROR:
            self._style._fmt = StructuredFormatter.debug_format

        return logging.Formatter.format(self, record)


def init():
    for handler in logging.getLogger().handlers:
        handler.setFormatter(StructuredFormatter())
