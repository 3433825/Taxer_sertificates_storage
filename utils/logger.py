import logging


def get_logger(name):
    logger = logging.getLogger(name)
    # Якщо обробники вже додані (наприклад, через pytest), не додаємо їх знову
    if not logger.handlers:
        logger.setLevel(logging.INFO)
    return logger
