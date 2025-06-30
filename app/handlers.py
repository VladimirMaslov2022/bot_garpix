from aiogram import F, Router, exceptions
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv

load_dotenv()


import app.keyboards as kb
import app.operations as oper
import app.utils as u

router = Router()


class Register(StatesGroup):
    emaili = State()
    firstname = State()
    lastname = State()
    username = State()
    password = State()
    contact = State()
    educational_institution_and_level = State()
    year_of_education_and_spec = State()
    u_id = State()

registred = False

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    finded = await oper.find_user('file','id',message.from_user.id)
    # r = await req_m.find_user('email',finded['user_email'])

    if finded['status']=="f":
        await message.answer(f"Здравствуйте, {finded['data']['first_name']}!",reply_markup=kb.main_registred) # r['users'][0]['firstname']
        registred = True
    else:
        await message.answer(f"Здравствуйте! \nНе удалось найти ваш аккаунт, необходимо зарегестрироваться",reply_markup=kb.main_unregistred)
        await state.update_data(u_id=message.from_user.id)


@router.message(Command('stop')) # остановка регистрации
async def register_stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Регистрация прервана')


@router.message(Command('help'))
async def cmd_help_comand(message: Message):
    await message.answer(f'Помощь\n'+
                         f'Для регистрации напишите в чат сообщение "Регистрация" или  команду /register\n'+
                         f'Для того, что бы остановить регистрацию, напишите в чат команду /stop\n'+
                        #  f'Для поиска пользователя по email напишите в чат команду /find_user_by_email example@mail.ru (нужная почта)\n'+
                         f'Для регистрации на курс напишите в чат команду /use_promo и после пробела введите промокод, который вам выдала организация\n'+
                         f'Для доступа к курсам напишите в чат сообщение "Мои курсы" или команду /my_courses')
    
@router.message(F.text == 'Помощь')
async def cmd_help_text(message: Message):
    await message.answer(f'Помощь\n'+
                         f'Для регистрации напишите в чат сообщение "Регистрация" или  команду /register\n'+
                         f'Для того, что бы остановить регистрацию, напишите в чат команду /stop\n'+
                        #  f'Для поиска пользователя по email напишите в чат команду /find_user_by_email example@mail.ru (нужная почта)\n'+ 
                         f'Для регистрации на курс напишите в чат команду /use_promo и после пробела введите промокод, который вам выдала организация\n'+
                         f'Для доступа к курсам напишите в чат сообщение "Мои курсы" или команду /my_courses')


# @router.message(Command('find_user_by_email'))
# async def cmd_help(message: Message, command: CommandObject):
#     if str(message.from_user.id) in os.getenv('ADMINS_TG_ID'):
#         if command.args is None:
#             await message.answer('Вы не ввели почту для поиска')
#         else:
#             r = await req_m.find_user('email',command.args)
#             finded = await db.find_user('email',command.args)

#             if finded!=False:
#                 await message.answer(f"Пользователь существует: {finded['first_name']} (в файле)")
#             else:
#                 await message.answer(f'Такого пользователя не существует (в файле)')
            
#             if len(r['users'])!=0:
#                 await message.answer(f"Пользователь существует: {r['users'][0]['firstname']} (в moodle)")
#             else:
#                 await message.answer(f'Такого пользователя не существует (в moodle)')


@router.message(F.text == 'Регистрация') # начало регистрации через сообщение
async def register_start_text(message: Message, state: FSMContext):
    await state.set_state(Register.emaili) 
    await message.answer('Регистрация (Шаг 1 из 8)\n\nВведите ваш адрес электронной почты\n(Пример: user@exampe.com)') # спрашиваем почту


@router.message(Command('register')) # начало регистрации через команду
async def register_start_command(message: Message, state: FSMContext):
    await state.set_state(Register.emaili)
    await message.answer('Регистрация (Шаг 1 из 8)\n\nВведите ваш адрес электронной почты\n(Пример: user@exampe.com)') # спрашиваем почту

@router.message(F.text == 'Мои курсы') # через сообщение
async def courses_text(message: Message):
    # await oper.check_user_groups_and_courses_by_id(message.from_user.id)
    c = await oper.find_user('file','id',message.from_user.id)
    if c['status']=="f":
        cc = str(c['data']['user_course']).split(',')
        text = ''
        if cc[0]!='None':
            for course in cc:
                text+=f'\n - https://study.garpix.com/course/view.php?id={course}'
            await message.answer(f'Курсы{text}') 
        else:
            await message.answer(f'Доступные вам курсы не найдены') 
    else:
        await message.answer(f'Для доступа к курсам необходимо зарегистрироваться') 

@router.message(Command('my_courses')) # через команду
@u.registered_required
async def courses_command(message: Message):
    # await oper.check_user_groups_and_courses_by_id(message.from_user.id)
    c = await oper.find_user('file','id',message.from_user.id)
    if c['status']=="f": # if c['data']['user_course']!=None:
        cc = str(c['data']['user_course']).split(',')
        text = ''
        if cc[0]!='None':
            for course in cc:
                text+=f'\n - https://study.garpix.com/course/view.php?id={course}'
            await message.answer(f'Курсы{text}') 
        else:
            await message.answer(f'Доступные вам курсы не найдены') 
    else:
        await message.answer(f'Для доступа к курсам необходимо зарегистрироваться') 

@router.message(Command('create_promo'))
@u.registered_required
async def create_promo(message: Message, command: CommandObject):
    if str(message.from_user.id) in os.getenv('ADMINS_TG_ID'):
        if command.args is None:
            await message.answer('Вы не ввели необходимые данные')
        else:
            data = command.args.split(' ')
            promo = await oper.create_promo(data[0],data[1])
            await message.answer(f"Создан промокод\n<code>{promo['promo']}</code>\n"+
                                 f"Использования - {promo['use_count']}, для курса с id {promo['course']}"
                                 ,parse_mode=ParseMode.HTML)

@router.message(Command('use_promo'))
@u.registered_required
async def use_promo(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Пожалуйста, укажите промокод")
        return
    
    promo = command.args.strip()
    result = await oper.reg_to_course_by_promo(message.from_user.id, promo)
    
    if result['status'] == 'y':
        await message.answer("Промокод успешно активирован! Курс добавлен в ваш профиль.")
    else:
        reasons = {
            'user_not_registered': "Для использования промокодов необходимо завершить регистрацию",
            'invalid_promo': "Промокод недействителен или достиг лимита активаций",
            'course_exists': "У вас уже есть доступ к этому курсу",
            'moodle_user_not_found': "Ошибка: ваш аккаунт не найден в системе",
            'internal_error': "Произошла внутренняя ошибка. Попробуйте позже"
        }
        await message.answer(reasons.get(result.get('reason', "Не удалось активировать промокод")))
        
# async def use_promo(message: Message, command: CommandObject):
#     if command.args is None:
#         await message.answer('Вы не необходимые данные')
#     else:
#         promo = command.args
#         r = await oper.reg_to_course_by_promo(message.from_user.id,promo)
#         if r['status']=='y':
#             await message.answer(f"Успешно использован промокод\n{promo}")
#         else:
#             await message.answer(f"Промокод недействителен")

@router.message(Register.contact, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(contact=message.contact.phone_number)
    await state.set_state(Register.educational_institution_and_level)
    await message.answer('Регистрация (Шаг 7 из 8)\n\nНапишите название вашего образовательного '+
                         'учреждения и уровень образования (среднее, высшее)') # спрашиваем учреждение

@router.message(F.text)
async def register_process(message: Message, state: FSMContext):
    match await state.get_state():
        case Register.emaili: 

            if await u.valid_email(message.text):
                r = await oper.find_user('moodle','email',message.text)
                if len(r['users'])==1:
                    await state.update_data(firstname=r['users'][0]['firstname'])
                    await state.update_data(lastname=r['users'][0]['lastname'])
                    await state.update_data(username=r['users'][0]['username'])
                    await state.update_data(emaili=message.text)
                    
                    await message.answer(f"Найден аккаунт с таким же адресом электонной почты\nЗдравствуйте, {r['users'][0]['firstname']}!"+
                                         "\nНеобходимо завершить регистрацию для доступа к курсам")
                    await state.set_state(Register.contact)
                    await message.answer(f'Регистрация (Шаг 6 из 8)\n\nОтправьте ваш контакт для связи',reply_markup=kb.get_number)
                else:
                    await state.update_data(emaili=message.text) # пишем почту
                    await state.set_state(Register.firstname)
                    await message.answer('Регистрация (Шаг 2 из 8)\n\nВведите ваше имя') # спрашиваем имя
                # поиск чела на мудл по емейлу, если есть, завершение регистрации используя данные с мудл
            else:
                await message.answer("Почта введена неправильно, повторите попытку")

        case Register.firstname: 

            await state.update_data(firstname=message.text) # пишем имя
            await state.set_state(Register.lastname)
            await message.answer('Регистрация (Шаг 3 из 8)\n\nВведите вашу фамилию') # спрашиваем фамилию

        case Register.lastname: 

            await state.update_data(lastname=message.text) # пишем фамилию
            await state.set_state(Register.username)
            await message.answer('Регистрация (Шаг 4 из 8)\n\nПридумайте логин\n(Пример: example_user_1)') # спрашиваем логин

        case Register.username: 

            await state.update_data(username=message.text) # пишем логин 
            await state.set_state(Register.password)
            await message.answer('Регистрация (Шаг 5 из 8)\n\nПридумайте пароль\n(Пример: Example_01pas)') # спрашиваем пароль

        case Register.password:

            await state.update_data(password=message.text) # пишем пароль 
            await state.set_state(Register.contact)
            await message.answer('Регистрация (Шаг 6 из 8)\n\nОтправьте ваш контакт для связи',reply_markup=kb.get_number)

        case Register.educational_institution_and_level:

            await state.update_data(educational_institution_and_level=message.text) # пишем учреждение 
            await state.set_state(Register.year_of_education_and_spec)
            await message.answer('Регистрация (Шаг 8 из 8)\n\nНапишите, на каком вы курсе обучаетесь и направление обучения (спецаильность)') # спрашиваем курс и специальность

        case Register.year_of_education_and_spec:
            
            await state.update_data(year_of_education_and_spec=message.text)
            await state.update_data(u_id=message.from_user.id)
            data = await state.get_data()
            reg = await oper.register_user(data) # регаем
            match reg:
                case 'exists': 
                    await message.answer(f"Такой пользователь уже существует!\nЗдравствуйте, {data['firstname']}!",reply_markup=kb.main_registred)
                    registred = True
                case 'error':
                    await message.answer(f"При регистрации произошла ошибка!")
                case _:
                    await message.answer(f"{data['firstname']}, регистрация завершена!",reply_markup=kb.main_registred)
                    registred = True
            await state.clear()
