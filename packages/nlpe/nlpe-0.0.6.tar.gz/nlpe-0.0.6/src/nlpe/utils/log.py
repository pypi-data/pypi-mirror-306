import logging
import os
from datetime import datetime
from pathlib import Path

_global_logger = None
import socket

def global_logger(log_dir: str = None, logger_name: str = None) -> logging.Logger:
    global _global_logger
    if isinstance(_global_logger, logging.Logger):
        return _global_logger

    if not isinstance(log_dir, Path) or not isinstance(log_dir, str) or len(log_dir) == 0:
        log_dir = Path(os.environ.get("LOG_DIR", Path("log", socket.gethostname())))
    if not isinstance(logger_name, str) or len(logger_name) == 0:
        logger_name = os.environ.get("PROJECT_NAME", "nlpe")
    os.makedirs(log_dir, exist_ok=True)
    ph = Path(log_dir, f"{logger_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    formatter = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] %(message)s")

    _global_logger = logging.getLogger(logger_name)
    _global_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(str(ph))
    file_handler.setFormatter(formatter)
    _global_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _global_logger.addHandler(console_handler)

    return _global_logger
