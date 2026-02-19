import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "logs/bot.log", logger_name: str | None = None) -> logging.Logger:
    """
    Creates/returns a logger that writes to:
      - a rotating file handler at `log_file`
      - console stream

    IMPORTANT:
    - Uses a unique logger name per log file by default so multiple log files work.
    """

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Unique logger per log file (so handlers don't conflict)
    if logger_name is None:
        safe_name = log_file.replace("\\", "_").replace("/", "_").replace(":", "_")
        logger_name = f"trading_bot__{safe_name}"

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # If this logger already has handlers, don't add duplicates
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
