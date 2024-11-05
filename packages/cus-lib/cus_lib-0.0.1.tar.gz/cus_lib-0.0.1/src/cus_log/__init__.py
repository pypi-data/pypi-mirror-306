"""
usage:

from log_config import setup_logger

logger = setup_logger("my_project.cus_log")
logger.debug("This is a debug message.")
"""

# 导入 cus_log 包中的公共接口
from .cus_log import setup_logger
