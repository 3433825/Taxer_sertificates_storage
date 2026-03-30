import logging
import os
from datetime import datetime


def get_logger(name):
    logger = logging.getLogger(name)

    # Якщо обробники вже додані, не додаємо їх знову
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Створюємо папку logs, якщо її немає
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Формуємо ім'я файлу на основі поточної дати
        log_filename = datetime.now().strftime("%d-%m-%Y.log")
        log_path = os.path.join(log_dir, log_filename)

        # Налаштування формату
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Додаємо запис у файл
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
