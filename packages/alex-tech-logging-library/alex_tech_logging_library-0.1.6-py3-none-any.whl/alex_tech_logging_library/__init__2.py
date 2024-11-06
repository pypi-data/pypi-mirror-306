import logging
from logging.handlers import TimedRotatingFileHandler
import time
import os
from datetime import datetime, timedelta, timezone

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

class AlignedTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.flush_on_write = True
        self.alignRollover()

    def alignRollover(self):
        current_time = datetime.now(timezone.utc) # get utc time now
        next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
        self.rolloverAt = int(next_minute.timestamp())
        print(f"Current time: {current_time}")
        print(f'Next minute: {next_minute}')
        print(f"Rollover at: {datetime.fromtimestamp(self.rolloverAt, tz=timezone.utc)}")

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

    file_handler = AlignedTimedRotatingFileHandler(log_file, when="M", interval=1, backupCount=60, utc=True)
    file_handler.suffix = "%Y%m%d-%H%M"
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
    logger = setup_logger('my_logger', 'logs/app.log')

    while True:
        logger.info("This is an info message")
        time.sleep(1)