import os
from logging import INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from sys import exit as exit_ex

from settings import path_to_html, path_to_little_ico, path_to_settings


def __get_logger__(name: str, file: str) -> object:
    """
    Функция создания логгера
    :param name: имя файла логгера
    :return: объект логгера
    """
    if 'log' not in os.listdir(path_to_settings):
        os.mkdir(os.path.join(path_to_settings, 'log'))

    file_logger = getLogger(name)
    file_logger.setLevel(INFO)

    logger_format = (
        '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = Formatter(fmt=logger_format, datefmt=date_format)

    handler = RotatingFileHandler(
        fr'settings/log/{file}.log',
        maxBytes=5252880,
        backupCount=5,
    )

    handler.setFormatter(formatter)
    file_logger.addHandler(handler)

    return file_logger


LOGGER = __get_logger__

def clean_after_app():
    logger = LOGGER('clean', 'app')
    logger.warning('Начинаю очистку файлов после программы')

    if os.path.isfile(path_to_little_ico):
        os.remove(path_to_little_ico)
    if os.path.isfile(path_to_html):
        os.remove(path_to_html)
    
    logger.warning('Очистка окончена? закрываю программу')
    exit_ex()
