import re,os
import pycurl as curl
from dotenv import load_dotenv

from functools import wraps
from aiogram.types import Message, CallbackQuery

load_dotenv()
from app.logger import log_info, log_error, log_warning
# logging.basicConfig(level=logging.INFO, filename=os.getenv('LOG_FILE_NAME'),filemode="w")

import app.operations as oper

async def valid_email(email):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.match(email_pattern, email)

async def valid_username(username):
    username_pattern = r"^[a-z_]*[0-9][a-z0-9_]*$"
    return re.match(username_pattern, username)

async def valid_password(password):
    password_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.match(password_pattern, password)


async def get_file():
    try:
        file_name = os.getenv('XLSX_FILE_NAME')
        file_src = os.getenv('NEXTCLOUD_URL')
        with open(file_name, "wb") as f:
            c = curl.Curl()
            c.setopt(c.URL, file_src)
            c.setopt(c.WRITEDATA, f)
            c.setopt(c.USERNAME, os.getenv('NEXTCLOUD_USERNAME'))
            c.setopt(c.PASSWORD, os.getenv('NEXTCLOUD_PASSWORD')) 
            c.perform()
            c.close()
        log_info("File downloaded from nextcloud")
        return True
    except Exception as e:
        if(e.args[0] == 28):
            template = f"Retry download file, because error when download file from nextcloud {0}. details:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            log_error('Retry download file, because error when download file from nextcloud', details=e.args)
            await get_file()
        else:
            template = "Error when download file from nextcloud {0}. details:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            log_error('Error when download file from nextcloud', details=e.args)
            return False


async def return_file():
    try:
        file_name = os.getenv('XLSX_FILE_NAME')
        file_src = os.getenv('NEXTCLOUD_URL')
        with open(file_name, "rb") as f:
            c = curl.Curl()
            c.setopt(c.URL, file_src)
            c.setopt(c.UPLOAD, 1)
            c.setopt(c.READDATA, f)
            c.setopt(c.USERNAME, os.getenv('NEXTCLOUD_USERNAME'))
            c.setopt(c.PASSWORD, os.getenv('NEXTCLOUD_PASSWORD')) 
            c.perform()
            c.close()
        log_info("File uploaded to nextcloud")
        return True
    except Exception as e:
        template = "Error when upload file to nextcloud {0}. details:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        log_error('Error when upload file to nextcloud', details=e.args)
        return False

async def is_user_registered(user_id):
    """Проверяет, зарегистрирован ли пользователь"""
    user_data = await oper.find_user('file', 'id', user_id)
    log_info('Is user registred?')
    if(user_data['status'] == "f"):
        log_info('User is not registred')
    return user_data['status'] == "f"

def registered_required(func):
    """Декоратор для проверки регистрации"""
    @wraps(func)
    async def wrapper(message: Message | CallbackQuery, *args, **kwargs):
        if not await is_user_registered(message.from_user.id):
            if isinstance(message, Message):
                await message.answer("Для использования этой функции необходимо зарегистрироваться!")
            else:  # CallbackQuery
                await message.answer("Для использования этой функции необходимо зарегистрироваться!")
                await message.answer()
            return
        return await func(message, *args, **kwargs)
    return wrapper