# Alex Tech Logging Library

A custom logging library built on Python's standard logging module.

## Installation
pip install alex-tech-logging-library

## Usage

```python
from alex_tech_logging_library import setup_logger

# name is the application name and log_file is full path of the log file that exists.
logger = setup_logger(name='my_logger', log_file='app.log')

# Example log messages
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```