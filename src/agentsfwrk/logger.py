import logging
import multiprocessing
import sys

APP_LOGGER_NAME = 'CaiApp'

def setup_applevel_logger(logger_name=APP_LOGGER_NAME, file_name=None):
    """
    Setup the logger for the application.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Prevent the log messages from being duplicated in the python root logger

    # Define a consistent formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # StreamHandler for stdout
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # FileHandler for logging to a file
    if file_name and not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def get_multiprocessing_logger(file_name=None):
    """
    Setup the logger for the application for multiprocessing.
    """
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s - %(processName)-10s - %(name)s - %(levelname)s - %(message)s")

    # Adding StreamHandler only if it's not already added
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # Adding FileHandler only if it's not already added and a filename is provided
    if file_name and not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def get_logger(module_name, logger_name=None):
    """
    Get the logger for the module.
    """
    return logging.getLogger(logger_name or APP_LOGGER_NAME).getChild(module_name)
