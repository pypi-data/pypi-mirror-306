import time

from pythonjsonlogger.jsonlogger import JsonFormatter


class GMTJsonFormatter(JsonFormatter):
    converter = time.gmtime
