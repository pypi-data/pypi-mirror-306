import logging
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
import time
import os


class UTCFormatter(logging.Formatter):
    converter = time.gmtime

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            s = f"{t}.{record.msecs:03d}"
        return s


class ImmediateFlushingTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flush_on_write = True

    def emit(self, record):
        super().emit(record)
        if self.flush_on_write:
            self.flush()


def setup_logger(name, log_file, level=logging.INFO):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    formatter = UTCFormatter(
        fmt='%(asctime)s.%(msecs)03d | %(levelname)8s | %(funcName)s:%(lineno)d | %(process)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = ImmediateFlushingTimedRotatingFileHandler(log_file, when="MIDNIGHT", backupCount=60, utc=True)
    # print(datetime.fromtimestamp(file_handler.rolloverAt, tz=timezone.utc))
    file_handler.suffix = "%Y%m%d"
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Usage
if __name__ == "__main__":
    logger = setup_logger('my_logger', 'logs/day_app.log')

    while True:
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        time.sleep(1)
