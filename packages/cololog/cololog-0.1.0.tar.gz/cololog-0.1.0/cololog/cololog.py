# В файле cololog/cololog.py
import logging
from colorama import Fore, Style, init
import inspect
import os

# Инициализируем colorama
init(autoreset=True)

# Маппинг строковых уровней на числовые значения logging
level_list = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


class cololog:
    def __init__(self, name, level=['debug', 'info', 'warning', 'error', 'critical'], colors=None, path_print=True, log_to_file=False, log_dir='', log_file='log.log', console_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        
        # Преобразуем строки уровня в соответствующие числовые значения
        level_values = [level_list[lvl] for lvl in level if lvl in level_list]

        # Если в level нет допустимых значений, устанавливаем DEBUG по умолчанию
        if not level_values:
            level_values = [logging.DEBUG]

        # Устанавливаем общий уровень логирования
        self.logger.setLevel(min(level_values))  # Используем минимальный уровень из переданных

        self.path_print = path_print

        # Форматтер для сообщений
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Если нужно логировать в файл, добавляем файловый обработчик
        if log_to_file:
            # Проверяем и создаем папку, если она не существует
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Формируем путь к файлу логов
            log_path = os.path.join(log_dir, log_file) if log_dir else log_file

            # Файловый обработчик
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setLevel(min(level_values))  # Используем минимальный уровень из переданных
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)  # Устанавливаем отдельный уровень для консоли
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Настройки цветов по умолчанию
        self.colors = colors or {
            logging.DEBUG: Fore.CYAN,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA
        }

    def _log(self, level, message, *args, **kwargs):
        """Универсальный метод для логирования с цветом."""
        frame = inspect.currentframe().f_back
        caller = inspect.getframeinfo(frame)

        # Форматирование сообщений с контекстом
        if self.path_print:
            formatted_message = f"{message} (в {caller.filename}, строка {caller.lineno})"
        else:
            formatted_message = f"{message}"

        # Применяем цвет для уровня логирования
        color = self.colors.get(level, Style.RESET_ALL)
        message_with_color = color + formatted_message

        # Логирование
        self.logger.log(level, message_with_color, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self._log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._log(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log(logging.WARNING, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self._log(logging.CRITICAL, message, *args, **kwargs)
