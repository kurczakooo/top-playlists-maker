import logging

def setup_logger(filename: str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # delete handlers if there are any
    if logger.hasHandlers():
        logger.handlers.clear()

    # Format 
    log_format = f"%(asctime)s | %(levelname)s | {filename} | %(message)s\n"
    date_format = "%Y-%m-%d %H:%M:%S"

    # set handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    logger.addHandler(handler)

    return logger