import os # ,logging
from dotenv import load_dotenv

import app.utils as u
import app.req_moodle as req_m
import app.req_file as req_f

load_dotenv(".env")
from app.logger import log_info, log_error

# logging.basicConfig(level=logging.INFO, filename=os.getenv('LOG_FILE_NAME'),filemode="w")

async def find_user(m, crit, val):
    match m:
        case 'moodle':
            return await req_m.find_user(crit,val)
        case 'file':
            await u.get_file()
            return await req_f.find_user(crit,val)

async def register_user(data):
    log_info("Starting register process")
    await u.get_file()
    finded_user_moodle = await find_user('moodle','email',data['emaili']) # поиск на moodle по почте
    if len(finded_user_moodle['users'])!=0: # если есть
        finded_user_file = await req_f.find_user('email',data['emaili']) # поиск в файле по почте
        if finded_user_file["status"]=="f": # если есть
            os.remove(os.getenv('XLSX_FILE_NAME'))
            return "exists"
        elif finded_user_file["status"]=="n": # иначе
            await req_f.reg_user(data)  # запись в файл
            await u.return_file() 
            os.remove(os.getenv('XLSX_FILE_NAME'))
            return ""
    else: # иначе
        r = await req_m.reg_user(data) # регистрация на moodle 
        if r == "reg":
            finded_user_file = await req_f.find_user('email',data['emaili']) # поиск в файле по почте
            if finded_user_file["status"]=="f": # если есть
                os.remove(os.getenv('XLSX_FILE_NAME'))
                return "exists"
            elif finded_user_file["status"]=="n": # иначе
                await req_f.reg_user(data)  # запись в файл
                await u.return_file() 
                os.remove(os.getenv('XLSX_FILE_NAME'))
                return ""
        else:
            return "error"


async def reg_to_groups(user_tg_id):
    log_info("Starting register to group process")
    await u.get_file()
    data = await find_user("file","id",user_tg_id)
    if data['user_course']!=None:
        user_moodle_id = await find_user("moodle","email",data['data']['user_email'])
        cc = data['user_course'].split(',')
        for course in cc:
            await req_m.add_user_to_course(course,user_moodle_id['users'][0]['id']) 
    os.remove(os.getenv('XLSX_FILE_NAME'))

async def reg_to_courses(user_tg_id):
    log_info("Starting register to course process")
    await u.get_file()
    data = await find_user("file","id",user_tg_id)
    if data['user_group']!=None:
        user_moodle_id = await find_user("moodle","email",data['data']['user_email'])
        cc = data['user_group'].split(',')
        for course in cc:
            await req_m.add_user_to_course(course,user_moodle_id['users'][0]['id'])
    os.remove(os.getenv('XLSX_FILE_NAME'))


async def reg_to_course_by_promo(user_tg_id: int, promo: str) -> dict:
    log_info("Starting register to course by promo process")
    """
    Регистрирует пользователя на курс по промокоду с проверкой дублирования
    Возвращает:
    - {'status': 'y'} - успешно
    - {'status': 'n', 'reason': '...'} - ошибка (с указанием причины)
    """
    try:
        # Получаем данные пользователя
        await u.get_file()
        user_data = await find_user("file", "id", user_tg_id)
        if user_data['status'] != "f":
            return {'status': 'n', 'reason': 'user_not_registered'}
        # Проверяем промокод
        promo_data = await req_f.check_promo(promo)
        if promo_data['status'] != 'v':
            return {'status': 'n', 'reason': 'invalid_promo'}
        course_id = promo_data['course']
        current_courses = user_data['data']['user_course']
        # Проверяем, есть ли уже такой курс у пользователя
        if current_courses:
            course_list = current_courses.split(',')
            if str(course_id) in course_list:
                return {'status': 'n', 'reason': 'course_exists'}
        # Добавляем курс
        await req_f.add_course_to_user(course_id, user_tg_id)
        # Регистрируем на Moodle
        moodle_user = await find_user("moodle", "email", user_data['data']['user_email'])
        if not moodle_user or not moodle_user.get('users'):
            return {'status': 'n', 'reason': 'moodle_user_not_found'}
        await req_m.add_user_to_course(course_id, moodle_user['users'][0]['id'])
        await u.return_file()
        return {'status': 'y'}
    except Exception as e:
        log_error("Error in reg_to_course_by_promo", error=str(e), user_id=user_tg_id)
        return {'status': 'n', 'reason': 'internal_error'}
    finally:
        if os.path.exists(os.getenv('XLSX_FILE_NAME')):
            os.remove(os.getenv('XLSX_FILE_NAME'))

# async def reg_to_course_by_promo(user_tg_id,promo):
#     log_info("Starting register to course by promo process")
#     await u.get_file()
#     data = await find_user("file","id",user_tg_id)
#     promo_f = await req_f.check_promo(promo)
#     if promo_f['status']=='v':
#         await req_f.add_course_to_user(promo_f['course'],user_tg_id)
#         user_moodle_id = await find_user("moodle","email",data['data']['user_email'])
#         await req_m.add_user_to_course(promo_f['course'],user_moodle_id['users'][0]['id'])
#         await u.return_file()
#         os.remove(os.getenv('XLSX_FILE_NAME'))
#         return {'status':'y'}
#     else:
#         os.remove(os.getenv('XLSX_FILE_NAME'))
#         return {'status':'n'}

async def create_promo(course,use_count):
    log_info("Starting create promo process")
    await u.get_file()
    promo = await req_f.create_promo(course,use_count)
    await u.return_file()
    os.remove(os.getenv('XLSX_FILE_NAME'))
    return promo