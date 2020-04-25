import logging
from logging.handlers import RotatingFileHandler
from contextlib import contextmanager
# import os

# настройка логирования
# формат лога
log_formatter = logging.Formatter('[%(asctime)s] [LINE:%(lineno)d] %(levelname)-8s: %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
 
# полный лог файл
# os.system('mkdir log')
file_handler = RotatingFileHandler('info.log', mode = 'a', maxBytes = 10485760,
                                 backupCount = 10, encoding = 'utf-8', delay = 0)
file_handler.setFormatter(log_formatter)
 
# лог файл только ошибок
file_error_handler = RotatingFileHandler('error.log', mode = 'a', maxBytes = 10485760,
                                 backupCount = 10, encoding = 'utf-8', delay = 0)
file_error_handler.setFormatter(log_formatter)
 
# инициализация логирования
err_logger = logging.getLogger('bad_log')
err_logger.setLevel(logging.ERROR)
info_logger = logging.getLogger('info_log')
info_logger.setLevel(logging.INFO)

info_logger.addHandler(file_handler)
err_logger.addHandler(file_error_handler)


@contextmanager
def log():
	yield
	file_handler.close()
	file_error_handler.close()

# logger = logging.getLogger('corona')

# logger.setLevel(logging.DEBUG)

# handler = logging.FileHandler('corona.txt', 'a', 'utf-8')
# formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")

# handler.setFormatter(formatter)
# logger.addHandler(handler)