import sys

from .sys_redirect import FakeStdOut

from loguru import logger
import os
if not sys.stdout:
    sys.stdout = FakeStdOut()

# 创建日志文件夹
if not os.path.exists("logs"):
    os.makedirs("logs")

# 移除默认的配置
logger.remove()

logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}", level="INFO")

# 配置文件日志输出
logger.add("logs/{time:YYYY-MM-DD}_debug.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}", level="DEBUG",
           rotation="00:00",
           filter=lambda record: record["level"].name == "DEBUG")
logger.add("logs/{time:YYYY-MM-DD}_info.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}", level="INFO",
           rotation="00:00",
           filter=lambda record: record["level"].name == "INFO")
logger.add("logs/{time:YYYY-MM-DD}_warning_error.log", format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}",
           level="WARNING", rotation="00:00",
           filter=lambda record: record["level"].name in ["WARNING", "ERROR"])


def get_logger():
    return logger
