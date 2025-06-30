import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

class BotLogger:
    def __init__(self):
        # Настраиваем основной логгер бота
        self.logger = logging.getLogger('bot')
        self.logger.setLevel(logging.INFO)
        
        # Отключаем propagation для aiogram логгера
        logging.getLogger('aiogram').propagate = False
        
        # Уникальный формат для наших логов
        bot_format = logging.Formatter(
            '%(asctime)s | BOT     | %(levelname)-8s | %(filename)-20s | %(funcName)-20s | %(message)s'
        )
        
        # Обработчик для файла
        file_handler = RotatingFileHandler(
            filename=os.getenv('LOG_FILE_NAME', 'bot.log'),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(bot_format)
        
        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(bot_format)
        
        # Добавляем обработчики только к нашему логгеру
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Настраиваем логгер aiogram для записи в тот же файл
        aiogram_logger = logging.getLogger('aiogram')
        aiogram_logger.setLevel(logging.INFO)
        aiogram_format = logging.Formatter(
            '%(asctime)s | AIOGRAM | %(levelname)-8s | %(message)s'
        )
        aiogram_file_handler = RotatingFileHandler(
            filename=os.getenv('LOG_FILE_NAME', 'bot.log'),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        aiogram_file_handler.setFormatter(aiogram_format)
        aiogram_logger.addHandler(aiogram_file_handler)

    def log(self, level: str, message: str, **kwargs):
        extra = {'custom_data': kwargs} if kwargs else None
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra=extra, stacklevel=3)

# Инициализация логгера
logger = BotLogger()

def log_info(message: str, **kwargs):
    logger.log('info', message, **kwargs)

def log_warning(message: str, **kwargs):
    logger.log('warning', message, **kwargs)

def log_error(message: str, **kwargs):
    logger.log('error', message, **kwargs)