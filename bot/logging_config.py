import logging
import os
import traceback

_logger_initialized = False


def setup_logging():
    global _logger_initialized
    
    if _logger_initialized:
        return
    
    os.makedirs('logs', exist_ok=True)
    
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    if not root_logger.handlers:
        file_handler = logging.FileHandler('logs/trading_bot.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    _logger_initialized = True


def get_logger(name):
    setup_logging()
    return logging.getLogger(name)


def log_exception(logger, message="Exception occurred"):
    logger.error(f"{message}: {traceback.format_exc()}")